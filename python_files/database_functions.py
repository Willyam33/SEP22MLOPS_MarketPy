from sqlalchemy.engine import create_engine
import datetime
import log


# By convention, -1 is used for error return code

# creating a connection to the database
# mysql_url = 'my_mysql' 
mysql_url = '172.17.0.2' 
mysql_user = 'root'
mysql_password = 'msq3!xAk3c'  
database_name = ''

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# creating the connection
mysql_engine = create_engine(connection_url)

def create_database():
    try:
        with mysql_engine.connect() as connection:
            connection.execute('CREATE DATABASE IF NOT EXISTS essai;')
            connection.execute('CREATE TABLE essai.datasets ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    name VARCHAR(64), \
                                    import_date VARCHAR(64), \
                                    invalid BIT, \
                                    size_before_cleaning INT, \
                                    size_after_cleaning INT);')
            connection.execute('CREATE TABLE essai.production_models ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    date VARCHAR(32), \
                                    version VARCHAR(8), \
                                    name VARCHAR(64), \
                                    scores VARCHAR(64), \
                                    dataset_scoring_ids VARCHAR(64), \
                                    remove_date VARCHAR(32));')
            connection.execute('CREATE TABLE essai.models ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    name VARCHAR(32), \
                                    library VARCHAR(64));')
            connection.execute('INSERT INTO essai.models (name, library) VALUES ("LinearRegression","sklearn.linear_model");')
            connection.execute('INSERT INTO essai.models (name, library) VALUES ("DecisionTreeRegressor","sklearn.tree");')
            connection.execute('INSERT INTO essai.models (name, library) VALUES ("RandomForestRegressor","sklearn.ensemble");')
            connection.execute('CREATE TABLE essai.predictions ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    date VARCHAR(64), \
                                    model_id INT, \
                                    user_id INT, \
                                    rating FLOAT, \
                                    tag VARCHAR(64), \
                                    bedroom INT, \
                                    bathroom INT, \
                                    pool INT, \
                                    jacuzzi INT, \
                                    nb_equip INT, \
                                    result FLOAT);')
            connection.execute('CREATE TABLE essai.users ( \
                                    id INT PRIMARY KEY AUTO_INCREMENT, \
                                    username VARCHAR(64), \
                                    password VARCHAR(64));')
            connection.execute('INSERT INTO essai.users (username, password) VALUES ("admin","admin");')
            connection.execute('INSERT INTO essai.users (username, password) VALUES ("user1","pass1");')
            connection.execute('INSERT INTO essai.users (username, password) VALUES ("user2","pass2");')
    except log as e:
        print(log.error_messages["DATABASE_CREATION_ERROR"])
        print(e)    

def drop_database():
    try:
        with mysql_engine.connect() as connection:
            connection.execute('DROP DATABASE essai;')
    except log as e:
        print(log.error_messages["DATABASE_DROP_ERROR"])
        print(e)    

############################# GENERIC FUNCITONS #############################################

def get_elements_from_select(command:str):
    ''' Executing mysql sqlalchemy engine with select command
        returns -1 if error, else results
    '''
    try:
        with mysql_engine.connect() as connection:
            results=connection.execute(command)
            return results
    except:
        return -1

def set_elements_for_insert(command:str):
    ''' Executing mysql sqlalchemy engine with insert command
        returns -1 if error, else last row id
    '''

    try:
        with mysql_engine.connect() as connection:
            lastrowid=connection.execute(command).lastrowid
            return lastrowid
    except:
        return -1

def set_elements_for_update(command:str):
    ''' Executing mysql sqlalchemy engine with update command
        returns -1 if error, else 0
    '''
    try:
        with mysql_engine.connect() as connection:
            connection.execute(command)
        return 0
    except:
        return -1

def delete_elements(command:str):
    ''' Deleting elements
        returns -1 if error, else 0
    '''
    try:
        with mysql_engine.connect() as connection:
            results=connection.execute(command)
        return 0
    except:
        return -1


############################# DATASET METADATA ACCESS #######################################

def save_new_dataset_metadata(filename_prm:str,
                              date_prm:str,
                              invalid_prm:bool,
                              size_before_cleaning_prm:int,
                              size_after_cleaning_prm:int):
    ''' Saving new dataset metadata
        returns -1 if error, else last row id
    '''

    if invalid_prm:
        command = \
            'INSERT INTO essai.datasets (name, import_date, invalid) VALUES \
            ("{filename}","{date}",{invalid});'.format(
                filename=filename_prm,
                date=date_prm,
                invalid=1,
                size_before_cleaning = 0,
                size_after_cleaning = 0
            )
    else:
        command = \
            'INSERT INTO essai.datasets (name, import_date, invalid, size_before_cleaning, size_after_cleaning) VALUES \
            ("{filename}","{date}",{invalid},{size_before_cleaning},{size_after_cleaning});'.format(
                filename=filename_prm,
                date=date_prm,
                invalid=0,
                size_before_cleaning = size_before_cleaning_prm,
                size_after_cleaning = size_after_cleaning_prm
        )
 
    return set_elements_for_insert(command)

