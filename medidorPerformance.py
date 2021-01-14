import MariaDB
import MongoDB
from time import time
import random
from faker import Faker
fake = Faker()

def delete():
 
    # RESETEA TODAS LAS TABLAS

    # SQL
    query = "DELETE FROM VACUNAS.LABORATORIO"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.CIUDAD"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.PACIENTE"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.VACUNA"
    ok = MariaDB.makeModification(query)

    return ok

def insertLab():
 
    # SETEA LOS VALORES DE LA ENTIDAD
    paises = ['Argentina','Rusia','China','EE.UU','Etiopia','Mexico']
    pais = random.choice(paises)

    publico = random.choice(['T','F'])

    proximo_laboratorio = MariaDB.makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.LABORATORIO;")[0]["CANT"]

    # SQL
    query = "INSERT INTO VACUNAS.LABORATORIO(PAIS,NOMBRELABORATORIO,PUBLICO) VALUES("
    query += "'" + pais +"',"
    query += "'Laboratorio_" + str(proximo_laboratorio) +"',"
    query += "'" + publico +"')"

    ok = MariaDB.makeModification(query)

    return ok

def insertCiudad():

    superficie = random.randint(10, 250)
    habitantes = random.randint(600, 5000000)

    proxima_ciudad = MariaDB.makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.CIUDAD;")[0]["CANT"]

    # SQL
    query = "INSERT INTO VACUNAS.CIUDAD(CANTIDADHABITANTES,NOMBRECIUDAD,SUPERFICIE) VALUES("
    query +=  str(habitantes) +","
    query += "'Ciudad_" + str(proxima_ciudad) +"',"
    query += str(superficie) +")"

    ok = MariaDB.makeModification(query)

    return ok

def insertVacunaPaciente():

    edad = random.randint(18, 99)
    sexo = random.choice(['H','M'])
    texto = fake.text()
    nombre = fake.name()
    fecha_aplicacion = fake.date_between(start_date='-90d', end_date='+60d')

    proximo_paciente = MariaDB.makeQuery("SELECT count(*) + 1 AS CANT FROM VACUNAS.PACIENTE;")[0]["CANT"]
    laboratorio_random = MariaDB.makeQuery("SELECT * FROM VACUNAS.LABORATORIO ORDER BY RAND() LIMIT 1;")[0]
    ciudad_random = MariaDB.makeQuery("SELECT * FROM VACUNAS.CIUDAD ORDER BY RAND() LIMIT 1;")[0]
    
    # SQL  
    # PACIENTE
    query = "INSERT INTO VACUNAS.PACIENTE(EDAD,NOMBREPACIENTE,SEXO) VALUES("
    query += "'" + str(edad) +"',"
    query += "'" + nombre +"',"
    query += "'" + sexo +"')"
    MariaDB.makeModification(query)

    # VACUNA
    query = "INSERT INTO VACUNAS.VACUNA(FECHAAPLICACION,OBSERVACIONES,IDPACIENTE,IDLABORATORIO,IDCIUDAD) VALUES("
    query += "'" + str(fecha_aplicacion) +"',"
    query += "'" + texto +"',"
    query +=  str(proximo_paciente) +","
    query +=  str(laboratorio_random["IDLaboratorio"]) +","
    query +=  str(ciudad_random["IDCiudad"]) +")"
    ok = MariaDB.makeModification(query)

    # NoSQL 
    mydict = { "name": "John", "address": "Highway 37","sdasad": 20 }
    MongoDB.makeModification(mydict)
    
    return ok

def timedQuery():
    # cursor = MongoDB.makeQuery()
    # for document in cursor:
    #     print('-----------')
    #     print(document)
    return True

# for x in range(58):
#     insertVacunaPaciente()

# random_query = MariaDB.makeQuery("SELECT * FROM VACUNAS.VACUNA INNER JOIN VACUNAS.PACIENTE;")

