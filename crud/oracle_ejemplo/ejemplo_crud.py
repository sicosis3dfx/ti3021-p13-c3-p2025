import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

def create_schema(query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print("Tabla verificada/creada.")
    except oracledb.DatabaseError as error:
        print(f"Nota: {error}")

def create_all_tables():
    print("--- Creando Tablas ---")
    tablas = [
        
        """
        CREATE TABLE Eventos (
            idevento NUMBER PRIMARY KEY,
            nombre VARCHAR2(50) NOT NULL,
            fecha DATE,
            lugar VARCHAR2(50)
        )
        """,
        
        """
        CREATE TABLE Participantes (
            idparticipante NUMBER PRIMARY KEY,
            nombre VARCHAR2(50) NOT NULL,
            rut VARCHAR2(12) UNIQUE,
            edad NUMBER,
            numeroinscripcion NUMBER
        )
        """,
        
        """
        CREATE TABLE Atletas (
            idparticipante NUMBER PRIMARY KEY,
            disciplina VARCHAR2(50),
            marca FLOAT,
            FOREIGN KEY (idparticipante) REFERENCES Participantes(idparticipante)
        )
        """,
        
        """
        CREATE TABLE Entrenadores (
            identrenador NUMBER PRIMARY KEY,
            equipo VARCHAR2(50)
        )
        """,
        
        """
        CREATE TABLE Jueces (
            idjuez NUMBER PRIMARY KEY,
            especialidad VARCHAR2(50)
        )
        """,

        """
        CREATE TABLE Inscripciones (
            idevento NUMBER,
            idparticipante NUMBER,
            PRIMARY KEY (idevento, idparticipante),
            FOREIGN KEY (idevento) REFERENCES Eventos(idevento),
            FOREIGN KEY (idparticipante) REFERENCES Participantes(idparticipante)
        )
        """
    ]

    for query in tablas:
        print(f"Procesando tabla...") 
        create_schema(query)

# --- CREATES ---

def create_eventos(id: int, nombre: str, fecha: str, lugar: str):
    sql = (
        "INSERT INTO Eventos (idevento, nombre, fecha, lugar) "
        "VALUES (:id, :nombre, :fecha, :lugar)" 
    )
    try:
        parametros = {
            "id": id,
            "nombre": nombre,
            "fecha": datetime.strptime(fecha, '%d-%m-%Y'),
            "lugar": lugar
        }   
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print("Inserción de datos exitosa.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar: {error}")
    except ValueError:
        print("Error: Formato de fecha incorrecto.")

def create_participantes(id: int, nombre: str, rut: str, edad: int, numeroinscripcion: int):
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
        print(f"No se pudo insertar: {error}")

def create_atletas(idparticipante: int, disciplina: str, marca: float):
    sql = (
        "INSERT INTO Atletas (idparticipante, disciplina, marca) "
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
        print(f"No se pudo insertar (Verifique que el ID exista en Participantes): \n{error}")

def create_entrenadores(identrenador: int, equipo: str):
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
        print(f"No se pudo insertar: {error}")

def create_jueces(idjuez: int, especialidad: str):
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
        print(f"No se pudo insertar: {error}")

# --- READS ---

def read_eventos():
    sql = "SELECT * FROM Eventos"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql)
                print("\n--- Eventos ---")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

def read_participantes():
    sql = "SELECT * FROM Participantes"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql)
                print("\n--- Participantes ---")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

def read_participante_by_id(id: int):
    sql = "SELECT * FROM Participantes WHERE idparticipante = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql, parametros)
                rows = list(resultado)
                if not rows:
                    print(f"No hay registros con el ID {id}")
                for fila in rows:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

def read_atletas():
    sql = "SELECT * FROM Atletas"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql)
                print("\n--- Atletas ---")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

def read_entrenadores():
    sql = "SELECT * FROM Entrenadores"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql)
                print("\n--- Entrenadores ---")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

def read_jueces():
    sql = "SELECT * FROM Jueces"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                resultado = cursor.execute(sql)
                print("\n--- Jueces ---")
                for fila in resultado:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"Error al leer: {error}")

# --- UPDATES ---