############################# MODEL METADATA ACCESS #######################################

def save_new_production_model_metadata(date_prm:str,
                                       version_prm:str,
                                       name_prm:str,
                                       scores_prm:str,
                                       dataset_scoring_ids_prm:str):
    ''' Saving new production model metadata
        returns -1 if error, else last row id
    '''

    command = \
        'INSERT INTO essai.production_models (date, version, name, scores, dataset_scoring_ids) VALUES  \
        ("{date}","{version}","{name}","{scores}","{dataset_scoring_ids}");'.format(
            date=date_prm,
            version=version_prm,
            name=name_prm,
            scores = scores_prm,
            dataset_scoring_ids = dataset_scoring_ids_prm
        )
    return set_elements_for_insert(command)

def save_prediction_metadata(date_prm:str,
                             model_id_prm:int,
                             user_id_prm:int,
                             rating_prm:float,
                             tag_prm:str,
                             bedroom_prm:int,
                             bathroom_prm:int,
                             pool_prm:int,
                             jacuzzi_prm:int,
                             nb_equip_prm:int,
                             result_prm:float):
    ''' Recording prediction, features and user id
        returns -1 if error, else last row id
    '''

    command = \
        'INSERT INTO essai.predictions (date, model_id, user_id, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result) VALUES  \
        ("{date}",{model_id},{user_id},{rating},"{tag}",{bedroom},{bathroom},{pool},{jacuzzi},{nb_equip},{result});'.format(
            date=date_prm,
            model_id=model_id_prm,
            user_id=user_id_prm,
            rating = rating_prm,
            tag = tag_prm,
            bedroom = bedroom_prm,
            bathroom = bathroom_prm,
            pool = pool_prm,
            jacuzzi = jacuzzi_prm,
            nb_equip = nb_equip_prm,
            result = result_prm           
        )
    return set_elements_for_insert(command)

def get_production_model_informations(command:str):
    ''' Getting production model informations
        with sql command
        returns -1 if error, 0 if no production model, else query results
    '''

    results=get_elements_from_select(command)
    if results==-1:
        return results
    else:
        results_list=results.fetchall()
        if len(results_list)==0:
            return 0 # Means there is no model in production
        elif len(results_list)>1:
            print(log.error_messages["DATABASE_INCONSISTENCY"])
            return -1 # Means there is an error 
        else:
            return results_list

def get_production_model_id():
    ''' Getting the production model id
        returns -1 if error, 0 if no production model, else model id
    '''

    command = 'SELECT id FROM essai.production_models WHERE remove_date IS NULL;'
    results=get_production_model_informations(command)
    if (results==0) or (results==-1):
        #Pas de modèle exploitable en production
        return results
    else:
        return results[0][0]

def get_production_model_version_and_name():
    ''' Getting the production model version and name
        returns -1 if error, 0 if no production model, else query results
    '''
    
    command = 'SELECT id, version, name FROM essai.production_models WHERE remove_date IS NULL;'
    results=get_production_model_informations(command)
    if (results==0) or (results==-1):
        #Pas de modèle exploitable en production
        return results,"",""
    else:
        return results[0][0], results[0][1], results[0][2]

def get_production_model_scoring():
    ''' Getting the production model version and name
        returns (-1,"","") if error, (0,"","") if no production model, else query results
    '''
    
    command = 'SELECT id, scores, dataset_scoring_ids FROM essai.production_models WHERE remove_date IS NULL;'
    results=get_production_model_informations(command)
    if (results==0) or (results==-1):
        return results,"",""
    else:
        return results[0][0], results[0][1], results[0][2]

def remove_model_from_production(model_id_prm:int,remove_date_prm:str):
    ''' Removing the production model means indicating a remove date on current production model
        returns -1 if error, 0 else
    '''

    command = 'UPDATE essai.production_models SET remove_date="{remove_date}" WHERE id={model_id};'.format(
        model_id=model_id_prm,
        remove_date=remove_date_prm   
    )
    return set_elements_for_update(command)

def set_production_model_scoring(model_id_prm:int,scores_prm:str,dataset_scoring_ids_prm:str):
    ''' Setting new score for production model
        returns -1 if error, 0 else
    '''
    command = 'UPDATE essai.production_models SET scores="{scores}", dataset_scoring_ids="{dataset_scoring_ids}" WHERE id={model_id};'.format(
        model_id=model_id_prm,
        scores=scores_prm,   
        dataset_scoring_ids=dataset_scoring_ids_prm   
    )
    return set_elements_for_update(command)

############################# MODEL METADATA ACCESS #######################################

