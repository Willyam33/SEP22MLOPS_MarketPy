import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sklearn
from sklearn.metrics import mean_absolute_percentage_error
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
import datetime

from joblib import dump
import database_functions
import data_manipulation
import properties 
import log

def manage_versionning(version,production_model_name,new_model_name):
    # Deformating version
    x,y=version[1:].split('.')
    # If new and old model name are not the same
    if production_model_name!=new_model_name:
        # Then updating first number
        x=int(x)+1
        y=0
    else:
        # Else updating second number
        y=int(y)+1
    # Formating version
    return ("V"+str(x)+"."+str(y))

def train_and_save_pipeline(model, features, target, dataset_id):
    ''' Train model and save it
    '''
    pipeline, score = data_manipulation.train_and_score_model(model, features, target)

    # Updating production model metadata (version and name)
    date = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S")
    production_model_id, production_model_version, production_model_name = \
        database_functions.get_production_model_version_and_name()

    if (production_model_id==-1):
        print(log.error_messages['UNABLE_TO_MANAGE_PRODUCTION_MODELS'])
        return -1
    elif (production_model_id==0): # If production model doesn't exists, Then 
        new_version="V1.0"
    else:
        # Removing current version 
        status=database_functions.remove_model_from_production(production_model_id,date)
        if status==-1:
            print(log.error_messages['UNABLE_TO_MANAGE_PRODUCTION_MODELS'])
            return -1
        # Creating new version
        new_version = manage_versionning(production_model_version,production_model_name,model['name']) 

    # Managing scores and dataset used for training
    scores=format(score, ".2f")
    dataset_scoring_ids=str(dataset_id)

    # Saving pipeline file
    try:
        dump(pipeline, properties.model_folder+properties.model_file)
    except:
        print(log.error_messages['UNABLE_TO_SAVE_PRODUCTION_PIPELINE_FILE'])
        print(log.warning_messages['NO_MODEL_IN_PRODUCTION'])       
        return -1

    # Saving in Database
    status=database_functions.save_new_production_model_metadata(
        date_prm=date,
        version_prm=new_version,
        name_prm=model['name'],
        scores_prm=scores,
        dataset_scoring_ids_prm=dataset_scoring_ids)
    if status==-1:
        print(log.error_messages['UNABLE_TO_MANAGE_PRODUCTION_MODELS'])
        print(log.warning_messages['NO_MODEL_IN_PRODUCTION'])
        return -1
    else:
        print(log.success_messages['NEW_MODEL_IN_PRODUCTION'])
        return 0




