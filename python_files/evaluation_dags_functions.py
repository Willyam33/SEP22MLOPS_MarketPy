import requests
import numpy as np
import os
import datetime
from time import strftime
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.neural_network import MLPRegressor
from sklearn import preprocessing
from sklearn.pipeline import Pipeline

from joblib import load
import json
import data_manipulation
import database_functions
import properties
import log

def get_dataframe_from_file_and_clean_data(filename,filepath=properties.raw_files_folder):
    ''' opens file, get dataframe, clean data, prepare for training and scale
    '''
    #read csv
    df=data_manipulation.get_dataframe_from_file(filename,filepath)
    
    #clean data
    cleaned_df=data_manipulation.clean_data(df)
    
    #save dataset  metadata
    date = datetime.datetime.now().strftime("%d-%b-%Y-%H:%M:%S")
    if (cleaned_df.empty):
        print(log.warning_messages['INVALID_DATASET'])
        dataset_id=database_functions.save_new_dataset_metadata(filename,
                                                                date_prm=date,
                                                                invalid_prm=True)
        if dataset_id==-1:
            print(log.error_messages['UNABLE_TO_SAVE_DATASET_METADATA'])
            return -1
    else:
        dataset_id=database_functions.save_new_dataset_metadata(filename,
                                                                date_prm=date,
                                                                invalid_prm=False,
                                                                size_before_cleaning_prm=len(df),
                                                                size_after_cleaning_prm=len(cleaned_df))
        if dataset_id==-1:
            print(log.error_messages['UNABLE_TO_SAVE_DATASET_METADATA'])
            return -1

        #prepare for training
        features,target=data_manipulation.prepare_for_training(cleaned_df)
        #scale data
        features_scaled=data_manipulation.scaler_transformation(features)

    return dataset_id, features_scaled, target

def compute_model_score(model, features, target):
    '''
    '''
    return data_manipulation.compute_model_score(model, features, target)

def predict_and_score_on_production_pipeline(features, target, dataset_id):
    '''
    '''
    # Getting production model scorings
    production_model_id, production_model_scores, production_model_dataset_scoring_ids = \
        database_functions.get_production_model_scoring()

    if (production_model_id==-1):
        print(log.error_messages['UNABLE_TO_MANAGE_PRODUCTION_MODELS'])
        return -1
    elif production_model_id==0:
        print(log.warning_messages['NO_MODEL_IN_PRODUCTION'])
        return 0
    else:
        # Getting production pipeline 
        try:
            pipeline=load(properties.model_folder+properties.model_file)
        except:
            print(log.error_messages['UNABLE_TO_LOAD_PRODUCTION_PIPELINE_FILE'])
            return -1

        # Predicting and scoring pipeline
        score=data_manipulation.predict_and_score_pipeline(pipeline,features,target)
    
        # Saving scoring in the database
        status=database_functions.set_production_model_scoring(
            model_id_prm=production_model_id,
            scores_prm=production_model_scores+','+format(score, ".2f"), 
            dataset_scoring_ids_prm=production_model_dataset_scoring_ids+','+str(dataset_id)
        )
        if status==-1:
            print(log.error_messages['UNABLE_TO_SAVE_PRODUCTION_SCORING_ON_NEW_DATASET'])
        else:
            print(log.success_messages['PRODUCTION_SCORING_UPDATED']) 
        return 0

