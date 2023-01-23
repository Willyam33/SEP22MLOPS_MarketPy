import requests
import numpy as np
import os
import datetime
from time import strftime
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from importlib import import_module

from joblib import dump
import json
import properties

def get_dataframe_from_file(filename,filepath=properties.raw_files_folder):
    ''' open file and get dataframe
    '''
    return pd.read_csv(filepath+filename)

def clean_data(df):

    #clean_data
    try:
        dfc = df.drop_duplicates()
        dfc = dfc.drop(['house_type','city_name','comments_nb'],axis=1)
        dfc = dfc[dfc['rating']!="Pas de note"]
        dfc = dfc[dfc['rating']!="Nouveau"]
        dfc = dfc[dfc['rating']!="Superhôte"]
        dfc = dfc[dfc['price_week']<8000]
        dfc = dfc[dfc['bathroom']!='Demi-salle']
        dfc = dfc[dfc['bathroom']!='5,5']
        dfc['rating'] = pd.to_numeric(dfc['rating'])
        dfc['bathroom'] = pd.to_numeric(dfc['bathroom'])
        dfc = dfc.dropna()
        dfc[['jacuzzi', 'pool']]=dfc[['jacuzzi', 'pool']].astype(int)
        return dfc
    except Exception as e:
        print(e)
        return {}

def prepare_features(df):
    num=df[['rating','bedroom','bathroom','nb_equip']]
    cat=df[['pool','tag','jacuzzi']]
    cat[['pool','jacuzzi']]=cat[['pool','jacuzzi']].astype(int).astype(str)
    for i,column in enumerate(cat.columns):
        if i==0:
            cat_dicho=pd.get_dummies(data=cat[column],prefix=column)
        else:
            cat_dicho=cat_dicho.join(pd.get_dummies(data=cat[column],prefix=column))
    features=pd.concat([num,cat_dicho],axis=1)
    print(features.columns)
    return features
    
def prepare_for_training(df):

    target=df['price_week']
    features=prepare_features(df)

    return features,target

def scaler_transformation(X):
    ''' Scaler transformation
    '''
    X[X.columns] = pd.DataFrame(StandardScaler().fit_transform(X),index=X.index)
    return X

def get_model_instance_from_module_and_name (module_name,model_name):
    module=import_module(module_name)
    model = getattr(module,model_name)
    return model()

def compute_model_score(model, X, y):
    model_instance = get_model_instance_from_module_and_name (model['library'],model['name'])

    cross_validation = cross_val_score(model_instance, X, y, cv=3, scoring='neg_mean_absolute_percentage_error')
    model_score = cross_validation.mean()
    return model_score

def predict(pipeline,X):
    return pipeline.predict(X)

def predict_and_score_pipeline(pipeline,X,y):
    # Predicting on test set
    y_pred=predict(pipeline,X)

    # Scoring
    score = mean_absolute_percentage_error(y_pred,y).mean()
    #print('SCORE = '+str(score))
    return score

def train_and_score_model(model, features, target):
    model_instance = get_model_instance_from_module_and_name (model['library'],model['name'])

    pipeline = Pipeline(steps = [('scaler', StandardScaler()),
                                 ('model', model_instance)])

    # Separating train set and test set
    X_train, X_test, y_train, y_test = train_test_split(features,target,train_size=0.7,random_state=42)
    
    # Training on train set
    pipeline.fit(X_train, y_train)

    score = predict_and_score_pipeline(pipeline,X_test,y_test)

    return pipeline, score

    

