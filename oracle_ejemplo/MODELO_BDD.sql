
            CREATE TABLE Eventos (
                idevento INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                fecha DATE,
                lugar VARCHAR(50)
            )

            CREATE TABLE Participantes (
                idparticipante INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                rut VARCHAR(10) UNIQUE,
                edad INTEGER,
                numeroinscripcion INTEGER
            )

            CREATE TABLE Atletas (
                idparticipante INTEGER PRIMARY KEY,
                disciplina TEXT,
                marca NUMERIC,
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            )

            CREATE TABLE Entrenadores (
                identrenador INTEGER PRIMARY KEY,
                equipo VARCHAR(50)
            )

            CREATE TABLE Jueces (
                idjuez INTEGER PRIMARY KEY,
                especialidad VARCHAR (50)
            )

            CREATE TABLE Inscripciones (
                idevento INTEGER,
                idparticipante INTEGER,
                PRIMARY KEY (idevento, idparticipante),
                FOREIGN KEY (idevento) REFERENCES Evento(idevento),
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            )