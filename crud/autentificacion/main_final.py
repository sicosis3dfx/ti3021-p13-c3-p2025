import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

# Cargo las credenciales del archivo .env
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
            # Esta es la tabla para guardar las consultas.
            # Agregué el campo 'origen' porque la pauta pide registrar el sitio proveedor.
            (
                "CREATE TABLE HISTORIAL_FINANCIERO ("
                "id INTEGER PRIMARY KEY, "
                "indicador VARCHAR2(20), "
                "valor NUMBER(10, 2), "
                "fecha_dato VARCHAR2(20), "
                "fecha_consulta DATE DEFAULT SYSDATE, "
                "usuario VARCHAR2(32), "
                "origen VARCHAR2(50)" 
                ")"
            )
        ]

        for table in tables:
            self.query(table)

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
                        return True 
            except oracledb.DatabaseError as error:
                # Si me sale el error 955 es porque la tabla ya existe.
                # Lo filtro para que no me llene la consola de errores rojos al iniciar.
                if "ORA-00955" in str(error):
                    return False 
                # Si es otro error (como credenciales o permisos), que me avise
                print(f"Error BD: {error}")
                return False
 
    def get_next_id(self, table_name):
        # Tuve problemas con el autoincrementable (error ORA-01400), así que hice esta función
        # para buscar el último ID y sumarle 1 manualmente.
        try:
            res = self.query(f"SELECT NVL(MAX(id), 0) + 1 FROM {table_name}")
            return res[0][0] if res else 1
        except:
            return 1

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        # bcrypt necesita que la password esté en bytes
        password_bytes = password.encode('utf-8')
        
        # Busco si el usuario existe en la base de datos
        resultado = db.query(
            sql = "SELECT * FROM USERS WHERE username = :username",
            parameters = {"username": username}
        )
        
        if not resultado or len(resultado) == 0:
            print("(!) Usuario no encontrado")
            return None 
        
        # Saco el hash que estaba guardado (está en la columna 2)
        hashed_password = resultado[0][2].encode('utf-8')
        
        # Comparo la clave ingresada con el hash guardado
        if bcrypt.checkpw(password_bytes, hashed_password):
            return username # Devuelvo el usuario para usarlo en el menú
        else:
            print("(!) Contraseña incorrecta")
            return None

    @staticmethod
    def register(db: Database, username: str, password: str):
        print(">> Registrando usuario...")
        password = password.encode('utf-8')
        
        # Generamos el hash con salt para que sea seguro
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password, salt)

        # Obtengo el siguiente ID disponible
        next_id = db.get_next_id("USERS")

        usuario = {
            "id": next_id,
            "username": username,
            "password": hash_password.decode('utf-8') # Lo paso a string para que Oracle no reclame
        }

        # Guardo en la base de datos
        exito = db.query(
            "INSERT INTO USERS (id, username, password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        
        # Verifico si realmente se guardó
        if exito:
            print(f">> Usuario {username} registrado con éxito.")
        else:
            print("(!) Error: No se pudo registrar en la Base de Datos.")

class Finance:
    def __init__(self, db: Database, usuario_actual: str, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url   
        self.db = db
        self.usuario_actual = usuario_actual # Guardo el usuario logueado para el historial

    def get_indicator(self, indicator: str, fecha: str = None):
        try:
            # Armo la URL dependiendo si piden el valor de hoy o una fecha pasada
            url = f"{self.base_url}/{indicator}"
            if fecha:
                url = f"{url}/{fecha}"
            
            # Consumo la API
            respuesta = requests.get(url).json()
            
            valor = 0
            fecha_valor = ""
            
            # La API entrega los datos distinto si es por fecha o actual, aquí lo filtro
            if fecha: 
                if len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]
            else: 
                if 'serie' in respuesta and len(respuesta['serie']) > 0:
                    valor = respuesta['serie'][0]['valor']
                    fecha_valor = respuesta['serie'][0]['fecha'][:10]

            # Requisito: Si tengo un valor, debo guardarlo en la BD
            if valor > 0:
                next_id = self.db.get_next_id("HISTORIAL_FINANCIERO")
                
                # Aquí cumplo con registrar el "sitio que provee los indicadores"
                sql = """
                    INSERT INTO HISTORIAL_FINANCIERO 
                    (id, indicador, valor, fecha_dato, usuario, origen) 
                    VALUES (:id, :ind, :val, :fec, :usu, :ori)
                """
                params = {
                    "id": next_id, 
                    "ind": indicator, 
                    "val": valor, 
                    "fec": fecha_valor, 
                    "usu": self.usuario_actual,
                    "ori": "mindicador.cl" # Dejo fijo el origen de los datos
                }
                self.db.query(sql, params)
                return valor
            return 0
        except Exception as e:
            print(f"Error al obtener el indicador: {e}")
            return 0

    def get_rango(self, indicator, anio):
        # Esta función es para consultar todo un año o período completo
        try:
            url = f"{self.base_url}/{indicator}/{anio}"
            print(f"Consultando año {anio}...")
            respuesta = requests.get(url).json()
            
            if 'serie' in respuesta:
                print(f"{'FECHA':<12} | {'VALOR':<10}")
                print("-" * 25)
                for item in respuesta['serie']:
                    # Muestro solo los primeros 10 caracteres de la fecha
                    print(f"{item['fecha'][:10]:<12} | ${item['valor']}")
        except:
            print("Error consultando rango")

    def ver_historial_usuario(self):
        # Muestro el historial filtrando por el usuario que está conectado
        print(f"\n========     HISTORIAL DE BÚSQUEDA DEL USUARIO: {self.usuario_actual}     ========")
        sql = "SELECT indicador, valor, fecha_dato, fecha_consulta, origen FROM HISTORIAL_FINANCIERO WHERE usuario = :u ORDER BY id DESC"
        datos = self.db.query(sql, {"u": self.usuario_actual})
        
        if datos and len(datos) > 0:
            print(f"{'INDICADOR':<10} | {'VALOR':<10} | {'FECHA DATO':<12} | {'ORIGEN':<15} | {'FECHA CONSULTA'}")
            print("-" * 80)
            for fila in datos:
                ind = fila[0].upper()
                val = fila[1]
                f_dato = fila[2]
                f_cons = fila[3].strftime("%Y-%m-%d %H:%M") 
                origen = fila[4]
                print(f"{ind:<10} | ${val:<9} | {f_dato:<12} | {origen:<15} | {f_cons}")
        else:
            print(">> No tienes consultas guardadas en el historial.")


    # Métodos simples para llamar a cada indicador
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
    # Inicio la conexión a la base de datos
    db = Database(
        username=os.getenv("ORACLE_USER"),
        dsn=os.getenv("ORACLE_DSN"),
        password=os.getenv("ORACLE_PASSWORD")
    )
    # Creo las tablas al inicio. Si fallan, la función query avisará.
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
        # Menú visual solicitado
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
            # Uso .lower() para aceptar mayúsculas y minúsculas sin problema
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