from sqlalchemy.engine import create_engine
import datetime
import log
import os
import sys

mysql_url = '172.17.0.2' 
mysql_user = 'root'
mysql_password = sys.argv[1]  
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
        connection.execute('ALTER USER root@localhost IDENTIFIED BY essai')
except log as e:
    print("Modification de mot de passe root en ERREUR")
    print(e)    
