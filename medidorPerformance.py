import MariaDB
import MongoDB
from time import time
import random
from faker import Faker
fake = Faker()

def truncate_DBs():
 
    # RESETEA TODAS LAS TABLAS

    # SQL
    query = "DELETE FROM VACUNAS.VACUNA"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.PACIENTE"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.LABORATORIO"
    ok = MariaDB.makeModification(query)
    query = "DELETE FROM VACUNAS.CIUDAD"
    ok = MariaDB.makeModification(query)

    # NO SQL
    MongoDB.truncate()

    return ok

def insertLab():
 
    # SETEA LOS VALORES DE LA ENTIDAD
    paises = ['Argentina','Rusia','China','EE.UU','Etiopia','Mexico']
    pais = random.choice(paises)

    publico = random.choice(['T','F'])

    proximo_laboratorio = MariaDB.makeQuery("SELECT IFNULL(MAX(ID) + 1,1) AS CANT FROM VACUNAS.LABORATORIO;")[0]["CANT"]

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

    proxima_ciudad = MariaDB.makeQuery("SELECT IFNULL(MAX(ID) + 1,1) AS CANT FROM VACUNAS.CIUDAD;")[0]["CANT"]

    # SQL
    query = "INSERT INTO VACUNAS.CIUDAD(CANTIDADHABITANTES,NOMBRECIUDAD,SUPERFICIE) VALUES("
    query +=  str(habitantes) +","
    query += "'Ciudad_" + str(proxima_ciudad) +"',"
    query += str(superficie) +")"

    ok = MariaDB.makeModification(query)

    return ok

def crear_vacuna_paciente():

    # SETEA FAKE STATE PARA UNA VACUNA CON SU PACIENTE
    edad = random.randint(18, 99)
    sexo = random.choice(['H','M'])
    observaciones = fake.text()
    nombre = fake.name()
    fecha_aplicacion = fake.date_between(start_date='-90d', end_date='+60d')

    # PROXIMO ID - SQL
    # TRAE LABORATORIO Y CIUDAD RANDOM
    laboratorio_random = MariaDB.makeQuery("SELECT * FROM VACUNAS.LABORATORIO ORDER BY RAND() LIMIT 1;")[0]
    ciudad_random = MariaDB.makeQuery("SELECT * FROM VACUNAS.CIUDAD ORDER BY RAND() LIMIT 1;")[0]
    
    # SQL  
    # PACIENTE
    query = "INSERT INTO VACUNAS.PACIENTE(EDAD,NOMBREPACIENTE,SEXO) VALUES("
    query += "'" + str(edad) +"',"
    query += "'" + nombre +"',"
    query += "'" + sexo +"')"
    MariaDB.makeModification(query)

    proximo_paciente = MariaDB.makeQuery("SELECT MAX(ID) AS CANT FROM VACUNAS.PACIENTE;")[0]["CANT"]
    print(proximo_paciente)

    # VACUNA
    query = "INSERT INTO VACUNAS.VACUNA(FECHAAPLICACION,OBSERVACIONES,IDPACIENTE,IDLABORATORIO,IDCIUDAD) VALUES("
    query += "'" + str(fecha_aplicacion) +"',"
    query += "'" + observaciones +"',"
    query +=  str(proximo_paciente) +","
    query +=  str(laboratorio_random["ID"]) +","
    query +=  str(ciudad_random["ID"]) +")"
    ok = MariaDB.makeModification(query)

    # NoSQL 
    vacuna_paciente = { 
            "fechaAplicacion": str(fecha_aplicacion),
            "observaciones": observaciones,
            "paciente": { "nombre": nombre, "edad": edad, "sexo": sexo },
            "ciudad": { "nombre":  ciudad_random["NOMBRECIUDAD"], "cantidadHabitantes":  ciudad_random["CANTIDADHABITANTES"], "superficie": ciudad_random["SUPERFICIE"]},
            "laboratorio": { "nombre": laboratorio_random["NOMBRELABORATORIO"], "pais": laboratorio_random["PAIS"], "publico": laboratorio_random["PUBLICO"]}
            }
    MongoDB.makeModification(vacuna_paciente)
    
    return ok

def timedQuery():
    # cursor = MongoDB.makeQuery()
    # for document in cursor:
    #     print('-----------')
    #     print(document)
    return True

def case_1():
    # Reportar las ciudades y cantidad pacientes vacunados por cada una.
    return True

for x in range(10000):
    crear_vacuna_paciente()

# random_query = MariaDB.makeQuery("SELECT * FROM VACUNAS.VACUNA INNER JOIN VACUNAS.PACIENTE;")
# laboratorio_random = MariaDB.makeQuery("SELECT * FROM VACUNAS.CIUDAD ORDER BY RAND() LIMIT 1;")[0]
# print(laboratorio_random)
# truncate_DBs()
cursor = MongoDB.makeQuery()
for document in cursor:
    print('-----------')
    print(document)
