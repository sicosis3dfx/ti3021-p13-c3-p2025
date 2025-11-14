import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password= password, dsn= dsn)


def create_table_personas():
    query = (
        "CREATE TABLE personas ("
        "rut VARCHAR2(50) PRIMARY KEY,"
        "nombres VARCHAR2(200),"
        "apellidos VARCHAR2(200),"
        "fecha_nacimiento DATE,"
        "cod_area VARCHAR2(20),"
        "numero_telefono VARCHAR2(50)"
        ")"
    )

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
             cur.execute(query)
            print("Tabla 'personas' creada.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo crear la tabla: {error}")

        [
            -- 1. Tabla Evento
            CREATE TABLE Evento (
                idevento INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                fecha DATE,
                lugar TEXT
            );

            -- 2. Tabla Participante
            CREATE TABLE Participante (
                idparticipante INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                rut VARCHAR(10) UNIQUE,
                edad INTEGER,
                numeroinscripcion INTEGER
            );

            -- 3. Tabla Atleta (Herencia de Participante)
            CREATE TABLE Atleta (
                idparticipante INTEGER PRIMARY KEY,
                disciplina TEXT,
                marca NUMERIC,
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            );

            -- 4. Tabla Entrenador
            CREATE TABLE Entrenador (
                identrenador INTEGER PRIMARY KEY,
                equipo TEXT
            );

            -- 5. Tabla Juez
            CREATE TABLE Juez (
                idjuez INTEGER PRIMARY KEY,
                especialidad TEXT
            );

            -- Tabla de Relación (Inscripción/Participación)
            CREATE TABLE Inscripcion (
                idevento INTEGER,
                idparticipante INTEGER,
                PRIMARY KEY (idevento, idparticipante),
                FOREIGN KEY (idevento) REFERENCES Evento(idevento),
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            );
            ]