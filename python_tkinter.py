#OBLIGATORIO: Importar librería tkinter
from tkinter import *
from tkinter import ttk
# OBTENER RUTA DEL SCRIPT DE PYTHON
import os       

#Ruta de script
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

#OBLIGATORIO: Inicializar TKINTER
root: Tk = Tk()

#onfiguracion general
root.title("")
icon = PhotoImage(
        file=os.path.join(script_dir, "icon.png")
    )
root.iconphoto( True, icon )


#Crear Un lienzo. Contexto, estilizacion
frame1: Frame = ttk.Frame( root, padding=10 )

# OBLIGATORIO: Manter el ciclo de vida de TKINTER
root.mainloop()