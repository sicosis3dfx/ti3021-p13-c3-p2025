# Proyecto: EcoTech Solutions - Backend y Lógica
# Módulo principal con clases para BD, Autenticación y Finanzas
import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

# Cargamos las credenciales desde el archivo .env para seguridad
load_dotenv()

class Database:
    def __init__(self):
        # Recuperamos las credenciales de las variables de entorno
        self.username = os.getenv("ORACLE_USER")
        self.dsn = os.getenv("ORACLE_DSN")
        self.password = os.getenv("ORACLE_PASSWORD")

    def get_connection(self):
        # Establecemos la conexión con Oracle Cloud
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)

    def create_all_tables(self):
        # Definimos las tablas necesarias para el sistema
        tables = [
            (
            "CREATE TABLE USERS(id INTEGER PRIMARY KEY, "
            "username VARCHAR(32) UNIQUE, "
            "password VARCHAR(128))"
            ),
            
            (
            "CREATE TABLE HISTORIAL_FINANCIERO (id INTEGER PRIMARY KEY, "
            "indicador VARCHAR2(20), "
            "valor NUMBER(10, 2), "
            "fecha_dato VARCHAR2(20), "
            "fecha_consulta DATE DEFAULT SYSDATE, "
            "usuario VARCHAR2(32), "
            "origen VARCHAR2(100))"
            )
        ]
        # Iteramos y ejecutamos la creación
        for table in tables:
            self.query(table)

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    # Si es un SELECT, devolvemos los datos en una lista
                    if sql.strip().upper().startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
                return True
        except oracledb.DatabaseError as error:
            # Si el error es ORA-00955 significa que la tabla ya existe, así que lo ignoramos
            if "ORA-00955" in str(error): return False
            print(f"Error en BD: {error}")
            return False

    def get_next_id(self, table_name):
        # Simulación de autoincrementable: buscamos el ID más alto y le sumamos 1
        try:
            res = self.query(f"SELECT NVL(MAX(id), 0) + 1 FROM {table_name}") 
            return res[0][0] if res else 1
        except:
            return 1

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        # Verificamos credenciales
        password = password.encode("UTF-8")
        resultado = db.query("SELECT * FROM USERS WHERE username = :username", {"username": username})

        if not resultado:
            return {"message": "Usuario no encontrado", "success": False}

        # Obtenemos el hash de la BD y comparamos
        hashed_password = bytes.fromhex(resultado[0][2])
        
        if bcrypt.checkpw(password, hashed_password):
            return {"message": "Inicio de sesión correcto", "success": True}
        else:
            return {"message": "Contraseña incorrecta", "success": False}

    @staticmethod
    def register(db: Database, username: str, password: str):
        try:
            if not username or not password:
                return {"message": "Faltan datos por ingresar", "success": False}
            
            # Obtenemos el siguiente ID disponible
            real_id = db.get_next_id("USERS")
            password = password.encode("UTF-8")
            
            # Encriptamos la contraseña con bcrypt antes de guardar
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt(12)).hex() 
            
            db.query("INSERT INTO USERS(id,username,password) VALUES (:id, :username, :password)", 
                     {"id": real_id, "username": username, "password": hash_password})
            return {"message": "Usuario registrado OK", "success": True}
        except Exception as error:
            return {"message": f"Error: {error}", "success": False}

class Finance:
    def __init__(self, db: Database = None, usuario_actual: str = None):
        # API pública que usaremos para los datos
        self.base_url = "https://mindicador.cl/api"
        self.db = db
        self.usuario_actual = usuario_actual

    def get_indicator(self, indicator: str, fecha_especifica: str = None) -> float:
        try:
            # Configuramos la URL dependiendo si piden fecha específica o el valor de hoy
            if fecha_especifica:
                url_consulta = f"{self.base_url}/{indicator}/{fecha_especifica}"
            else:
                now = datetime.datetime.now()
                fecha_hoy = f"{now.day}-{now.month}-{now.year}"
                url_consulta = f"{self.base_url}/{indicator}/{fecha_hoy}"
            
            # Hacemos la petición a la API
            respuesta = requests.get(url_consulta).json()
            
            # Fallback: Si pedimos hoy y la API no tiene dato (ej: fin de semana), pedimos el general
            if not respuesta.get("serie") and not fecha_especifica:
                url_consulta = f"{self.base_url}/{indicator}" 
                respuesta = requests.get(url_consulta).json()

            if not respuesta.get("serie"):
                return -1 # Retorno de error controlado

            valor = respuesta["serie"][0]["valor"]
            fecha_dato = respuesta["serie"][0]["fecha"][:10]

            # Si tenemos conexión y usuario, guardamos el registro en el historial
            if self.db and self.usuario_actual:
                self.guardar_historial(indicator, valor, fecha_dato, url_consulta)

            return valor
        except Exception as error:
            print(f"Error consultando API: {error}")
            return -1

    def get_yearly_data(self, indicator: str, year: str):
        # Consulta para traer los datos de todo un año (para análisis)
        try:
            url_especifica = f"{self.base_url}/{indicator}/{year}"
            respuesta = requests.get(url_especifica).json()
            
            if self.db and self.usuario_actual and respuesta.get('serie'):
                # Dejamos registro en el historial de que se hizo esta consulta masiva
                self.guardar_historial(indicator, 0, f"{year}-01-01", url_especifica)

            return respuesta.get('serie', [])
        except Exception as error:
            print(f"Error en consulta anual: {error}")
            return []

    def guardar_historial(self, indicator, valor, fecha_dato, origen_personalizado):
        # Método auxiliar para insertar en la tabla de historial
        try:
            next_id = self.db.get_next_id("HISTORIAL_FINANCIERO")
            sql = """INSERT INTO HISTORIAL_FINANCIERO (id, indicador, valor, fecha_dato, usuario, origen) 
                     VALUES (:id, :ind, :val, :fec, :usu, :ori)"""
            
            params = {
                "id": next_id, 
                "ind": indicator, 
                "val": valor, 
                "fec": fecha_dato, 
                "usu": self.usuario_actual, 
                "ori": origen_personalizado
            }
            self.db.query(sql, params)
        except Exception as e:
            print(f"No se pudo guardar historial: {e}")

    def get_history(self):
        # Recupera las últimas consultas del usuario actual
        if not self.db or not self.usuario_actual: return []
        sql = "SELECT indicador, valor, fecha_dato, fecha_consulta, origen FROM HISTORIAL_FINANCIERO WHERE usuario = :u ORDER BY id DESC"
        return self.db.query(sql, {"u": self.usuario_actual})