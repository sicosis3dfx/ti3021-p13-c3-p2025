class Evento:
    def __init__(self, nombre: str, idevento: int, fecha: str, lugar: str):
        self._nombre: str = nombre
        self._idevento: int = idevento
        self._fecha: str = fecha
        self._lugar: str = lugar

    @property
    def nombre(self) -> str:
        return self._nombre

class Participante:
    def __init__(self, nombre: str, rut: str, idparticipante: int, edad: int, numeroinscripcion: int):
        self._nombre: str = nombre
        self._rut: str = rut
        self._idparticipante: int = idparticipante
        self._edad: int = edad
        self._numeroinscripcion: int = numeroinscripcion

    @property
    def nombre(self) -> str:        
        return self._nombre
    @property
    def rut(self) -> str:        
        return self._rut
    @property
    def edad(self) -> int:        
        return self._edad

class Atleta:
    def __init__(self, disciplina: str, marca: float):
        self._disciplina: str = disciplina
        self._marca: float = marca  
    @property
    def disciplina(self) -> str:
        return self._disciplina
    @property
    def marca(self) -> float:
        return self._marca
        
class Entrenador:
    def __init__(self, equipo: str):
        self._equipo: str = equipo
    @property
    def equipo(self) -> str:
        return self._equipo
        
class Juez:
    def __init__(self, especialidad: str):  
        self._especialidad: str = especialidad
    @property
    def especialidad(self) -> str:
        return self._especialidad

evento1 : Evento = Evento("Juegos Olimpicos", 1, "26-07-2024", "Paris")
participante1 : Participante = Participante("Juan Perez", "18389678-3", 1, 25, 1001)
participante2 : Participante = Participante("Pedro González", "17542897-8", 2, 23, 1002)
participante3 : Participante = Participante("Fernando Peña", "16224893-9", 3, 24, 1003)
participante4 : Participante = Participante("Hugo Morales", "16556891-8", 4, 24, 1004)
participante5 : Participante = Participante("Jaime Améstica", "17264877-6", 5, 25, 1005)
participante6 : Participante = Participante("Jorge Romero ", "18224227-K", 6, 23, 1006)
atleta1 : Atleta = Atleta("100m planos", 9.58)
entrenador1 : Entrenador = Entrenador("Equipo Nacional")
juez1 : Juez = Juez("Atletismo")
print()
print("----- Datos del Evento y Participantes -----")
print(f"Participante: {participante1.nombre}, Rut: {participante1.rut}, ID único: {participante1._idparticipante}, Edad: {participante1.edad}, Inscripción Nº: {participante1._numeroinscripcion}")
print(f"Participante: {participante2.nombre}, Rut: {participante2.rut}, ID único: {participante2._idparticipante}, Edad: {participante2.edad}, Inscripción Nº: {participante2._numeroinscripcion}")
print(f"Participante: {participante3.nombre}, Rut: {participante3.rut}, ID único: {participante3._idparticipante}, Edad: {participante3.edad}, Inscripción Nº: {participante3._numeroinscripcion}")
print(f"Participante: {participante4.nombre}, Rut: {participante4.rut}, ID único: {participante4._idparticipante}, Edad: {participante4.edad}, Inscripción Nº: {participante4._numeroinscripcion}")
print(f"Participante: {participante5.nombre}, Rut: {participante5.rut}, ID único: {participante5._idparticipante}, Edad: {participante5.edad}, Inscripción Nº: {participante5._numeroinscripcion}")
print(f"Participante: {participante6.nombre}, Rut: {participante6.rut}, ID único: {participante6._idparticipante}, Edad: {participante6.edad}, Inscripción Nº: {participante6._numeroinscripcion}")
print(f"Evento: {evento1.nombre}, ID único: {evento1._idevento}, Fecha: {evento1._fecha}, Lugar: {evento1._lugar}")
print(f"Atleta: {atleta1.disciplina}, Disciplina: {atleta1.disciplina}, Marca: {atleta1.marca} segundos")
print(f"Entrenador: {entrenador1.equipo}")
print(f"Juez: {juez1.especialidad}")
print("----- Fin de los Datos -----\n")