# IMPORTA CLIENTE SQL
import pymysql
from time import time

# CONECTA CON MARIA DB
def connectionDB():

    databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
    databaseUserName            = "root"       # User name of the database server
    databaseUserPassword        = "root"           # Password for the database user

    charSet                     = "utf8mb4"     # Character set
    cusrorType                  = pymysql.cursors.DictCursor

    connectionInstance   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,
                                            charset=charSet,cursorclass=cusrorType)
    
    return connectionInstance

# QUERY + COMMIT
def makeModification(query):
    
    try:
        connection = connectionDB()
        cursorInsatnce        = connection.cursor()    

        # SQL QUERY TIME
        tic = time()
        sqlStatement  = query 
        toc = time()
        print(toc - tic)

        cursorInsatnce.execute(sqlStatement)
        cursorInsatnce.execute("COMMIT")
    except:
        raise 
        
    finally:
        connection.close()
    
    return True

# QUERY + FETCH ALL
def makeQuery(query):
    
    try:
        connection = connectionDB()
        cursorInsatnce  = connection.cursor() 

        # SQL QUERY TIME   
        tic = time()
        cursorInsatnce.execute(query)
        toc = time()
        print(toc - tic)

        #RESULTADOS FUERA DEL TIEMPO 
        databaseList = cursorInsatnce.fetchall()

    except:
        raise 

    finally:
        connection.close()
    
    return databaseList