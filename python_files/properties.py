from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np

raw_files_folder = '/home/ubuntu/raw_files/' #triggered directory for raw files
clean_data_folder = '/home/ubuntu/clean_data' #directory for cleaned data files
model_folder = '/home/ubuntu/model/' #directory for operational models
model_file = 'model.pckl'

model_list = [ 
    {
        'nature': "Régression linéaire",
        'object': LinearRegression()
    },
    {
        'nature': "Arbre de décision",
        'object': DecisionTreeRegressor()
    },
    {
        'nature': "Forêt aléatoire",
        'object': RandomForestRegressor()
    },
    {
        'nature': "Perceptron Multi-couche",
        'object': MLPRegressor()
    }
]

