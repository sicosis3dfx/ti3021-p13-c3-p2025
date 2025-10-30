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

    def __str__(self):
        return f"""
                Rut: {self} - {self.digito_verificador}
                Nombre Completo: {self.nombres} {self.apeliidos}
                Fecha de nacimiento: {self.fecha_nacimiento}
                Numero de telefono: +{self.cod_area} {self.telefono}
                """

# Creamos una lista para almacenar varios objetos instanciados de la clase Persona
personas: list [Persona] = []


def persona_existente(nueva_persona: Persona) -> bool:
    for persona in personas:
        if persona.rut == nueva_persona.rut:
            print(f"La persona con rut: {persona.rut}-{persona.digito_verificador}.")
            return True

    print("Persona no existente.")
    return False

def create_persona():
    rut = int(input("Ingrese el RUT (sin dígito verificador): "))
    digito_verificador = input("Ingrese el dígito verificador: ")
    nombres = input("Ingrese los nombres: ")
    apellidos = input("Ingrese los apellidos: ")

    dia_nacimiento: int = int(input("Ingresa el día de nacimiento de la persona: "))
    mes_nacimiento: int = int(input("Ingresa el mes de nacimiento de la persona: "))    
    anio_nacimiento: int = int(input("Ingresa el año de nacimiento de la persona: "))
    fecha_nacimiento: date = date(
        year=anio_nacimiento,
        month=mes_nacimiento,
        day=dia_nacimiento
    )

    cod_area = int(input("Ingrese el código de área: "))
    telefono = int(input("Ingrese el número de teléfono: ")) 
    
    nueva_persona = Persona(
        rut,
        digito_verificador,
        nombres,
        apellidos,
        fecha_nacimiento,
        cod_area,
        telefono
    )

    if persona_existente(nueva_persona):
        for persona in personas:
            if persona.rut == nueva_persona.rut:
                print(f"Persona ya existente con rut: {persona.rut}-{persona.digito_verificador}")
                return True
            
        print("Persona ya existente.")
        return False
        

def read_persona():
    for persona in personas:
        print("="*20)
        print(persona)   
        print("="*20)

def update_persona(rut:int):
    rut_busqueda = int(input("Ingresa el rut sin digito verificador (Ej: 12345678): "))
    for persona in personas:
        if persona.rut == rut_busqueda:
            while True:
                print(
                    f"""
                    =============================
                    ||   Edición de personas   ||
                    =============================
                    1. Rut: {persona.rut}
                    2. Digito verificador {persona.digito_verificador}
                    3. Nombres: {persona.nombres}
                    4. Apellidos: {persona.apellidos}
                    5. Fecha de Nacimiento: {persona.fecha_nacimiento}
                    6. Codigo de Area {persona.cod_area}
                    7. Telefono: {persona.telefono}
                    0. No seguir modificando.
                    """
                )
                
                opcion = input("¿Qué datos quieres modifiar?")

                if opcion == "1":
                    rut: int = int(input("Ingresa el rut de la persona): "))
                    for persona in personas:
                        if persona.rut == rut:
                            print(f"La persona con el rut {persona.rut} ya existe. Intente con otro rut.")
                        else:
                            persona.rut = rut
                            print("Rut modificado correctamente.")
                elif opcion == "2":
                    digito_verificador: str = input("Ingresa el nuevo dígito verificador: ")
                    persona.digito_verificador = digito_verificador
                    print("Dígito verificador modificado correctamente.")
                elif opcion == "3":
                    nombres: str = input("Ingresa los nuevos nombres: ")
                    persona.nombres = nombres
                    print("Nombres modificados correctamente.") 
                elif opcion == "4":
                    apellidos: str = input("Ingresa los nuevos apellidos: ")
                    persona.apellidos = apellidos
                    print("Apellidos modificados correctamente.")
                elif opcion == "5":
                    dia_nacimiento: int = int(input("Ingresa el día de nacimiento de la persona: "))
                    mes_nacimiento: int = int(input("Ingresa el mes de nacimiento de la persona: "))    
                    anio_nacimiento: int = int(input("Ingresa el año de nacimiento de la persona: "))
                    fecha_nacimiento: date = date(
                        year=anio_nacimiento,
                        month=mes_nacimiento,
                        day=dia_nacimiento
                    )
                    persona.fecha_nacimiento = fecha_nacimiento
                    print("Fecha de nacimiento modificada correctamente.")
                
                elif opcion == "6":
                    cod_area: int = int(input("Ingresa el nuevo código de área: "))
                    persona.cod_area = cod_area
                    print("Código de área modificado correctamente.")
                
                elif opcion == "7":
                    telefono: int = int(input("Ingresa el nuevo número de teléfono: "))
                    persona.telefono = telefono
                    print("Número de teléfono modificado correctamente.")
                
                elif opcion == "0":
                    print("Modificación finalizada.")
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")
                    input("Presione Enter para continuar...")

    print(f"Persona con rut {rut_busqueda}, no encontrada. ")
    input("Presione Enter para continuar...")
                    
                    
def delete_persona():
    rut_busqueda = int(input("Ingresa el rut sin digito verificador (Ej: 12345678): ")) 
    for persona in personas:
        if rut_busqueda == persona.rut:
            print(f"Eliminando a persoa con datos : {persona}")
            personas.remove(persona)
            print(f"Persona con rut {rut_busqueda} eliminada correctamente.")
            return
while True:
    print(
        """
        =============================
        ||   Gestión de Personas   ||
        =============================
        1. Crear Persona
        2. Leer Personas
        3. Actualizar Persona
        4. Eliminar Persona
        0. Salir
        """
    )

    opcion = input("Seleccione una opción [1-4,0]: ")
    if opcion == "1":
        create_persona()
    elif opcion == "2":
        read_persona()
    elif opcion == "3":
        update_persona()
    elif opcion == "4":
        delete_persona()
    elif opcion == "0":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intente nuevamente.")
        input("Presione Enter para continuar...")

create_persona()
print