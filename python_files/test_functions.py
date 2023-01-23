import sqlalchemy
from sqlalchemy.engine import create_engine

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

# Simulate database alteration for users table
def alter_table(table_name):
    try:
        with mysql_engine.connect() as connection:
            connection.execute('ALTER TABLE essai.'+table_name+' RENAME TO essai.'+table_name+'_bidon;')
    except:
        print("Erreur dans le protocole de test : Echec de l'alteration de table")

def un_alter_table(table_name):
    try:
        with mysql_engine.connect() as connection:
            connection.execute('ALTER TABLE essai.'+table_name+'_bidon RENAME TO essai.'+table_name+';')
    except:
        print("Erreur dans le protocole de test : Echec de l'alteration de table")

