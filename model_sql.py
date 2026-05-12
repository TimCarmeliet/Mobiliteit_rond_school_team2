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

    # tabel voor verplaatsingen gelinkt aan student en transport
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


# STUDENTS

# voegt een nieuwe student toe
def add_student(naam, klas, afstand):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Students (naam, klas, afstand)
                      VALUES (?, ?, ?)''', (naam, klas, afstand))

    conn.commit()
    conn.close()

# geeft alle studenten terug
def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()

    conn.close()
    return students

# geeft één student terug op basis van id
def get_student_by_id(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Students WHERE id = ?', (student_id,))
    student = cursor.fetchone()

    conn.close()
    return student

# past gegevens van een bestaande student aan
def update_student(student_id, naam, klas, afstand):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''UPDATE Students
                      SET naam = ?, klas = ?, afstand = ?
                      WHERE id = ?''', (naam, klas, afstand, student_id))

    conn.commit()
    conn.close()

# verwijdert een student en zijn bijhorende verplaatsingen
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # verwijder eerst de mobility logs van deze student
    cursor.execute('DELETE FROM Mobility_log WHERE student_id = ?', (student_id,))

    # verwijder dan pas de student zelf
    cursor.execute('DELETE FROM Students WHERE id = ?', (student_id,))

    conn.commit()
    conn.close()
 
    
# TRANSPORT

# voegt een nieuw vervoersmiddel toe
def add_transport(type):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Transport (type) VALUES (?)', (type,))

    conn.commit()
    conn.close()

# geeft alle vervoersmiddelen terug
def get_all_transport():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Transport')
    transport = cursor.fetchall()

    conn.close()
    return transport

# verwijdert een vervoersmiddel en zijn bijhorende verplaatsingen
def delete_transport(transport_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # verwijder eerst de mobility logs met dit transport
    cursor.execute('DELETE FROM Mobility_log WHERE transport_id = ?', (transport_id,))

    # verwijder dan pas het vervoersmiddel zelf
    cursor.execute('DELETE FROM Transport WHERE id = ?', (transport_id,))

    conn.commit()
    conn.close()