from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
import flet as ft
import os

class App:
    def __init__ (self, page: ft.Page):
        self.page = page
        self.page.title = "EcoTech Solutions"
        self.db = Database(
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        ) 
        try:
            self.db.create_all_tables()
        except Exception as error:
            print(f"Error al crear las tablas: {error}")
        
        self.page_register()
    
    def page_register(self):
        self.page.controls.clear()
        
        self.input_id = ft.TextField( 
            label="Ingrese su ID",
            hint_text="Ingresa el número de ID del Usuario"
            )
        self.input_username = ft.TextField( 
            label="Ingrese su Nombre de Usuario",
            hint_text="Ingresa tu nombre de usuario"
            )
        self.input_password = ft.TextField( 
            label="Ingrese su Contraseña",
            hint_text="Ingresa tu contraseña",
            password=True,
            can_reveal_password=True
            )
        self.button_register = ft.Button( 
            text="Registrar",
            on_click=self.handle_register 
            )
        self.text_status = ft.Text( 
            value="" 
        )
        self.text_login = ft.Text(
            value="¿Ya tienes una cuenta? Inicia sesión aquí.",
        )
        self.button_login = ft.TextButton(
            text="Iniciar Sesión",
            on_click=lambda e: self.page_login()
        )

        self.page.add(
            self.input_id,
            self.input_username,
            self.input_password,
            self.button_register,
            self.text_status,
            self.text_login,
            self.button_login
        )
        
        self.page.update()

    def handle_register(self, e):
        try:
            id_usuario = (self.input_id.value or "").strip()
            username = (self.input_username.value or "").strip()
            password = (self.input_password.value or "").strip()
        
            status = Auth.register(
                db=self.db,
                id=id_usuario,
                username=username,
                password=password
            )
            self.text_status.value = f"{ status['message'] }"
            self.page.update()

        except ValueError:
            self.text_status.value = "El ID solo puede contener numeros"
            self.page.update()
    
    def page_login(self):
        self.page.controls.clear()
        # CODIGO DE LOGIN DE USUARIOS
        self.page.update()
    
    def page_main_menu(self):
        self.page.controls.clear()
        # CODIGO DEL MENU PRINCIPAL
        self.page.update()

    def page_indicator_menu(self):
        self.page.controls.clear()
        # CODIGO DEL MENU DE INDICADORES
        self.page.update()
    
    def page_history_menu(self):
        self.page.controls.clear()
        # CODIGO DEL MENU DE HISTORIAL
        self.page.update()

if __name__ == "__main__":
    load_dotenv()
    ft.app(target=App)