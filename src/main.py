import sqlite3

# Funzione per connettersi al database
def connect_db():
    return sqlite3.connect('spese_personali.db')

# MODULO 0: Setup iniziale e creazione tabelle con vincoli obbligatori
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    # Tabella Categorie
    cursor.execute('''CREATE TABLE IF NOT EXISTS Categorie (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Nome TEXT UNIQUE NOT NULL)''')
    # Tabella Spese con vincoli CHECK e FOREIGN KEY
    cursor.execute('''CREATE TABLE IF NOT EXISTS Spese (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Data TEXT NOT NULL,
                        Importo REAL NOT NULL CHECK (Importo > 0),
                        ID_Categoria INTEGER NOT NULL,
                        Descrizione TEXT,
                        FOREIGN KEY (ID_Categoria) REFERENCES Categorie(ID))''')
    # Tabella Budget con vincolo UNIQUE per mese/categoria
    cursor.execute('''CREATE TABLE IF NOT EXISTS Budget (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Mese TEXT NOT NULL,
                        Importo REAL NOT NULL CHECK (Importo > 0),
                        ID_Categoria INTEGER NOT NULL,
                        UNIQUE(Mese, ID_Categoria),
                        FOREIGN KEY (ID_Categoria) REFERENCES Categorie(ID))''')
    conn.commit()
    conn.close()

# MODULO 1: Gestione delle Categorie 
def gestione_categorie():
    nome = input("Inserisci il nome della categoria: ").strip()
    if not nome:
        print("Errore: il nome non può essere vuoto.")
        return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Categorie (Nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")
    except sqlite3.IntegrityError:
        print("Errore: La categoria esiste già.")
    conn.close()

# MODULO 2: Inserimento di una Spesa 
def inserisci_spesa():
    data = input("Data (YYYY-MM-DD): ")
    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print("Errore: l'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return
    
    categoria = input("Nome della categoria: ")
    descrizione = input("Descrizione facoltativa: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM Categorie WHERE Nome = ?", (categoria,))
    res = cursor.fetchone()
    
    if res:
        cursor.execute("INSERT INTO Spese (Data, Importo, ID_Categoria, Descrizione) VALUES (?, ?, ?, ?)",
                       (data, importo, res[0], descrizione))
        conn.commit()
        print("Spesa inserita correttamente.")
    else:
        print("Errore: la categoria non esiste.")
    conn.close()

# MODULO 3: Definizione del Budget Mensile 
def definisci_budget():
    mese = input("Mese (YYYY-MM): ")
    categoria = input("Nome della categoria: ")
    try:
        importo = float(input("Importo del budget: "))
        if importo <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Inserire un numero valido.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM Categorie WHERE Nome = ?", (categoria,))
    res = cursor.fetchone()
    
    if res:
        cursor.execute("INSERT OR REPLACE INTO Budget (Mese, Importo, ID_Categoria) VALUES (?, ?, ?)",
                       (mese, importo, res[0]))
        conn.commit()
        print("Budget mensile salvato correttamente.")
    else:
        print("Errore: la categoria non esiste.")
    conn.close()

# MODULO 4: Visualizzazione Report con Sottomenu 
def visualizza_report():
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        
        scelta = input("Scelta: ")
        conn = connect_db()
        cursor = conn.cursor()

        if scelta == '1':
            cursor.execute('''SELECT C.Nome, SUM(S.Importo) 
                              FROM Spese S JOIN Categorie C ON S.ID_Categoria = C.ID 
                              GROUP BY C.Nome''')
            print("\nCategoria.. ..Totale Speso")
            for row in cursor.fetchall():
                print(f"{row[0]}.......{row[1]:.2f}")
        
        elif scelta == '2':
            mese = input("Inserisci mese (YYYY-MM): ")
            cursor.execute('''SELECT C.Nome, B.Importo, SUM(S.Importo)
                              FROM Budget B 
                              JOIN Categorie C ON B.ID_Categoria = C.ID
                              LEFT JOIN Spese S ON S.ID_Categoria = C.ID AND S.Data LIKE ?
                              WHERE B.Mese = ?
                              GROUP BY C.Nome''', (f"{mese}%", mese))
            results = cursor.fetchall()
            if not results:
                print("Nessun budget o spesa trovata per questo mese.")
            for row in results:
                speso = row[2] if row[2] else 0
                stato = "SUPERAMENTO BUDGET" if speso > row[1] else "OK"
                print(f"\nMese: {mese}\nCategoria: {row[0]}\nBudget: {row[1]}\nSpeso: {speso}\nStato: {stato}")

        elif scelta == '3':
            # Implementazione del Report 3: Elenco ordinato per data 
            cursor.execute('''SELECT S.Data, C.Nome, S.Importo, S.Descrizione 
                              FROM Spese S JOIN Categorie C ON S.ID_Categoria = C.ID 
                              ORDER BY S.Data ASC''')
            print("\nData       | Categoria  | Importo | Descrizione")
            print("-" * 50)
            for row in cursor.fetchall():
                print(f"{row[0]} | {row[1]:<10} | {row[2]:>7.2f} | {row[3]}")

        elif scelta == '4':
            conn.close()
            break
        else:
            print("Scelta non valida.")
        conn.close()

# MENU PRINCIPALE [cite: 4, 5]
def main():
    setup_db()
    print("BENVENUTO NEL SISTEMA GESTIONE SPESE")
    while True:
        print("\n--- SISTEMA SPESE PERSONALI ---")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        
        scelta = input("Inserisci la tua scelta: ")

        if scelta == '1': gestione_categorie()
        elif scelta == '2': inserisci_spesa()
        elif scelta == '3': definisci_budget()
        elif scelta == '4': visualizza_report()
        elif scelta == '5': 
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprovare.")

if __name__ == "__main__":
    main()
