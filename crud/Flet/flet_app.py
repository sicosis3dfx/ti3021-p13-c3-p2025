# 1. paso: Importar la biblioteca Flet
import flet as ft

# 2. paso: Clase principal de la aplicación
class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola Mundo"
        # Siempre como ultima linea de __init__ llamar a
        self.build()
    # Metodo principal para agregar elementos a la pagina/aplicacion
    def build(self):
        self.page.add(
            ft.Text(value ="Hola Mundo")
        )
# 3. paso: Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=App)