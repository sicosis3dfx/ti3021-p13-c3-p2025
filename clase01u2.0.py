class Evento:
    def __init__(self, nombre: str, idevento: int, fecha: str, lugar: str):
        self._nombre: str = nombre
        self._idevento: int = idevento
        self._fecha: int = fecha
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



evento1 : Evento = Evento("Juegos Olimpicos", 1, "2024-07-26", "Paris")
participante1 : Participante = Participante("Juan Perez", "12345678-9", 1, 25, 1001)
participante2 : Participante = Participante("Pedro Pérez", "12564897-8", 2, 23, 1002)
atleta1 : Atleta = Atleta("100m planos", 9.58)
entrenador1 : Entrenador = Entrenador("Equipo Nacional")
juez1 : Juez = Juez("Atletismo")
print("")
print(f"Participante: {participante1.nombre}, Rut: {participante1.rut}, ID único: {participante1._idparticipante}, Edad: {participante1.edad}, Inscripción Nº: {participante1._numeroinscripcion}")
print("")
print(f"Participante: {participante2.nombre}, Rut: {participante2.rut}, ID único: {participante2._idparticipante}, Edad: {participante2.edad}, Inscripción Nº: {participante2._numeroinscripcion}")
print("")
print(f"Evento: {evento1.nombre}, ID único: {evento1._idevento}, Fecha: {evento1._fecha}, Lugar: {evento1._lugar}")
print("")
print(f"Atleta: {atleta1.disciplina}, Disciplina: {atleta1.disciplina}, Marca: {atleta1.marca} segundos")
print("")
print(f"Entrenador: {entrenador1.equipo}")
print("")
print(f"Juez: {juez1.especialidad}")
print("")