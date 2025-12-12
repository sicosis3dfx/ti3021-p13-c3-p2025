# Conectarnos a la base de datos
import oracledb
#Rescatar variables de entorno
import os
from dotenv import load_dotenv
# Implementar hasheo de contraseñas
import bcrypt
# Importar el tipo de dato opcional 
from typing import Optional
# Peticiones HTTP
import datetime
import requests
# Cargar las variables desde el archivo .env
load_dotenv()
# Rescatar las credenciales de conexión de Oracledb
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self, username, password, dsn):
            self.username = username, 
            self.password = password, 
            self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sentence: str, parameters: Optional [dict] = None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    return resultado
                for fila in resultado:
                    print(fila)
            connection.commit()
        except oracledb.DatabaseError as error:
            print(f"Hubo un error con la base de datos: {error}")
# Genera ña autentificación
class Auth:
    @staticmethod
    def register(db: Database, username: str, password: str):
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password.salt)
        usuario = {
            "username": username,
            "password": hashed_password
        }
        db.query(   
            "INSERT INTO USERS(id, usernamne, password) VALUES (: id, :username, :password)",
            usuario
        )
    
    @staticmethod
    def login(db: Database, username: str, password: str):
        usuario = db:query(
            "SELECT * FROM USERS WHERE username = :username",
            {"username": username}
        )

        for usuario in resultado:
            password_user = usuario[2]
            return bcrypt.checkpw(password, password_user)

class Finance:
    def __init__(self, base_url: str):
        self.base_url = base_url
    def get_uf(self, fecha: str = None):
        if not fecha:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            fecha = f"{year}-{month}-{day}"
        url = f"{self.base_url}/uf/{fecha}"
        data = requests.get(url=url).json()
        pass
    def get_uf():
        pass
    @staticmethod
    def get_utm():
        pass
    @staticmethod
    def get_dollar():
        pass
    @staticmethod
    def get_euro():
        pass
    @staticmethod
    def get_ipc():
        pass
    @staticmethod
    def get_ivp():
        pass

if __name__ == "__main__":
    db = Database(username=username, password=password, dsn=dsn)
    db.query("")