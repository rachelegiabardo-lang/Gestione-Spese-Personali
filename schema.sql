CREATE TABLE Categorie (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT UNIQUE NOT NULL
);

CREATE TABLE Spese (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Data TEXT NOT NULL,
    Importo REAL NOT NULL CHECK (Importo > 0),
    ID_Categoria INTEGER NOT NULL,
    Descrizione TEXT,
    FOREIGN KEY (ID_Categoria) REFERENCES Categorie(ID)
);

CREATE TABLE Budget (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Mese TEXT NOT NULL,
    Importo REAL NOT NULL CHECK (Importo > 0),
    ID_Categoria INTEGER NOT NULL,
    UNIQUE(Mese, ID_Categoria),
    FOREIGN KEY (ID_Categoria) REFERENCES Categorie(ID)
);

-- Inserimento dati iniziali
INSERT INTO Categorie (Nome) VALUES ('Svago'), ('Alimentari');

INSERT INTO Budget (Mese, Importo, ID_Categoria) 
VALUES ('2026-05', 20.00, 1);

INSERT INTO Spese (Data, Importo, ID_Categoria, Descrizione) 
VALUES ('2026-05-12', 34.98, 1, 'Cinema');