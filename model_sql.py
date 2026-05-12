import sqlite3

SCHOOL_DATA = 'school.db'

def get_db_connection():
    conn = sqlite3.connect(SCHOOL_DATA, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# maakt tabellen aan
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # tabel voor studenten
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naam TEXT NOT NULL,
        klas TEXT NOT NULL,
        afstand REAL NOT NULL
    )''')

    # tabel voor vervoersmiddelen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL
    )''')

    # tabel voor verplaatsingen, gelinkt aan student en transport
    cursor.execute('''CREATE TABLE IF NOT EXISTS Mobility_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        transport_id INTEGER NOT NULL,
        datum TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(id),
        FOREIGN KEY (transport_id) REFERENCES Transport(id)
    )''')

    conn.commit()
    conn.close()
