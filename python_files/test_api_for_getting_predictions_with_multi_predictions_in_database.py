import pytest
import log
import requests
import json

# Test of api.py
url_root = 'http://127.0.0.1:8000'

# Test API functions for getting predictions with several predictions in database

########################################
# API Test for getting all predictions #
########################################

def test_get_all_predictions_with_multi_predictions():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters None
    # return Three results with prediction features, result anf user_id who did the prediction

    endpoint="/predictions"
    r = requests.get(url=url_root+endpoint,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)

    assert ((json.loads(r.text))[0]['id']==1)
    assert ((json.loads(r.text))[0]['model_id']==2)
    assert ((json.loads(r.text))[0]['user_id']==3)
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['date'])==str)

    assert ((json.loads(r.text))[1]['id']==2)
    assert ((json.loads(r.text))[1]['model_id']==2)
    assert ((json.loads(r.text))[1]['user_id']==2)
    assert ((json.loads(r.text))[1]['rating']==4.6)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==3)
    assert ((json.loads(r.text))[1]['bathroom']==1)
    assert ((json.loads(r.text))[1]['pool']==0)
    assert ((json.loads(r.text))[1]['jacuzzi']==0)
    assert ((json.loads(r.text))[1]['nb_equip']==20)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['date'])==str)

    assert ((json.loads(r.text))[2]['id']==3)
    assert ((json.loads(r.text))[2]['model_id']==2)
    assert ((json.loads(r.text))[2]['user_id']==3)
    assert ((json.loads(r.text))[2]['rating']==4.8)
    assert ((json.loads(r.text))[2]['tag']=='')
    assert ((json.loads(r.text))[2]['bedroom']==3)
    assert ((json.loads(r.text))[2]['bathroom']==1)
    assert ((json.loads(r.text))[2]['pool']==0)
    assert ((json.loads(r.text))[2]['jacuzzi']==0)
    assert ((json.loads(r.text))[2]['nb_equip']==20)
    assert (type((json.loads(r.text))[2]['result'])==float)
    assert (type((json.loads(r.text))[2]['date'])==str)

###############################################
# API Test for getting predictions for a user #
###############################################

def test_get_predictions_for_a_user_with_multi_predictions():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return - Two results with prediction features and result

    endpoint="/predictions"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)

    assert ((json.loads(r.text))[0]['model_id']==2)
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['tag']=='')
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['date'])==str)

    assert ((json.loads(r.text))[1]['model_id']==2)
    assert ((json.loads(r.text))[1]['rating']==4.8)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==3)
    assert ((json.loads(r.text))[1]['bathroom']==1)
    assert ((json.loads(r.text))[1]['pool']==0)
    assert ((json.loads(r.text))[1]['jacuzzi']==0)
    assert ((json.loads(r.text))[1]['nb_equip']==20)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['date'])==str)

#######################################################
# API Test for getting predictions details for a user #
#######################################################

def test_get_predictions_details_for_a_user_with_multi_predictions():
    
    # Normal Test Case
    # header : username="admin", password="admin"
    # parameters 'user2'
    # return - Two results with details on production model used for prediction

    endpoint="/predictions_details"
    parameters="/user2"
    r = requests.get(url=url_root+endpoint+parameters,
                     headers={"username": "admin",
                              "password": "admin"}) 
    assert (r.status_code==200)
    assert ((json.loads(r.text))[0]['predictions.id']==1)
    assert ((json.loads(r.text))[0]['model_id']==2)
    assert ((json.loads(r.text))[0]['version']=='V1.1')
    assert ((json.loads(r.text))[0]['name']=='LinearRegression')
    assert ((json.loads(r.text))[0]['rating']==4.5)
    assert ((json.loads(r.text))[0]['bedroom']==3)
    assert ((json.loads(r.text))[0]['bathroom']==1)
    assert ((json.loads(r.text))[0]['pool']==0)
    assert ((json.loads(r.text))[0]['jacuzzi']==0)
    assert ((json.loads(r.text))[0]['nb_equip']==20)
    assert (type((json.loads(r.text))[0]['result'])==float)
    assert (type((json.loads(r.text))[0]['predictions.date'])==str)
    assert (type((json.loads(r.text))[0]['production_models.date'])==str)

    assert ((json.loads(r.text))[1]['predictions.id']==3)
    assert ((json.loads(r.text))[1]['model_id']==2)
    assert ((json.loads(r.text))[1]['version']=='V1.1')
    assert ((json.loads(r.text))[1]['name']=='LinearRegression')
    assert ((json.loads(r.text))[1]['rating']==4.8)
    assert ((json.loads(r.text))[1]['tag']=='')
    assert ((json.loads(r.text))[1]['bedroom']==3)
    assert ((json.loads(r.text))[1]['bathroom']==1)
    assert ((json.loads(r.text))[1]['pool']==0)
    assert ((json.loads(r.text))[1]['jacuzzi']==0)
    assert ((json.loads(r.text))[1]['nb_equip']==20)
    assert (type((json.loads(r.text))[1]['result'])==float)
    assert (type((json.loads(r.text))[1]['predictions.date'])==str)
    assert (type((json.loads(r.text))[1]['production_models.date'])==str)
