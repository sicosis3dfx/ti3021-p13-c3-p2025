class Evento:
    def __init__(self, Nombre: str, IdEvento: int, Fecha: str, Lugar: str):
        self._nombre: str = Nombre
        self._idevento: int = IdEvento
        self._fecha: int = Fecha
        self._lugar: str = Lugar

class Participante:
    def __init__(self, Nombre: str, Rut: str, IdParticipante: int, Edad: int, NumeroInscripcion: int):
        self._nombre: str = Nombre
        self._rut: str = Rut
        self._idparticipante: int = IdParticipante
        self._edad: int = Edad
        self._numeroinscripcion: int = NumeroInscripcion

class Atleta:
    def __init__(self, Disciplina: str, Marca: float):
        self._disciplina: str = Disciplina
        self._marca: float = Marca  
        
class Entrenador:
    def __init__(self, Equipo: str):
        self._equipo: str = Equipo
        
class Juez:
    def __init__(self, Especialidad: str):  
        self._especialidad: str = Especialidad
        