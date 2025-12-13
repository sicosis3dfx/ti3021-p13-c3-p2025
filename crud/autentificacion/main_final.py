import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()

class Database:
    def __init__(self, username, dsn, password):
        self.username = username
        self.dsn = dsn
        self.password = password
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)  
    def create_all_tables(self):
        tables = [
            (
                "CREATE TABLE USERS ("
                "id INTEGER PRIMARY KEY, "
                "username VARCHAR2(32) UNIQUE, "
                "password VARCHAR2(128)"
                ")"
            ),
            # AGREGADO: Tabla obligatoria para Historial de consultas
            (
                "CREATE TABLE HISTORIAL ("
                "id INTEGER PRIMARY KEY, "
                "indicador VARCHAR2(20), "
                "valor NUMBER(10, 2), "
                "fecha_dato VARCHAR2(20), "
                "fecha_consulta DATE DEFAULT SYSDATE, "
                "usuario VARCHAR2(32)"
                ")"
            )
        ]
        for table in tables:
            try:
                self.query(table)
            except:
                pass # Si la tabla existe, ignoramos el error para no detener el programa


    def query(self, sql: str, parameters: Optional[dict] = None):
            try:
                with self.get_connection() as connection:
                    with connection.cursor() as cursor:
                        ejecucion = cursor.execute(sql, parameters)
                        if sql.strip().upper().startswith("SELECT"):
                            resultado = []
                            for fila in ejecucion:
                                resultado.append(fila)
                            return resultado 
                        connection.commit()
                        return True  # Retornamos True para saber si guardó bien
            except oracledb.DatabaseError as error:
                # Si es el error 955 (tabla existe), lo ignoramos.
                if "ORA-00955" in str(error):
                    return False 
                
                # Si es otro error, sí lo mostramos
                print(f"Error BD: {error}")
                return [] # Retornamos lista vacía en error para no romper len()
 
    # AGREGADO: Metodo para arreglar el error ORA-01400 (Falta de ID)
    def get_next_id(self, table_name):
        res = self.query(f"SELECT NVL(MAX(id), 0) + 1 FROM {table_name}")
        return res[0][0] if res else 1

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        # Corrección: codificar a utf-8 para evitar errores de tipo
        password_bytes = password.encode('utf-8')
        resultado = db.query(
            sql = "SELECT * FROM USERS WHERE username = :username",
            parameters = {"username": username}
        )
        
        if not resultado or len(resultado) == 0:
            print("Usuario no encontrado")
            return None # Retornamos None si falla
        
        # Recuperamos password de la BD (indice 2)
        hashed_password = resultado[0][2].encode('utf-8')
        
        if bcrypt.checkpw(password_bytes, hashed_password):
            print("Inicio de sesión exitoso")
            return username # Retornamos el usuario para guardarlo en el historial
        else:
            print("Contraseña incorrecta")
            return None

    @staticmethod
    def register(db: Database, username: str, password: str):
        # Modificado: Calculamos el ID aqui para arreglar el error ORA-01400
        print("Registrando usuario...")
        password = password.encode('utf-8')
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password, salt)

        # Obtenemos el siguiente ID disponible
        next_id = db.get_next_id("USERS")

        usuario = {
            "id": next_id,
            "username": username,
            "password": hash_password.decode('utf-8') # Guardamos como string en Oracle
        }

        db.query(
            "INSERT INTO USERS (id, username, password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        print(f"Usuario {username} registrado con éxito (ID: {next_id}).")

class Finance:
    # Modificado: Recibimos db y usuario para poder guardar el historial
    def __init__(self, db: Database, usuario_actual: str, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url   
        self.db = db
        self.usuario_actual = usuario_actual

    def get_indicator(self, indicator: str, fecha: str = None):
        try:
            url = f"{self.base_url}/{indicator}"
            if fecha:
                url = f"{url}/{fecha}"
            
            respuesta = requests.get(url).json()
            
            # Para extraer valor (API devuelve distinto si es fecha o actual)
            valor = 0
            fecha_valor = ""
            
            if fecha: # Busqueda especifica
                if len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]
            else: # Valor actual
                if 'serie' in respuesta and len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]

            # AGREGADO: Se Guardar en Base de Datos 
            if valor > 0:
                next_id = self.db.get_next_id("HISTORIAL")
                sql = "INSERT INTO HISTORIAL (id, indicador, valor, fecha_dato, usuario) VALUES (:id, :ind, :val, :fec, :usu)"
                params = {
                    "id": next_id, "ind": indicator, "val": valor, 
                    "fec": fecha_valor, "usu": self.usuario_actual
                }
                self.db.query(sql, params)
                return valor
            return 0
        except Exception as e:
            print(f"Error al obtener el indicador: {e}")
            return 0

    # AGREGADO: Metodo para Rangos
    def get_rango(self, indicator, anio):
        try:
            url = f"{self.base_url}/{indicator}/{anio}"
            print(f"Consultando año {anio}...")
            respuesta = requests.get(url).json()
            if 'serie' in respuesta:
                for item in respuesta['serie']:
                    print(f"Fecha: {item['fecha'][:10]} | Valor: {item['valor']}")
                    # Aquí podrías guardar masivamente si quisieras
        except:
            print("Error consultando rango")

    def get_uf(self, fecha: str = None):
        valor = self.get_indicator("uf", fecha)
        print(f"Valor Unidad de Fomento (UF): ${valor}")
    def get_usd(self, fecha: str = None):
        valor = self.get_indicator("dolar", fecha) 
        print(f"Valor Dólar (USD): ${valor}")
    def get_eur(self, fecha: str = None):
        valor = self.get_indicator("euro", fecha)
        print(f"Valor Euro (EUR): ${valor}")
    def get_utm(self, fecha: str = None):
        valor = self.get_indicator("utm", fecha)
        print(f"Valor UTM: ${valor}")
    def get_ipc(self, fecha: str = None):
        valor = self.get_indicator("ipc", fecha)
        print(f"Valor IPC: {valor}%")
    def get_ivp(self, fecha: str = None):
        valor = self.get_indicator("ivp", fecha)
        print(f"Valor IVP: ${valor}")
    
       
