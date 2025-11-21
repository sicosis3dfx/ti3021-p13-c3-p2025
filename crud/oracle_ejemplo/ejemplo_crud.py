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
                "CREATE TABLE Eventos ("
                "idevento INTEGER PRIMARY KEY,"
                "nombre VARCHAR(50) NOT NULL,"
                "fecha DATE,"
                "lugar VARCHAR(50)"
            ),
            (
                "CREATE TABLE Participantes ("
                "idparticipante INTEGER PRIMARY KEY,"
                "nombre VARCHAR(50) NOT NULL,"
                "rut VARCHAR(10) UNIQUE,"
                "edad INTEGER,"
                "numeroinscripcion INTEGER"
            ),
            (
                "CREATE TABLE Atletas ("
                "idparticipante INTEGER PRIMARY KEY,"
                "disciplina TEXT,"
                "marca FLOAT,"
                "FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)"
            ),
            (
                "CREATE TABLE Entrenadores ("
                "identrenador INTEGER PRIMARY KEY,"
                "equipo VARCHAR(50)"
            ),
            (
                "CREATE TABLE Jueces ("
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
def create_eventos(
    id: int,
    nombre: str,
    fecha: str,
    lugar: str,
):
    sql = (
        "INSERT INTO Eventos (idevento, nombre, fecha, lugar) "
        "VALUES (:id, :nombre, :fecha, :lugar)" 
    )
    
    parametros = {
        "id": id,
        "nombre": nombre,
        "fecha": datetime.strptime(fecha, '%d-%m-%Y'),
        "lugar": lugar
        
    }   
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

def create_participantes(
    id: int,
    nombre: str,
    rut: str,
    edad: int,
    numeroinscripcion: int,
):
    sql = (
        "INSERT INTO Participantes (idparticipante, nombre, rut, edad, numeroinscripcion) "
        "VALUES (:id, :nombre, :rut, :edad, :numeroinscripcion)"
    )   
    
    parametros = {
        "id": id,
        "nombre": nombre,
        "rut": rut,
        "edad": edad,
        "numeroinscripcion": numeroinscripcion
    }
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

def create_atletas(
    idparticipante: int,
    disciplina: str,
    marca: float,
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

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")
    
def create_entrenadores(
    identrenador: int,
    equipo: str,
):
    sql = (
        "INSERT INTO Entrenadores (identrenador, equipo) "
        "VALUES (:identrenador, :equipo)"
    )   

    parametros = {  
        "identrenador": identrenador,
        "equipo": equipo
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

def create_jueces(
    idjuez: int,
    especialidad: str,
):
    sql = (
        "INSERT INTO Jueces (idjuez, especialidad) "
        "VALUES (:idjuez, :especialidad)"
    )
    
    parametros = {
        "idjuez": idjuez,
        "especialidad": especialidad
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo insertar el dato \n {error} \n {sql} \n {parametros}")

def read_eventos():
    sql = (
    "SELECT * FROM Eventos"
    )

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultado = cursor.execute(sql)
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
                print(f"No se pudo leer los datos \n {error} \n {sql}")

def read_participantes():
    sql = (
    "SELECT * FROM Participantes"
    )

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultado = cursor.execute(sql)
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
                print(f"No se pudo leer los datos \n {error} \n {sql}")

def read_participante_by_id(id: int):
    sql = (
    "SELECT * FROM Participantes WHERE idparticipante = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultado = cursor.execute(sql, parametros)
                if len(resultado) == 0:
                    return print(f"No hay registros con el ID {id}")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
                print(f"No se pudo leer el dato \n {error} \n {sql} \n {parametros}")

def read_atletas():
    sql = (
    "SELECT * FROM Atletas"
    )
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultado = cursor.execute(sql)
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
                print(f"No se pudo leer los datos \n {error} \n {sql}")

def read_entrenadores():
    pass

def read_jueces():
    pass