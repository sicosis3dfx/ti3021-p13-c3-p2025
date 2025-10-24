"""
CRUD
---
CREATE : crear un nuevo registro
Read: Leer registro/s
Update: Actualizar un registro existente
Delete: Eliminar un registro existente
"""
"""
Glorasario
----
* pass
Palabra reservada para que Python no exija el mínimo necesario para el funcionamiento de la funcion/metodo.

* IDE
Viene de la palabra Integrated Development Environment que significa Entorno de Desarrollo Integrado, que son 
los editores de código que normalmente usamos para programar en informática.

* lint o linter
Es el encargado de vigilar que la sintaxis del código IDE sea correcta y te sugiere
en funcion de este.
"""
from datetime import date

# Primero, debemos crear una clase
class Persona:
    #Definir como se inicializa
    def __init__(
            self,
            rut,
            digito_verificador: str,
            nombres: str,
            apellido: str,
            fecha_nacimiento: date,
            cod_area: int,
            telefono: int
    ):
        
        self.rut: int = rut
        self.digito_verificador: str = digito_verificador
        self.nombres: str = nombres
        self.apellidos: str = apellido
        self.fecha_nacimiento: date = fecha_nacimiento
        self.cod_area: int = cod_area
        self.telefono: int = telefono    

# Creamos una lista para almacenar varios objetos instanciados de la clase Persona
personas: list [Persona] = []


def persona_existente(nueva_persona: Persona) -> bool:
    for persona in personas:
        if persona.rut == nueva_persona.rut:
            print(f"La persona con rut: {persona.rut}-{persona.digito_verificador}.")


    print("Persona no existente.")
    return True

def create_persona():
    rut = int(input("Ingrese el RUT (sin dígito verificador): "))
    digito_verificador = input("Ingrese el dígito verificador: ")
    nombres = input("Ingrese los nombres: ")
    apellidos = input("Ingrese los apellidos: ")
    dia_nacimiento = int(input("Ingrese el día de nacimiento (1-31): "))
    mes_nacimiento = int(input("Ingrese el mes de nacimiento (1-12): "))
    anio_nacimiento = int(input("Ingrese el año de nacimiento (YYYY): "))
    fecha_nacimiento_input: date = date("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
    cod_area = int(input("Ingrese el código de área: "))
    telefono = int(input("Ingrese el número de teléfono: ")) 
    
    nueva_persona = Persona(
        rut,
        digito_verificador,
        nombres,
        apellidos,
        fecha_nacimiento_input,
        cod_area,
        telefono
    )

    if persona_existente(nueva_persona: Persona) -> bool:
        for persona in personas:
            if persona.rut == nueva_persona.rut:
                print(f"Persona ya existente con rut: {persona.rut}-{persona.digito_verificador}")
                return True
            
        print("Persona ya existente.")
        return False
        

def read_persona():
    pass    

def update_persona():
    pass  

def delete_persona():
    pass

create_persona()
print