def update_evento(id: int, nombre: Optional[str] = None, fecha: Optional[str] = None, lugar: Optional[str] = None):
    modificaciones = []
    parametros = {"id": id}

    if nombre:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if fecha:
        try:
            modificaciones.append("fecha = :fecha")
            parametros["fecha"] = datetime.strptime(fecha, '%d-%m-%Y')
        except ValueError:
            print("Fecha inválida omitida.")
    if lugar:
        modificaciones.append("lugar = :lugar")
        parametros["lugar"] = lugar
    
    if not modificaciones:
        print("No hay campos para actualizar.")
        return
    
    sql = f"UPDATE Eventos SET {', '.join(modificaciones)} WHERE idevento = :id"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Evento {id} actualizado.")
    except oracledb.DatabaseError as error:
        print(f"Error update: {error}")

def update_participante(id: int, nombre: Optional[str] = None, rut: Optional[str] = None, edad: Optional[int] = None, numeroinscripcion: Optional[int] = None):
    modificaciones = []
    parametros = {"id": id}

    if nombre:
        modificaciones.append("nombre = :nombre")
        parametros["nombre"] = nombre
    if rut:
        modificaciones.append("rut = :rut")
        parametros["rut"] = rut
    if edad:
        modificaciones.append("edad = :edad")
        parametros["edad"] = edad
    if numeroinscripcion:
        modificaciones.append("numeroinscripcion = :numeroinscripcion")
        parametros["numeroinscripcion"] = numeroinscripcion
    
    if not modificaciones:
        print("No hay campos para actualizar.")
        return

    sql = f"UPDATE Participantes SET {', '.join(modificaciones)} WHERE idparticipante = :id"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Participante {id} actualizado.")
    except oracledb.DatabaseError as error:
        print(f"Error update: {error}")

def update_atleta(idparticipante: int, disciplina: Optional[str] = None, marca: Optional[float] = None):
    modificaciones = []
    parametros = {"idparticipante": idparticipante}

    if disciplina:
        modificaciones.append("disciplina = :disciplina")
        parametros["disciplina"] = disciplina
    if marca:
        modificaciones.append("marca = :marca")
        parametros["marca"] = marca
    
    if not modificaciones:
        print("No hay campos para actualizar.")
        return
    
    sql = f"UPDATE Atletas SET {', '.join(modificaciones)} WHERE idparticipante = :idparticipante"
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Atleta {idparticipante} actualizado.")
    except oracledb.DatabaseError as error:
        print(f"Error update: {error}")

def update_entrenador(identrenador: int, equipo: Optional[str] = None):
    modificaciones = []
    parametros = {"identrenador": identrenador}

    if equipo:
        modificaciones.append("equipo = :equipo")
        parametros["equipo"] = equipo
    
    if not modificaciones:
        print("No hay campos para actualizar.")
        return
    
    sql = f"UPDATE Entrenadores SET {', '.join(modificaciones)} WHERE identrenador = :identrenador"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Entrenador {identrenador} actualizado.")
    except oracledb.DatabaseError as error:
        print(f"Error update: {error}")

def update_juez(idjuez: int, especialidad: Optional[str] = None):
    modificaciones = []
    parametros = {"idjuez": idjuez}

    if especialidad:
        modificaciones.append("especialidad = :especialidad")
        parametros["especialidad"] = especialidad
    
    if not modificaciones:
        print("No hay campos para actualizar.")
        return
    
    sql = f"UPDATE Jueces SET {', '.join(modificaciones)} WHERE idjuez = :idjuez"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Juez {idjuez} actualizado.")
    except oracledb.DatabaseError as error:
        print(f"Error update: {error}")

# --- DELETES ---

def delete_evento(id: int):
    sql = "DELETE FROM Eventos WHERE idevento = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {id} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo eliminar: {error}")

def delete_participantes(id: int):
    sql = "DELETE FROM Participantes WHERE idparticipante = :id"
    parametros = {"id": id}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {id} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo eliminar (Posiblemente tenga datos asociados en Atletas): {error}")

def delete_atleta(idparticipante: int):
    sql = "DELETE FROM Atletas WHERE idparticipante = :idparticipante"
    parametros = {"idparticipante": idparticipante}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {idparticipante} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo eliminar: {error}")

def delete_entrenador(identrenador: int):
    sql = "DELETE FROM Entrenadores WHERE identrenador = :identrenador"
    parametros = {"identrenador": identrenador}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {identrenador} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo eliminar: {error}")