if __name__ == "__main__":
    db = Database(
        username=os.getenv("ORACLE_USER"),
        dsn=os.getenv("ORACLE_DSN"),
        password=os.getenv("ORACLE_PASSWORD")
    )
    db.create_all_tables()

    # --- MENU DE LOGIN ---
    usuario_logueado = None
    while not usuario_logueado:
        print("\n1. Login | 2. Registro")
        op = input("Opción: ")
        if op == "1":
            u = input("User: ")
            p = input("Pass: ")
            usuario_logueado = Auth.login(db, u, p)
        elif op == "2":
            u = input("Nuevo User: ")
            p = input("Nueva Pass: ")
            # Quitamos el ID manual, lo calcula la clase Auth
            Auth.register(db, u, p)

    # --- MENU PRINCIPAL (Ya autenticado) ---
    indicadores = Finance(db, usuario_logueado) # Pasamos el usuario para guardar historial
    
    while True:
        print("\n--- MENU FINANCIERO ---")
        print("1. Consultar Indicadores (Actual o Fecha)")
        print("2. Consultar Periodo (Año completo)")
        print("3. Salir")
        sel = input(">> ")
        
        if sel == "3": break
        
        if sel == "1":
            tipo = input("Indicador (UF, Dolar, Euro, UTM, IPC, IVP): ").lower()
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ")
            if fecha == "": fecha = None
            
            if tipo == "uf": indicadores.get_uf(fecha)
            elif tipo == "dolar": indicadores.get_usd(fecha)
            elif tipo == "euro": indicadores.get_eur(fecha)
            elif tipo == "utm": indicadores.get_utm(fecha)
            elif tipo == "ipc": indicadores.get_ipc(fecha)
            elif tipo == "ivp": indicadores.get_ivp(fecha)

        elif sel == "2":
            tipo = input("Indicador (UF, Dolar, Euro, UTM, IPC, IVP): ").lower()
            anio = input("Año (ej: 2024): ")
            indicadores.get_rango(tipo, anio)