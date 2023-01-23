import pytest
import log
import requests
import json
from test_functions import alter_table, un_alter_table

# Test of api.py
url_root = 'http://127.0.0.1:8000'

# Test API functions for getting predictions with several predictions in database

######################################
# API Test for realizing predictions #
######################################

def test_predict_ok():
    
    # Normal Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return - The prediction (float value)

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

def test_predict_one_element_lack():
    
    # Parameter Error Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format - minus one information
    # return - The prediction (float value)

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==422)

def test_predict_wrong_type_for_parameter():
    
    # Normal Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format - minus one information
    # return - The prediction (float value)

    input = {
        "rating": "toto",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==422)

def test_predict_user_unknown():
    
    # Normal Test Case
    # header : username="user3", password="pass3"
    # body parameters - Input format
    # return - 401 - "user3 n existe pas"

    input = {
        "rating": "4.5",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user3",
                               "password": "pass3"}) 
    assert ((json.loads(r.text))['detail']=='L utilisateur n existe pas !')
    assert (r.status_code==401)

def test_predict_bad_password():
    
    # Normal Test Case
    # header : username="user2", password="pass_incorrect"
    # body parameters - Input format
    # return HTTPCode 401,"Le mot de passe est incorrect !"

    input = {
        "rating": "4.5",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi": "0",
        "nb_equip": "20" 
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass_incorrect"}) 
    assert ((json.loads(r.text))['detail']=='Le mot de passe est incorrect !')
    assert (r.status_code==401)
 
def test_predict_corrupted_production_models_table():
    
    # Normal Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return HTTPCode 500,"Erreur d accès à la base de données"

    alter_table('production_models')

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert ((json.loads(r.text))['detail']=='Erreur d accès à la base de données')
    assert (r.status_code==500)

    un_alter_table('production_models')

def test_predict_corrupted_predictions_table():
    
    # Normal Test Case
    # header : username="user2", password="pass2"
    # body parameters - Input format
    # return prediction in spite of corruption table

    alter_table('predictions')

    input = {
        "rating": "4.50",
        "tag": "",
        "bedroom": "3",
        "bathroom": "1",
        "pool": "0",
        "jacuzzi" : "0",
        "nb_equip" : "20"
    }

    endpoint="/predict"
    r = requests.post(url=url_root+endpoint,
                      json=input,
                      headers={"Content-Type": "application/json",
                               "username": "user2",
                               "password": "pass2"}) 
    assert (r.status_code==200)
    value=float(r.text)
    assert(type(value)==float)
    assert(value>0)

    un_alter_table('predictions')