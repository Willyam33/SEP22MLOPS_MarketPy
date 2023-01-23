from fastapi import FastAPI, Header, HTTPException 
from pydantic import BaseModel, Field
from typing import List, Optional
import access
import log
import data_manipulation
import database_functions
import datetime
import pandas as pd
import properties
from joblib import load

pool_possible_values = 3
jacuzzi_possible_values = 2

class Input(BaseModel):
    """ Classe décrivant les caractéritiques du logement à estimer """
    rating:float
    tag:str
    bedroom:int
    bathroom:int
    pool:int
    jacuzzi:int
    nb_equip:int

api = FastAPI(
    title="API for Pricing Rental Prediction",
    description="Predicting the pricing of a holiday rental with inputs",
    version="1.0.0"
)

def prepare_results_for_API_return(results,columns=""):
    # Dictionnary - Ready for API
    dict_results = []
    if columns == "":
        for dict_row in results.mappings():
            dict_results.append(dict_row)
    else:
        columns_list=columns.split(", ")
        for result in results.fetchall():
            dict_row=dict(zip(columns_list,result))
            dict_results.append(dict_row)   
    return dict_results


def manage_access_control(access_control):
    if access_control['status']==access.ERROR:
        raise HTTPException(status_code=500, detail=access_control['error_code'])
    elif access_control['status']==access.DENIED:
        raise HTTPException(status_code=401, detail=access_control['error_code'])

@api.get('/', name="Vérify API is UP")
def get_index():
    """
    Returns API UP...
    """
    return 'API UP...'

@api.post('/predict', name="Predict price")
def predict(
        input: Input,
        username=Header(None, description='user login'), 
        password=Header(None, description='user password')):
    """
    Doing prediction
    """

    """ Access control """
    manage_access_control(access.verify_user_access(username,password))

    """ Coherency control """
    if ( (input.bathroom > 10 or input.bathroom < 0) or
         (input.bedroom > 10 or input.bedroom < 0) or
         (input.tag != "" and input.tag != "Superhôte") or
         (input.pool > 2 or input.pool < 0) or
         (input.jacuzzi > 1 or input.jacuzzi < 0) or
         (input.nb_equip > 40 or input.nb_equip <0) ):
        return log.error_messages['NOT_IN_RANGE']

    data=pd.DataFrame({
        'rating': input.rating,
        'bedroom': input.bedroom,
        'bathroom': input.bathroom,
        'nb_equip': input.nb_equip},index=[0])
    
    for i in range(pool_possible_values):
        data['pool_'+str(i)]=0
    data['tag_Pas de tag']=0
    data['tag_Superhôte']=0
    for i in range(jacuzzi_possible_values):
        data['jacuzzi_'+str(i)]=0

    if input.tag=="Superhôte":
        data['tag_Superhôte']=1
    else:
        data['tag_Pas de tag']=1

    for i in range(jacuzzi_possible_values):
        if input.jacuzzi==i:
            data['jacuzzi_'+str(i)]=1

    for i in range(pool_possible_values):
        if input.pool==i:
            data['pool_'+str(i)]=1

    production_model_id = database_functions.get_production_model_id()
    if production_model_id==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif production_model_id!=0:
        # Getting production pipeline 
        try:
            pipeline=load(properties.model_folder+properties.model_file)
        except:
            return log.error_messages['MODEL_NOT_FOUND']

        """ Predicting """
        prediction=data_manipulation.predict(pipeline,data)[0]

        """ Saving Prediction in the database """
        database_functions.save_prediction_metadata(
            date_prm = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S"), 
            model_id_prm = production_model_id,
            user_id_prm = database_functions.get_user_id(username),
            rating_prm = input.rating,
            tag_prm = input.tag,
            bedroom_prm = input.bedroom,
            bathroom_prm = input.bathroom,
            pool_prm = input.pool,
            jacuzzi_prm = input.jacuzzi,
            nb_equip_prm = input.nb_equip,
            result_prm = prediction)

        return prediction
    else:
        return log.error_messages['NO_MODEL_IN_PRODUCTION']

@api.get('/predictions/{username_who_did_predictions}', name="Get predictions")
def get_predictions(
        username_who_did_predictions: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting predictions done by an identified user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    results=database_functions.get_predictions_for_user(username_who_did_predictions)
    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=prepare_results_for_API_return(results)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION_FOR_USER']+username_who_did_predictions
        else:
            return dict_results

@api.get('/predictions_details/{username_who_did_predictions}', name="Get predictions and model details for an identified user")
def get_predictions_details(
        username_who_did_predictions: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting predictions done by an identified user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    results=database_functions.get_predictions_details_for_user(username_who_did_predictions)
    columns=database_functions.get_predictions_details_columns()

    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=prepare_results_for_API_return(results,columns)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION_FOR_USER']+username_who_did_predictions
        else:
            return dict_results

@api.get('/predictions', name="Get predictions")
def get_predictions(
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Getting all predictions occured, with models and users informations
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    results=database_functions.get_all_predictions()
    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        dict_results=prepare_results_for_API_return(results)
        if len(dict_results)==0:
            return log.warning_messages['NO_PREDICTION']
        else:
            return dict_results

@api.delete('/delete_user/{username_to_delete}', name="Delete user from database")
def delete_user(
        username_to_delete: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Deleting user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    if username_to_delete not in database_functions.get_users_username():
        return log.error_messages['USER_UNKNOWN']

    status=database_functions.delete_user(username_to_delete)
    if status==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return username_to_delete+log.success_messages['USER_DELETED']

@api.put('/add_user/{username_to_add}/{password_to_add}', name="Add user to database")
def add_user(
        username_to_add: str,
        password_to_add: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Adding new user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    users_username=database_functions.get_users_username()
    if users_username==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif username_to_add in users_username:
        return username_to_add+log.error_messages['USER_ALREADY_EXISTS']

    results=database_functions.add_user(username_to_add,password_to_add)
    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return username_to_add+log.success_messages['USER_ADDED']

@api.delete('/delete_model/{model}', name="Delete model from database")
def delete_model(
        model: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Deleting user
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    models_name=database_functions.get_models_name()
    if models_name==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif model not in models_name:
        return model+log.error_messages['MODEL_UNKNOWN']

    results=database_functions.delete_model(model)
    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return model+log.success_messages['MODEL_DELETED']

@api.put('/add_model/{library}/{model}', name="Add model template to database")
def add_model(
        library: str,
        model: str,
        username=Header(None, description='admin login'), 
        password=Header(None, description='admin password')):
    """
    Adding new model
    """

    """ Access control """
    manage_access_control(access.verify_admin_access(username,password))

    """ Coherency control """
    models_name=database_functions.get_models_name()
    if models_name==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    elif model in models_name:
        return model+log.error_messages['MODEL_ALREADY_IN_BASE']

    results=database_functions.add_model(library,model)
    if results==-1:
        raise HTTPException(status_code=500, detail=log.error_messages['DATABASE_ERROR'])
    else:
        return model+log.success_messages['MODEL_ADDED']

