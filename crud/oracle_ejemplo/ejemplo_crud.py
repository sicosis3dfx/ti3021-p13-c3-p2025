import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password= password, dsn= dsn)

def create_schema (query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada \n {query}")
    except oracledb.DatabaseError as error:
                print(f"No se pudo crear la tabla: {error}")

def create_table_personas():
    tables = [
            (
                "CREATE TABLE Evento ("
                "idevento INTEGER PRIMARY KEY,"
                "nombre VARCHAR(50) NOT NULL,"
                "fecha DATE,"
                "lugar VARCHAR(50)"
            ),
            (
                "CREATE TABLE Participante ("
                "idparticipante INTEGER PRIMARY KEY,"
                "nombre VARCHAR(50) NOT NULL,"
                "rut VARCHAR(10) UNIQUE,"
                "edad INTEGER,"
                "numeroinscripcion INTEGER"
            ),
            (
                "CREATE TABLE Atleta ("
                "idparticipante INTEGER PRIMARY KEY,"
                "disciplina TEXT,"
                "marca NUMERIC,"
                "FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)"
            ),
            (
                "CREATE TABLE Entrenador ("
                "identrenador INTEGER PRIMARY KEY,"
                "equipo VARCHAR(50)"
            ),
            (
                "CREATE TABLE Juez ("
                "idjuez INTEGER PRIMARY KEY,"
                "especialidad VARCHAR(50)"
            ),
            (
                "CREATE TABLE Inscripcion ("
                "idevento INTEGER,"
                "idparticipante INTEGER,"
                "PRIMARY KEY (idevento, idparticipante),"
                "FOREIGN KEY (idevento) REFERENCES Evento(idevento),"
                "FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)"
            ),
    ]
    for query in tables:
            create_schema(query)
from datetime import datetime
def create_evento(
    id,
    nombre,
    fecha,
    lugar
):
    sql = (
        "INSERT INTO Evento (idevento, nombre, fecha, lugar) "
        "VALUES (:id, :nombre, :fecha, :lugar)"
    )
    
    parametros = {
        "id": id,
        "nombre": nombre,
        "fecha": datetime.strptime(fecha, '%d-%m-%Y'),
        "lugar": lugar
        
    }   

def create_participante(
    id,
    nombre,
    rut,
    edad,
    numeroinscripcion
):
    sql = (
        "INSERT INTO Participante (idparticipante, nombre, rut, edad, numeroinscripcion) "
        "VALUES (:id, :nombre, :rut, :edad, :numeroinscripcion)"
    )   
    
    parametros = {
        "id": id,
        "nombre": nombre,
        "rut": rut,
        "edad": edad,
        "numeroinscripcion": numeroinscripcion
    }
    
def create_atleta(
    idparticipante,
    disciplina,
    marca
):
    sql = (
        "INSERT INTO Atleta (idparticipante, disciplina, marca) "
        "VALUES (:idparticipante, :disciplina, :marca)"
    )
    
    parametros = {
        "idparticipante": idparticipante,
        "disciplina": disciplina,
        "marca": marca
    }

    
def create_entrenador(
    identrenador,
    equipo
):
    sql = (
        "INSERT INTO Entrenador (identrenador, equipo) "
        "VALUES (:identrenador, :equipo)"
    )   

    parametros = {  
        "identrenador": identrenador,
        "equipo": equipo
    }

    
def create_juez(
    idjuez,
    especialidad
):
    sql = (
        "INSERT INTO Juez (idjuez, especialidad) "
        "VALUES (:idjuez, :especialidad)"
    )
    
    parametros = {
        "idjuez": idjuez,
        "especialidad": especialidad
    }
    