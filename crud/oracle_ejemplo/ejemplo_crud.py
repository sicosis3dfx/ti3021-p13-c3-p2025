import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
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

def create_all_tables():
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
    sql = (
    "SELECT * FROM Entrenadores"
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

def read_jueces():
    sql = (
    "SELECT * FROM Jueces"
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

    # UPDATE - Actualización de datos
def update_evento(
            id: int,
            nombre: Optional[str] = None,
            fecha: Optional[str] = None,
            lugar: Optional[str] = None
    ):
         modificaciones = []
         parametros = {"id": id}

         if nombre is not None:
             modificaciones.append("nombre = :nombre")
             parametros["nombre"] = nombre
         if fecha is not None:
             modificaciones.append("fecha = :fecha")
             parametros["fecha"] = datetime.strptime(fecha, '%d-%m-%Y')
         if lugar is not None:
             modificaciones.append("lugar = :lugar")
             parametros["lugar"] = lugar
         if not modificaciones:
             print("No hay campos para actualizar.")
             return
    
def update_participante(
            id: int,
            nombre: Optional[str] = None,
            rut: Optional[str] = None,
            edad: Optional[int] = None,
            numeroinscripcion: Optional[int] = None
    ):
         modificaciones = []
         parametros = {"id": id}

         if nombre is not None:
             modificaciones.append("nombre = :nombre")
             parametros["nombre"] = nombre
         if rut is not None:
             modificaciones.append("rut = :rut")
             parametros["rut"] = rut
         if edad is not None:
             modificaciones.append("edad = :edad")
             parametros["edad"] = edad
         if numeroinscripcion is not None:
             modificaciones.append("numeroinscripcion = :numeroinscripcion")
             parametros["numeroinscripcion"] = numeroinscripcion
         if not modificaciones:
             print("No hay campos para actualizar.")
             return
         
def update_atleta(
            idparticipante: int,
            disciplina: Optional[str] = None,
            marca: Optional[float] = None
    ):
         modificaciones = []
         parametros = {"idparticipante": idparticipante}

         if disciplina is not None:
             modificaciones.append("disciplina = :disciplina")
             parametros["disciplina"] = disciplina
         if marca is not None:
             modificaciones.append("marca = :marca")
             parametros["marca"] = marca
         if not modificaciones:
             print("No hay campos para actualizar.")
             return
         
def update_entrenador(
            identrenador: int,
            equipo: Optional[str] = None
    ):
         modificaciones = []
         parametros = {"identrenador": identrenador}

         if equipo is not None:
             modificaciones.append("equipo = :equipo")
             parametros["equipo"] = equipo
         if not modificaciones:
             print("No hay campos para actualizar.")
             return
    
def update_juez(
            idjuez: int,
            especialidad: Optional[str] = None
    ):
         modificaciones = []
         parametros = {"idjuez": idjuez}

         if especialidad is not None:
             modificaciones.append("especialidad = :especialidad")
             parametros["especialidad"] = especialidad
         if not modificaciones:
             print("No hay campos para actualizar.")
             return
         
         sql = f"UPDATE Eventos SET {', '.join(modificaciones)} WHERE idevento = :id"

         with get_connection() as conn:
             with conn.cursor() as cur:
                cur.execute(sql, parametros)
             conn.commit()
             print(f"Dato con ID {id} actualizado exitosamente.")
                
    # DELETE - Eliminación de datos

def delete_evento(id: int):
    sql = (
         "DELETE FROM Eventos WHERE idevento = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {id} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dato \n {error} \n {sql} \n {parametros}")

def delete_participante(id: int):
    sql = (
        "DELETE FROM Participantes WHERE idparticipante = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {id} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dato \n {error} \n {sql} \n {parametros}")   

def delete_atleta(idparticipante: int):
    sql = (
        "DELETE FROM Atletas WHERE idparticipante = :idparticipante"
    )
    parametros = {"idparticipante": idparticipante}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {idparticipante} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dato \n {error} \n {sql} \n {parametros}")

def delete_entrenador(identrenador: int):
    sql = (
         "DELETE FROM Entrenadores WHERE identrenador = :identrenador"
    )
    parametros = {"identrenador": identrenador}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {identrenador} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dato \n {error} \n {sql} \n {parametros}")

def delete_juez(idjuez: int):
    sql = (
         "DELETE FROM Jueces WHERE idjuez = :idjuez"
    )
    parametros = {"idjuez": idjuez}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {idjuez} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
                print(f"No se pudo eliminar el dato \n {error} \n {sql} \n {parametros}")

def main():
    pass

if __name__ == "__main__":
    main()
