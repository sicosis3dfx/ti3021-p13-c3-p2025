# Menú sin login
def menu_indicadores(finance_app):
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        
        print(
            """
            ====================================
            |          Menu: Opciones          |
            |----------------------------------|
            | 1. Consultar UF                  |
            | 2. Consultar Dólar (USD)         |
            | 3. Consultar Euro                |
            | 4. Consultar UTM (Mensual)       |
            | 5. Consultar IPC (Mensual)       |
            | 6. Consultar IVP                 |
            | 0. Salir                         |
            ====================================
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

# Menú solo mediante Login
def menu_indicadores(finance_app):
    """Menú secundario: Solo accesible tras login"""
    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
            ====================================
            |       Menu: Indicadores          |
            |----------------------------------|
            | 1. Consultar UF                  |
            | 2. Consultar Dólar (USD)         |
            | 3. Consultar Euro                |
            | 4. Consultar UTM (Mensual)       |
            | 5. Consultar IPC (Mensual)       |
            | 0. Cerrar Sesión (Volver)        |
            ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("\n--- Valor UF ---")
            finance_app.get_uf()
            input("\nPresione ENTER para continuar...")
        
        elif opcion == "2":
            print("\n--- Valor Dólar ---")
            finance_app.get_usd()
            input("\nPresione ENTER para continuar...")

        elif opcion == "3":
            print("\n--- Valor Euro ---")
            finance_app.get_eur()
            input("\nPresione ENTER para continuar...")

        elif opcion == "4":
            print("\n--- Valor UTM ---")
            finance_app.get_utm()
            input("\nPresione ENTER para continuar...")

        elif opcion == "5":
            print("\n--- Valor IPC ---")
            finance_app.get_ipc()
            input("\nPresione ENTER para continuar...")

        elif opcion == "0":
            break
        else:
            input("Opción inválida. ENTER para continuar.")

def main():
    # Inicializamos la DB y la App Financiera una sola vez
    db = Database(username, password, dsn)
    finance_app = Finance()

    while True:
        os.system("cls" if os.name == 'nt' else 'clear')
        print(
            """
            ====================================
            |     SISTEMA DE FINANZAS          |
            |----------------------------------|
            | 1. Iniciar Sesión                |
            | 2. Registrarse                   |
            | 0. Salir                         |
            ====================================
            """
        )
        opcion = input("Elige una opción: ")

        if opcion == "1":
            os.system("cls")
            print("\n--- Iniciar Sesión ---")
            u = input("Usuario: ")
            p = input("Contraseña: ")
            
            if Auth.login(db, u, p):
                input("\nLogin Correcto. Presione ENTER para ir al sistema...")
                # Aquí derivamos al menú secundario
                menu_indicadores(finance_app)
            else:
                print("\nError: Usuario o contraseña incorrectos.")
                input("Presione ENTER para intentar de nuevo...")

        elif opcion == "2":
            os.system("cls")
            print("\n--- Registro de Usuario ---")
            u = input("Nuevo Usuario: ")
            p = input("Nueva Contraseña: ")
            # Llamamos al metodo de registro
            Auth.register(db, u, p)
            input("Presione ENTER para continuar...")

        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            input("Opción inválida. ENTER para continuar.")

if __name__ == "__main__":
    main()