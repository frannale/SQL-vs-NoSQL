# import the mysql client for python
import pymysql
# import mongoDB
from pymongo import MongoClient
client = MongoClient(‘<<MongoDB Connection String>>’)
from time import time
import random
from faker import Faker
fake = Faker()

def connectionDB():
    # Create a connection object
    databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
    databaseUserName            = "root"       # User name of the database server
    databaseUserPassword        = "root"           # Password for the database user

    charSet                     = "utf8mb4"     # Character set
    cusrorType                  = pymysql.cursors.DictCursor

    connectionInstance   = pymysql.connect(host=databaseServerIP, user=databaseUserName, password=databaseUserPassword,
                                            charset=charSet,cursorclass=cusrorType)
    
    return connectionInstance

def makeModification(query):
    try:
        # Create a cursor object
        connection = connectionDB()
        cursorInsatnce        = connection.cursor()    

        tic = time()
        # SQL Statement to create a database
        sqlStatement  = query 
        toc = time()
        print(toc - tic)

        # Execute the create database SQL statment through the cursor instance
        cursorInsatnce.execute(sqlStatement)
        cursorInsatnce.execute("COMMIT")
    except:
        raise 
        
    finally:
        connection.close()
    
    return True

def makeQuery(query):
    try:
        # Create a cursor object
        connection = connectionDB()
        cursorInsatnce  = connection.cursor() 

        # Execute the sqlQuery    
        tic = time()
        cursorInsatnce.execute(query)
        toc = time()
        print(toc - tic)

        #Fetch all the rows
        databaseList = cursorInsatnce.fetchall()

    except:
        raise 

    finally:
        connection.close()
    
    return databaseList

def insertLab():
 
    # SETEA LOS VALORES DE LA ENTIDAD
    paises = ['Argentina','Rusia','China','EE.UU','Etiopia','Mexico']
    pais = random.choice(paises)

    publico = random.choice(['T','F'])

    proximo_laboratorio = makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.LABORATORIO;")[0]["CANT"]

    # SQL
    query = "INSERT INTO VACUNAS.LABORATORIO(PAIS,NOMBRELABORATORIO,PUBLICO) VALUES("
    query += "'" + pais +"',"
    query += "'Laboratorio_" + str(proximo_laboratorio) +"',"
    query += "'" + publico +"')"

    ok = makeModification(query)

    return ok

def insertCiudad():

    superficie = random.randint(10, 250)
    habitantes = random.randint(600, 5000000)

    proxima_ciudad = makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.CIUDAD;")[0]["CANT"]

    # SQL
    query = "INSERT INTO VACUNAS.CIUDAD(CANTIDADHABITANTES,NOMBRECIUDAD,SUPERFICIE) VALUES("
    query +=  str(habitantes) +","
    query += "'Ciudad_" + str(proxima_ciudad) +"',"
    query += str(superficie) +")"

    ok = makeModification(query)

    return ok

def insertVacunaPaciente():

    edad = random.randint(18, 99)

    sexo = random.choice(['H','M'])

    proximo_paciente = makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.PACIENTE;")[0]["CANT"]
    laboratorio_random = makeQuery("SELECT * FROM VACUNAS.LABORATORIO ORDER BY RAND() LIMIT 1;")[0]
    ciudad_random = makeQuery("SELECT * FROM VACUNAS.CIUDAD ORDER BY RAND() LIMIT 1;")[0]

    fecha_aplicacion = fake.date_between(start_date='-90d', end_date='+60d')

    
    # PACIENTE
    query = "INSERT INTO VACUNAS.PACIENTE(EDAD,NOMBREPACIENTE,SEXO) VALUES("
    query += "'" + str(edad) +"',"
    query += "'" + fake.name() +"',"
    query += "'" + sexo +"')"

    makeModification(query)

    # VACUNA
    query = "INSERT INTO VACUNAS.VACUNA(FECHAAPLICACION,OBSERVACIONES,IDPACIENTE,IDLABORATORIO,IDCIUDAD) VALUES("
    query += "'" + str(fecha_aplicacion) +"',"
    query += "'" + fake.text() +"',"
    query +=  str(proximo_paciente) +","
    query +=  str(laboratorio_random["IDLaboratorio"]) +","
    query +=  str(ciudad_random["IDCiudad"]) +")"

    ok = makeModification(query)
    
    return ok

# for x in range(58):
#     insertVacunaPaciente()

ciudad_random = makeQuery("SELECT * FROM VACUNAS.VACUNA INNER JOIN VACUNAS.PACIENTE;")