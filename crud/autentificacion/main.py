# Conectarnos a la base de datos
import oracledb
# Rescatar variables de entorno
import os
from dotenv import load_dotenv
# Implementar hasheo de contraeñas
import bcrypt
# Importar el tipo de dato Opcional
from typing import Optional
# Implementar peticiones HTTP
import requests
# Importar liberia de fechas
import datetime

# Cargar las variables desde el archivo .env
load_dotenv()

# Rescatar las credenciales de conexion con Oracle
# (Asegúrate de tener esto configurado en tu .env)
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sentence: str, parameters: Optional[dict] = None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    if sentence.lstrip().upper().startswith("SELECT"):
                        return list(resultado)
                    connection.commit()
                    return resultado
        except oracledb.DatabaseError as error:
            print(f"Hubo un error con al base de datos:\n{error}")


# Generar autenticacion
class Auth:
    @staticmethod
    def register(db: Database, username: str, password: str):
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt).decode('utf-8')
        usuario = {
            "id": 1,
            "username": username,
            "password": hashed_password
        }

        db.query(
            "INSERT INTO USERS(id,username,password) VALUES (:id,:username,:password)",
            usuario
        )
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        resultado = db.query(
            "SELECT * FROM USERS WHERE username = :username",
            {"username" : username}
        )

        if resultado:
            for usuario in resultado:
                password_user = usuario[2]
                return bcrypt.checkpw(password.encode('utf-8'), password_user.encode('utf-8'))
        return False

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    
    def get_indicator(self, indicator: str = None, fecha:str=None):
        if not indicator:
            return print("Indicador faltante")
        
        # --- CAMBIO AQUÍ ---
        # Si el usuario NO pasa fecha, NO agregamos nada a la URL.
        # Al llamar a "/api/ipc" (sin fecha), la API devuelve el historial y el [0] es el actual.
        if fecha:
            url = f"{self.base_url}/{indicator}/{fecha}"
        else:
            url = f"{self.base_url}/{indicator}" 
            
        try:
            response = requests.get(url=url)
            data = response.json()
            
            # Verificamos que 'serie' exista y tenga datos
            if 'serie' in data and len(data['serie']) > 0:
                valor = data['serie'][0]['valor']
                print(f"{indicator.upper()}: {valor}")
            else:
                print(f"{indicator.upper()}: No hay datos.")
                
        except Exception as e:
            print(f"Error al obtener {indicator}: {e}")

    # Métodos simplificados
    def get_uf(self, fecha: str = None):
        self.get_indicator("uf", fecha)
    def get_ivp(self, fecha: str = None):
        self.get_indicator("ivp", fecha)
    def get_ipc(self, fecha: str = None):
        self.get_indicator("ipc", fecha)
    def get_utm(self, fecha: str = None):
        self.get_indicator("utm", fecha)
    def get_usd(self, fecha: str = None):
        self.get_indicator("dolar", fecha)
    def get_eur(self, fecha: str = None):
        self.get_indicator("euro", fecha)
"""
if __name__ == "__main__":
    indicadores = Finance()
    print("\n1. Valor Unidad de Fomento :")
    indicadores.get_uf()
    
    print("\n2. Índice de valor Promedio :")
    indicadores.get_ivp()
    
    print("\n3. Índice de Precio al Consumidor (%) :")
    indicadores.get_ipc()
    
    print("\n4. Valor Unidad Tributaria Mensual :")
    indicadores.get_utm()
    
    print("\n5. Valor Dólar -> a Peso Chileno (CLP):")
    indicadores.get_usd()
    
    print("\n6. Valor Euro -> a Peso Chileno (CLP):")
    indicadores.get_eur()
"""
def menu_indicadores(finance_app):
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        
        print(
            """
            █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
            █             MENU FINANCIERO           █
            █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
            █                                       █
            █  [1] >> Consultar UF                  █
            █  [2] >> Consultar Dólar (USD)         █
            █  [3] >> Consultar Euro                █
            █  [4] >> Consultar UTM (Mensual)       █
            █  [5] >> Consultar IPC (Mensual)       █
            █  [6] >> Consultar IVP                 █
            █                                       █
            █  [0] >> SALIR                         █
            █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("\n--- Valor $ Unidad de Fomento ---")
            finance_app.get_uf()
            input("\nPresione ENTER para continuar...")
        
        elif opcion == "2":
            print("\n--- Valor $ Dólar -> a Peso Chileno (CLP) ---")
            finance_app.get_usd()
            input("\nPresione ENTER para continuar...")

        elif opcion == "3":
            print("\n--- Valor $ Euro -> a Peso Chileno (CLP) ---")
            finance_app.get_eur()
            input("\nPresione ENTER para continuar...")

        elif opcion == "4":
            print("\n--- Valor $ Unidad Tributaria Mensual ---")
            finance_app.get_utm()
            input("\nPresione ENTER para continuar...")

        elif opcion == "5":
            print("\n--- Valor % Índice de Precio al Consumidor ---")
            finance_app.get_ipc()
            input("\nPresione ENTER para continuar...")

        elif opcion == "6":
            print("\n--- Valor $ Índice de valor Promedio ---")
            finance_app.get_ivp()
            input("\nPresione ENTER para continuar...")

        elif opcion == "0":
            print("\nSaliendo del programa...")
            break
        else:
            input("\nOpción inválida. Presione ENTER para intentar de nuevo.")

if __name__ == "__main__":
    # Instanciamos la clase de finanzas
    app = Finance() 
    # Llamamos al menú de manera directa
    menu_indicadores(app)

"""
# Conectarnos a la base de datos
import oracledb
# Rescatar variables de entorno
import os
from dotenv import load_dotenv
# Implementar hasheo de contraeñas
import bcrypt
# Importar el tipo de dato Opcional
from typing import Optional
# Implementar peticiones HTTP
import requests
# Importar liberia de fechas
import datetime
# Cargar las variables desde el archivo .env
load_dotenv()
# Rescatar las credenciales de conexion con Oracle
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sentence: str, parameters: Optional[dict] = None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    return resultado
                connection.commit()
        except oracledb.DatabaseError as error:
            print(f"Hubo un error con al base de datos:\n{error}")


# Generar autenticacion
class Auth:
    @staticmethod
    def register(db: Database, username: str, password: str):
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password,salt)
        usuario = {
            "id": 1,
            "username": username,
            "password": hashed_password
        }

        db.query(
            "INSERT INTO USERS(id,username,password) VALUES (:id,:username:password)",
            usuario
        )
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        resultado = db.query(
            "SELECT * FROM USERS WHERE username = :username",
            {"username" : username}
        )

        for usuario in resultado:
            password_user = usuario[2]
            return bcrypt.checkpw(password, password_user)

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    def get_indicator(self, indicator: str = None, fecha:str=None):
        if not indicator:
            return print("Indicador faltante")
        if not fecha:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            fecha = f"{day}-{month}-{year}"
        url = f"{self.base_url}/{indicator}/{fecha}"
        data = requests.get(url=url).json()
        print(data['serie'][0]['valor']) 
    def get_uf(self, fecha: str = None):
        self.get_indicator("uf", fecha)
    def get_ivp(self, fecha: str = None):
        self.get_indicator("ivp", fecha)
    def get_ipc(self, fecha: str = None):
        self.get_indicator("ipc", fecha)
    def get_utm(self, fecha: str = None):
        self.get_indicator("utm", fecha)
    def get_usd(self, fecha: str = None):
        self.get_indicator("dolar", fecha)
    def get_eur(self, fecha: str = None):
        self.get_indicator("euro", fecha)

if __name__ == "__main__":
    indicadores = Finance()
"""