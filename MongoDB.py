# IMPORTA CLIENTE NoSQL
from pymongo import MongoClient
from time import time

# CONECTA CON MARIA DB
def connectionDB():
    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.localhost
    connectionInstance = db['vacunas']

    return connectionInstance

# QUERY + COMMIT
def makeModification(data):
    
    try:
        connectionDB().insert_one(data)
        
    except:
        raise 
        
    
    return True

# QUERY + FETCH ALL
def makeQuery(filterBy = {}):
    try:
        tic = time()
        databaseList = connectionDB().find(filterBy)
        toc = time()
        print("NoSQL: " + str(toc - tic))
    except:
        raise 

    return databaseList

# QUERY + FETCH ALL
def truncate(filterBy = {}):
    try:
         databaseList = connectionDB().remove(filterBy)
    except:
        raise 

    return databaseList
