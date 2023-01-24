from sqlalchemy.engine import create_engine
import datetime
import log
import os
#from dotenv import load_dotenv

#pipload_dotenv()
# By convention, -1 is used for error return code
print(os.environ.get('GITHUB_ACTOR'))
# creating a connection to the database
# mysql_url = 'my_mysql' 
mysql_url = '172.17.0.2' 
mysql_user = 'root'
mysql_password = 'essai'
#mysql_password = os.environ.get('DB_PASSWORD')  
database_name = ''

# recreating the URL connection
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)
print("TATA")
print(mysql_user)
print(mysql_password)
print(os.environ.get('DB_PASSWORD'))
print(mysql_url)
print("TATA")

print("TOTO")
print(connection_url)
print("TOTO")
# creating the connection
mysql_engine = create_engine(connection_url)

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
