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
                "especialidad (50)"
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
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    print("Tabla 'personas' creada.")
        except oracledb.DatabaseError as error:
                print(f"No se pudo crear la tabla: {error}")