def delete_juez(idjuez: int):
    sql = "DELETE FROM Jueces WHERE idjuez = :idjuez"
    parametros = {"idjuez": idjuez}
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
                connection.commit()
                print(f"Dato con ID {idjuez} eliminado exitosamente.")
    except oracledb.DatabaseError as error:
        print(f"No se pudo eliminar: {error}")


# --- MENÚS ---

def menu_eventos():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |        Menu: Eventos             |
                |----------------------------------|
                | 1. Crear Evento                  |
                | 2. Listar Eventos                |
                | 3. Modificar Evento              |
                | 4. Eliminar Evento               |
                | 0. Volver                        |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            os.system("cls")
            print("\n--- Crear Evento ---")
            try:
                id = int(input("ID Evento: "))
                nombre = input("Nombre: ")
                fecha = input("Fecha (DD-MM-YYYY): ")
                lugar = input("Lugar: ")
                create_eventos(id, nombre, fecha, lugar)
            except ValueError:
                print("Error: El ID debe ser un número.")
            input("ENTER para continuar...")

        elif opcion == "2":
            os.system("cls")
            read_eventos()
            input("ENTER para continuar...")

        elif opcion == "3":
            os.system("cls")
            print("\n--- Modificar Evento ---")
            id = input("ID del evento a modificar: ")
            print("[Deje en blanco si no desea modificar el campo]")
            nombre = input("Nuevo nombre: ")
            fecha = input("Nueva fecha (DD-MM-YYYY): ")
            lugar = input("Nuevo lugar: ")

            nombre = nombre if len(nombre.strip()) > 0 else None
            fecha = fecha if len(fecha.strip()) > 0 else None
            lugar = lugar if len(lugar.strip()) > 0 else None

            update_evento(id, nombre, fecha, lugar)
            input("ENTER para continuar...")

        elif opcion == "4":
            os.system("cls")
            id = input("ID a eliminar: ")
            delete_evento(id)
            input("ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def menu_participantes():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |      Menu: Participantes         |
                |----------------------------------|
                | 1. Inscribir Participante        |
                | 2. Listar Participantes          |
                | 3. Buscar por ID                 |
                | 4. Modificar Participante        |
                | 5. Eliminar Participante         |
                | 0. Volver                        |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            print("\n--- Crear Participante ---")
            try:
                id = int(input("ID Participante: "))
                nombre = input("Nombre Completo: ")
                rut = input("RUT: ")
                edad = int(input("Edad: "))
                num = int(input("Número de Inscripción: "))
                create_participantes(id, nombre, rut, edad, num)
            except ValueError:
                print("Error: ID, Edad y Número deben ser enteros.")
            input("ENTER para continuar...")

        elif opcion == "2":
            os.system("cls")
            read_participantes()
            input("ENTER para continuar...")

        elif opcion == "3":
            os.system("cls")
            id = input("ID a buscar: ")
            read_participante_by_id(id)
            input("ENTER para continuar...")

        elif opcion == "4":
            os.system("cls")
            print("\n--- Modificar Participante ---")
            id = input("ID del participante a modificar: ")
            print("[Deje en blanco si no desea modificar el campo]")
            
            nombre = input("Nuevo Nombre: ")
            rut = input("Nuevo RUT: ")
            edad_str = input("Nueva Edad: ")
            
            nombre = nombre if len(nombre.strip()) > 0 else None
            rut = rut if len(rut.strip()) > 0 else None
            edad = int(edad_str) if len(edad_str.strip()) > 0 else None

            update_participante(id, nombre, rut, edad)
            input("ENTER para continuar...")

        elif opcion == "5":
            os.system("cls")
            id = input("ID a eliminar: ")
            delete_participantes(id)
            input("ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def menu_atletas():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |         Menu: Atletas            |
                |----------------------------------|
                | 1. Registrar Atleta              |
                | 2. Listar Atletas                |
                | 3. Modificar Atleta              |
                | 4. Eliminar Atleta               |
                | 0. Volver                        |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            print("\n--- Crear Atleta ---")
            try:
                id = int(input("ID del Participante (ya existente): "))
                disciplina = input("Disciplina: ")
                marca = float(input("Marca (decimal): "))
                create_atletas(id, disciplina, marca)
            except ValueError:
                print("Error: ID debe ser entero y Marca un número decimal.")
            input("ENTER para continuar...")

        elif opcion == "2":
            os.system("cls")
            read_atletas()
            input("ENTER para continuar...")

        elif opcion == "3":
            os.system("cls")
            print("\n--- Modificar Atleta ---")
            id = input("ID del Participante/Atleta a modificar: ")
            print("[Deje en blanco si no desea modificar el campo]")
            
            disciplina = input("Nueva Disciplina: ")
            marca_str = input("Nueva Marca: ")
            
            disciplina = disciplina if len(disciplina.strip()) > 0 else None
            marca = float(marca_str) if len(marca_str.strip()) > 0 else None

            update_atleta(id, disciplina, marca)
            input("ENTER para continuar...")

        elif opcion == "4":
            os.system("cls")
            id = input("ID del Atleta a eliminar: ")
            delete_atleta(id)
            input("ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def menu_entrenadores():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |       Menu: Entrenadores         |
                |----------------------------------|
                | 1. Registrar Entrenador          |
                | 2. Listar Entrenadores           |
                | 3. Modificar Entrenador          |
                | 4. Eliminar Entrenador           |
                | 0. Volver                        |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            print("\n--- Crear Entrenador ---")
            try:
                id = int(input("ID Entrenador: "))
                equipo = input("Equipo: ")
                create_entrenadores(id, equipo)
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            input("ENTER para continuar...")

        elif opcion == "2":
            os.system("cls")
            read_entrenadores()
            input("ENTER para continuar...")

        elif opcion == "3":
            os.system("cls")
            print("\n--- Modificar Entrenador ---")
            id = input("ID del Entrenador a modificar: ")
            print("[Deje en blanco si no desea modificar el campo]")
            
            equipo = input("Nuevo Equipo: ")
            equipo = equipo if len(equipo.strip()) > 0 else None

            update_entrenador(id, equipo)
            input("ENTER para continuar...")

        elif opcion == "4":
            os.system("cls")
            id = input("ID del Entrenador a eliminar: ")
            delete_entrenador(id)
            input("ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def menu_jueces():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |          Menu: Jueces            |
                |----------------------------------|
                | 1. Registrar Juez                |
                | 2. Listar Jueces                 |
                | 3. Modificar Juez                |
                | 4. Eliminar Juez                 |
                | 0. Volver                        |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            print("\n--- Crear Juez ---")
            try:
                id = int(input("ID Juez: "))
                especialidad = input("Especialidad: ")
                create_jueces(id, especialidad)
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            input("ENTER para continuar...")

        elif opcion == "2":
            os.system("cls")
            read_jueces()
            input("ENTER para continuar...")

        elif opcion == "3":
            os.system("cls")
            print("\n--- Modificar Juez ---")
            id = input("ID del Juez a modificar: ")
            print("[Deje en blanco si no desea modificar el campo]")
            
            especialidad = input("Nueva Especialidad: ")
            especialidad = especialidad if len(especialidad.strip()) > 0 else None

            update_juez(id, especialidad)
            input("ENTER para continuar...")

        elif opcion == "4":
            os.system("cls")
            id = input("ID del Juez a eliminar: ")
            delete_juez(id)
            input("ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def main():
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
                ====================================
                |    SISTEMA DE GESTIÓN DEPORTIVA  |
                |----------------------------------|
                | 1. Inicializar BD (Crear Tablas) |
                | 2. Gestionar Eventos             |
                | 3. Gestionar Participantes       |
                | 4. Gestionar Atletas             |
                | 5. Gestionar Entrenadores        |
                | 6. Gestionar Jueces              |
                | 0. Salir                         |
                ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            create_all_tables()
            input("Tablas verificadas. ENTER para continuar...")
        elif opcion == "2":
            os.system("cls")
            menu_eventos()
        elif opcion == "3":
            os.system("cls")
            menu_participantes()
        elif opcion == "4":
            os.system("cls")
            menu_atletas()
        elif opcion == "5":
            os.system("cls")
            menu_entrenadores()
        elif opcion == "6":
            os.system("cls")
            menu_jueces()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            input("Opción inválida. ENTER para continuar.")

if __name__ == "__main__":
    main()