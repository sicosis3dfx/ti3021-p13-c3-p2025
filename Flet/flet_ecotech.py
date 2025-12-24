from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
import flet as ft
import os

load_dotenv()


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Solutions"
        self.db = Database(
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )

        try:
            self.db.create_all_tables()
        except Exception as error:
            print(f"{error}")

        self.loged_user = ""

        self.page_register()

    def page_register(self):
        self.page.controls.clear()

        self.input_id = ft.TextField(
            label="ID del usuario",
            hint_text="Ingresa un número para el ID del usuario"
        )
        self.input_username = ft.TextField(
            label="Nombre de usuario",
            hint_text="Ingresa un nombre de usuario"
        )
        self.input_password = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa una contraseña",
            password=True,
            can_reveal_password=True
        )
        self.button_register = ft.Button(
            text="Registrarse",
            on_click=self.handle_register
        )
        self.text_status = ft.Text(
            value=""
        )
        self.text_login = ft.Text(
            value="¿Ya tienes una cuenta?"
        )
        self.button_login = ft.Button(
            text="Inicia sesión",
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
            id_user = int((self.input_id.value or "").strip())
            username = (self.input_username.value or "").strip()
            password = (self.input_password.value or "").strip()

            status = Auth.register(db=self.db,
                                   id=id_user,
                                   username=username,
                                   password=password)

            self.text_status.value = f"{status["message"]}"
            self.page.update()

        except ValueError:
            self.text_status.value = "ID sólo debe de ser númerico"
            self.page.update()

    def page_login(self):
        self.page.controls.clear()

        self.input_username = ft.TextField(
            label="Nombre de usuario",
            hint_text="Ingresa tu nombre de usuario"
        )
        self.input_password = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            password=True,
            can_reveal_password=True
        )
        self.button_login = ft.Button(
            text="Iniciar sesión",
            on_click=self.handle_login
        )
        self.text_status = ft.Text(
            value=""
        )

        self.text_register = ft.Text(
            value="¿Aún no tienes cuenta?"
        )
        self.button_register = ft.Button(
            text="Registrate",
            on_click=lambda e: self.page_register()
        )

        self.page.add(
            self.input_username,
            self.input_password,
            self.button_login,
            self.text_status,
            self.text_register,
            self.button_register
        )

        self.page.update()

    def handle_login(self, e):
        username = (self.input_username.value or "").strip()
        password = (self.input_password.value or "").strip()

        status = Auth.login(db=self.db,
                            username=username,
                            password=password)

        self.text_status.value = status["message"]
        self.page.update()

        if status["success"]:
            self.loged_user = username
            self.page_main_menu()

    def page_main_menu(self):
        self.page.controls.clear()
        
        self.text_title_main_menu = ft.Text(
            value="Main Menu",
            color="#cc0000",
            size=32,
            weight=ft.FontWeight("bold")
        )
        self.text_welcome = ft.Text(
            value=f"Hola {self.loged_user}"
        )
        self.button_indicators = ft.Button(
            text="Consultar Indicadores",
            on_click= lambda e: self.page_indicator_menu()
        )
        self.button_history = ft.Button(
            text="Historial de consultas",
            on_click= lambda e: self.page_history_menu()
        )
        self.button_logout = ft.Button(
            text="Cerrar sesión",
            on_click= lambda e: self.page_login()
        )
        self.page.add(
            self.text_title_main_menu,
            self.text_welcome,
            self.button_indicators,
            self.button_history,
            self.button_logout
        )

        self.page.update()

    def page_indicator_menu(self):
        self.page.controls.clear()
        # CODIGO
        self.page.update()

    def page_history_menu(self):
        self.page.controls.clear()
        # CODIGO
        self.page.update()


if __name__ == "__main__":
    ft.app(target=App)