def get_models_name():
    ''' Getting models name
        returns -1 if error, 0 if no model available, else names
    '''

    command = 'SELECT name FROM essai.models;'
    results = get_elements_from_select(command)
    if (results==-1) or (results==0):
        return results
    else:
        return ([item[0] for item in results.fetchall()])

def add_model(library_prm,name_prm):
    ''' Adding new model
        return -1 if error, else last row id
    '''

    command = 'INSERT INTO essai.models (name, library) VALUES ("{name}","{library}");'.format(
        name=name_prm,
        library=library_prm
    )
    return set_elements_for_insert(command)

def delete_model(name_prm):
    ''' Deleting a model
        return -1 if error, else 0
    '''

    command = 'DELETE FROM essai.models WHERE name="{name}";'.format(
        name=name_prm,
    )
    return delete_elements(command)

############################# USER METADATA ACCESS #######################################

def get_password(username_prm):
    ''' Getting password for user
        returns -1 if error, 0 if user doesn't exist, else password
    '''

    command = 'SELECT password FROM essai.users WHERE username="{username}";'.format(
        username=username_prm
    )
    results = get_elements_from_select(command)
    if (results == -1):
        return results
    else:
        return results.fetchall()[0][0]

def get_users_username():
    ''' Getting users username
        returns -1 if error, 0 if no user declared, else usernames
    '''
    
    command = 'SELECT username FROM essai.users;'
    results = get_elements_from_select(command)
    if (results==-1):
        return results
    else:
        return ([item[0] for item in results.fetchall()])

def get_user_id(username_prm):
    ''' Getting users username
        returns -1 if error, 0 if user doesn't exist, else usernames
    '''

    command = 'SELECT id FROM essai.users WHERE username="{username}";'.format(
        username=username_prm
    )
    results = get_elements_from_select(command)
    if (results==-1):
        return results
    else:
        return results.fetchall()[0][0]

def add_user(username_prm,password_prm):
    ''' Adding user
        returns -1 if error, else last row id
    '''

    command = 'INSERT INTO essai.users (username, password) VALUES ("{username}","{password}");'.format(
        username=username_prm,
        password=password_prm
    )
    return set_elements_for_insert(command)

def delete_user(username_prm):
    ''' Deleting user
        returns -1 if error, else 0
    '''

    command = 'DELETE FROM essai.users WHERE username="{username}";'.format(
        username=username_prm,
    )
    return delete_elements(command)

####################### PREDICTION METADATA ACCESS ###########################################

def get_predictions_for_user(username_prm):
    ''' Getting predictions for a user
        returns -1 if error, 0 if no prediction, else predictions informations
    '''

    command = 'SELECT date, model_id, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result \
               FROM essai.predictions LEFT JOIN essai.users ON essai.predictions.user_id = essai.users.id \
               WHERE username="{username}";'.format(
        username=username_prm
    )
    return (get_elements_from_select(command))

def get_predictions_details_for_user(username_prm):
    ''' Getting detailed predictions, included production models metadata, for a user
        returns -1 if error, 0 if no prediction, else predictions informations
    '''

    command = 'SELECT {predictions_details_columns} \
               FROM essai.predictions LEFT JOIN essai.users ON essai.predictions.user_id = essai.users.id \
               LEFT JOIN essai.production_models ON essai.predictions.model_id = essai.production_models.id \
               WHERE username="{username}";'.format(
        username=username_prm,
        predictions_details_columns=get_predictions_details_columns()
    )
    return (get_elements_from_select(command))

def get_predictions_details_columns():
    ''' Used for mapping because of dysfonctionnement of Result.mappings() in sqlaclchemy library for joint tables
    '''
    return "predictions.id, predictions.date, model_id, production_models.date, version, name, rating, tag, bedroom, bathroom, pool, jacuzzi, nb_equip, result"

####################### FULL ACCESS ###########################################

def get_all_predictions():
    ''' Getting all predictions
        returns -1 if error, 0 if no prediction, else predictions metadata
    '''

    command = 'SELECT * FROM essai.predictions;'
    return (get_elements_from_select(command))

def get_all_models():
    ''' Getting all models
        returns -1 if error, 0 if no model, else models metadata
    '''

    command = 'SELECT * FROM essai.models;'
    return (get_elements_from_select(command).fetchall())

def get_all_production_models():
    ''' Getting all production models
        returns -1 if error, 0 if no production model, else production models metadata
    '''

    command = 'SELECT * FROM essai.production_models;'
    return (get_elements_from_select(command).fetchall())

def get_all_datasets():
    ''' Getting all datasets
        returns -1 if error, 0 if no dataset, else datasets metadata
    '''

    command = 'SELECT * FROM essai.datasets;'
    return (get_elements_from_select(command).fetchall())

def get_all_users(): 
    ''' Getting all users
        returns -1 if error, 0 if no user, else users metadata
    '''

    command = 'SELECT * FROM essai.users;'   
    return (get_elements_from_select(command).fetchall())
    


