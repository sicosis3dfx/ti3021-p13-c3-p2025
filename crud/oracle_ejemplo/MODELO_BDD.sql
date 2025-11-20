
            CREATE TABLE Evento (
                idevento INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                fecha DATE,
                lugar VARCHAR(50)
            )

            CREATE TABLE Participante (
                idparticipante INTEGER PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                rut VARCHAR(10) UNIQUE,
                edad INTEGER,
                numeroinscripcion INTEGER
            )

            CREATE TABLE Atleta (
                idparticipante INTEGER PRIMARY KEY,
                disciplina TEXT,
                marca NUMERIC,
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            )

            CREATE TABLE Entrenador (
                identrenador INTEGER PRIMARY KEY,
                equipo VARCHAR(50)
            )

            CREATE TABLE Juez (
                idjuez INTEGER PRIMARY KEY,
                especialidad VARCHAR (50)
            )

            CREATE TABLE Inscripcion (
                idevento INTEGER,
                idparticipante INTEGER,
                PRIMARY KEY (idevento, idparticipante),
                FOREIGN KEY (idevento) REFERENCES Evento(idevento),
                FOREIGN KEY (idparticipante) REFERENCES Participante(idparticipante)
            )