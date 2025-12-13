import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

# Cargo las credenciales desde el archivo .env
load_dotenv()

class Database:
    def __init__(self, username, dsn, password):
        # Guardo los datos de conexión
        self.username = username
        self.dsn = dsn
        self.password = password

    def get_connection(self):
        # Creo la conexión real usando la librería
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)  

    def create_all_tables(self):
        # Defino las sentencias SQL para crear las tablas necesarias
        tables = [
            (
                "CREATE TABLE USERS ("
                "id INTEGER PRIMARY KEY, "
                "username VARCHAR2(32) UNIQUE, "
                "password VARCHAR2(128)"
                ")"
            ),
            # Tabla para cumplir con el requisito de Historial
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
        # Recorro la lista y ejecuto la creación.
        # OJO: Aquí ya no uso try-except para que si hay un error real, se muestre en query.
        for table in tables:
            self.query(table)

    def query(self, sql: str, parameters: Optional[dict] = None):
            try:
                # Uso 'with' para asegurar que la conexión se cierre bien
                with self.get_connection() as connection:
                    with connection.cursor() as cursor:
                        ejecucion = cursor.execute(sql, parameters)
                        
                        # Si es una consulta de lectura (SELECT), devuelvo los datos
                        if sql.strip().upper().startswith("SELECT"):
                            resultado = []
                            for fila in ejecucion:
                                resultado.append(fila)
                            return resultado 
                        
                        # Si es escritura (INSERT, CREATE), guardo los cambios
                        connection.commit()
                        return True 
            except oracledb.DatabaseError as error:
                # Si el error es 955, es porque la tabla ya existe. 
                # Ese error lo oculto para que no se vea feo al iniciar.
                if "ORA-00955" in str(error):
                    return False 
                
                # Cualquier otro error (permisos, sintaxis) SÍ lo muestro
                print(f"Error BD: {error}")
                return False
 
    def get_next_id(self, table_name):
        # Truco para calcular el ID manual y evitar error ORA-01400 (NULL ID)
        try:
            res = self.query(f"SELECT NVL(MAX(id), 0) + 1 FROM {table_name}")
            return res[0][0] if res else 1
        except:
            return 1

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        # Paso la contraseña a bytes
        password_bytes = password.encode('utf-8')
        
        # Busco si existe el usuario
        resultado = db.query(
            sql = "SELECT * FROM USERS WHERE username = :username",
            parameters = {"username": username}
        )
        
        if not resultado or len(resultado) == 0:
            print("(!) Usuario no encontrado")
            return None 
        
        # Obtengo el hash de la BD (columna 2)
        hashed_password = resultado[0][2].encode('utf-8')
        
        # Comparo
        if bcrypt.checkpw(password_bytes, hashed_password):
            return username 
        else:
            print("(!) Contraseña incorrecta")
            return None

    @staticmethod
    def register(db: Database, username: str, password: str):
        print(">> Registrando usuario...")
        password = password.encode('utf-8')
        
        # Aplico hash + salt por seguridad
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password, salt)

        # Calculo ID
        next_id = db.get_next_id("USERS")

        usuario = {
            "id": next_id,
            "username": username,
            "password": hash_password.decode('utf-8') 
        }

        # Guardo y verifico si funcionó
        exito = db.query(
            "INSERT INTO USERS (id, username, password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        
        if exito:
            print(f">> Usuario {username} registrado con éxito.")
        else:
            print("(!) Error: No se pudo registrar el usuario en la Base de Datos.")

class Finance:
    def __init__(self, db: Database, usuario_actual: str, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url   
        self.db = db
        self.usuario_actual = usuario_actual # Guardo quién está usando el sistema

    def get_indicator(self, indicator: str, fecha: str = None):
        try:
            # Armo la URL según si es hoy o fecha pasada
            url = f"{self.base_url}/{indicator}"
            if fecha:
                url = f"{url}/{fecha}"
            
            respuesta = requests.get(url).json()
            
            valor = 0
            fecha_valor = ""
            
            # Proceso la respuesta JSON de la API
            if fecha: 
                if len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]
            else: 
                if 'serie' in respuesta and len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]

            # Si tengo un valor válido, lo guardo en Oracle (Requisito obligatorio)
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

    def get_rango(self, indicator, anio):
        try:
            url = f"{self.base_url}/{indicator}/{anio}"
            print(f"Consultando año {anio}...")
            respuesta = requests.get(url).json()
            
            if 'serie' in respuesta:
                print(f"{'FECHA':<12} | {'VALOR':<10}")
                print("-" * 25)
                for item in respuesta['serie']:
                    print(f"{item['fecha'][:10]:<12} | ${item['valor']}")
        except:
            print("Error consultando rango")

    def ver_historial_usuario(self):
        # Muestro el historial filtrado por el usuario actual
        print(f"\n======== HISTORIAL DE: {self.usuario_actual} ========")
        sql = "SELECT indicador, valor, fecha_dato, fecha_consulta FROM HISTORIAL WHERE usuario = :u ORDER BY id DESC"
        datos = self.db.query(sql, {"u": self.usuario_actual})
        
        if datos and len(datos) > 0:
            print(f"{'INDICADOR':<10} | {'VALOR':<10} | {'FECHA DATO':<12} | {'FECHA CONSULTA'}")
            print("-" * 65)
            for fila in datos:
                ind = fila[0].upper()
                val = fila[1]
                f_dato = fila[2]
                f_cons = fila[3].strftime("%Y-%m-%d %H:%M") 
                print(f"{ind:<10} | ${val:<9} | {f_dato:<12} | {f_cons}")
        else:
            print(">> No tienes consultas guardadas en el historial.")


    # Métodos "wrapper" para cada indicador
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
    # Inicio la conexión
    db = Database(
        username=os.getenv("ORACLE_USER"),
        dsn=os.getenv("ORACLE_DSN"),
        password=os.getenv("ORACLE_PASSWORD")
    )
    # Intento crear tablas (si fallan, saldrá el error en consola)
    db.create_all_tables()

    # --- MENU DE LOGIN ---
    usuario_logueado = None
    while not usuario_logueado:
        print("\n")
        print("█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print("█      ACCESO DE USUARIOS      █")
        print("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print(" [1] Iniciar Sesión")
        print(" [2] Registrarse")
        op = input(" >> Seleccione: ")
        
        if op == "1":
            u = input(" Usuario: ")
            p = input(" Contraseña: ")
            usuario_logueado = Auth.login(db, u, p)
        elif op == "2":
            u = input(" Nuevo Usuario: ")
            p = input(" Nueva Contraseña: ")
            Auth.register(db, u, p)

    # --- MENU PRINCIPAL ---
    indicadores = Finance(db, usuario_logueado)
    
    while True:
        print("\n")
        print("            █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
        print("            █             MENU FINANCIERO           █")
        print("            █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        print("            █                                       █")
        print("            █  [1] >> Consultar Indicador (Día)     █")
        print("            █  [2] >> Consultar Periodo (Año)       █")
        print("            █  [3] >> Ver Mi Historial              █")
        print("            █                                       █")
        print("            █  [4] >> SALIR                         █")
        print("            █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█")
        
        sel = input("            >> Opción: ")
        
        if sel == "4": 
            print("Cerrando sesión... ¡Hasta luego!")
            break
        
        if sel == "3": 
            indicadores.ver_historial_usuario()
            input("\nPresione ENTER para volver...")
            continue

        if sel == "1":
            print("\n   --- SELECCIÓN DE INDICADOR ---")
            print("   UF | Dolar | Euro | UTM | IPC | IVP")
            # Con .lower() el usuario puede escribir UF o uf y funciona igual
            tipo = input("   >> Escriba el nombre: ").lower()
            fecha = input("   >> Fecha (dd-mm-yyyy) o ENTER para hoy: ")
            if fecha == "": fecha = None
            
            if tipo == "uf": indicadores.get_uf(fecha)
            elif tipo == "dolar": indicadores.get_usd(fecha)
            elif tipo == "euro": indicadores.get_eur(fecha)
            elif tipo == "utm": indicadores.get_utm(fecha)
            elif tipo == "ipc": indicadores.get_ipc(fecha)
            elif tipo == "ivp": indicadores.get_ivp(fecha)
            else: print("   (!) Indicador no válido.")
            input("   Presione ENTER para continuar...")

        elif sel == "2":
            print("\n   --- CONSULTA DE PERIODO (AÑO) ---")
            print("   UF | Dolar | Euro | UTM | IPC | IVP")
            tipo = input("   >> Escriba el nombre: ").lower()
            anio = input("   >> Ingrese Año (ej: 2024): ")
            indicadores.get_rango(tipo, anio)
            input("   Presione ENTER para continuar...")