import sqlite3

class Model:
    def __init__(self):
        self.conn = sqlite3.connect("school.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naam TEXT,
            klas TEXT,
            afstand REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mobility_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            transport_id INTEGER,
            datum TEXT
        )
        """)

        self.conn.commit()

    # STUDENTS
    def add_student(self, naam, klas, afstand):
        self.conn.execute(
            "INSERT INTO Students (naam, klas, afstand) VALUES (?, ?, ?)",
            (naam, klas, afstand)
        )
        self.conn.commit()

    def get_students(self):
        return self.conn.execute("SELECT * FROM Students").fetchall()

    def update_student(self, student_id, naam, klas, afstand):
        self.conn.execute(
            "UPDATE Students SET naam=?, klas=?, afstand=? WHERE id=?",
            (naam, klas, afstand, student_id)
        )
        self.conn.commit()

    def delete_student(self, student_id):
        self.conn.execute("DELETE FROM Students WHERE id=?", (student_id,))
        self.conn.commit()

    # TRANSPORT
    def add_transport(self, t):
        self.conn.execute("INSERT INTO Transport (type) VALUES (?)", (t,))
        self.conn.commit()

    def get_transport(self):
        return self.conn.execute("SELECT * FROM Transport").fetchall()

    def update_transport(self, transport_id, t):
        self.conn.execute(
            "UPDATE Transport SET type=? WHERE id=?",
            (t, transport_id)
        )
        self.conn.commit()

    def delete_transport(self, transport_id):
        self.conn.execute("DELETE FROM Transport WHERE id=?", (transport_id,))
        self.conn.commit()

    def transport_in_use(self, transport_id):
        return self.conn.execute(
            "SELECT COUNT(*) FROM Mobility_log WHERE transport_id=?",
            (transport_id,)
        ).fetchone()[0]

    # MOBILITY
    def add_mobility(self, student_id, transport_id, datum):
        self.conn.execute(
            "INSERT INTO Mobility_log (student_id, transport_id, datum) VALUES (?, ?, ?)",
            (student_id, transport_id, datum)
        )
        self.conn.commit()

    def get_mobility(self):
        return self.conn.execute("SELECT * FROM Mobility_log").fetchall()

    def get_mobility_overview(self):
        return self.conn.execute(
            """
            SELECT
                Mobility_log.id,
                Students.naam,
                Transport.type,
                Mobility_log.datum
            FROM Mobility_log
            JOIN Students ON Mobility_log.student_id = Students.id
            JOIN Transport ON Mobility_log.transport_id = Transport.id
            ORDER BY Mobility_log.id
            """
        ).fetchall()

    def update_mobility(self, mobility_id, student_id, transport_id, datum):
        self.conn.execute(
            "UPDATE Mobility_log SET student_id=?, transport_id=?, datum=? WHERE id=?",
            (student_id, transport_id, datum, mobility_id)
        )
        self.conn.commit()

    def delete_mobility(self, mobility_id):
        self.conn.execute("DELETE FROM Mobility_log WHERE id=?", (mobility_id,))
        self.conn.commit()

    # ANALYSE
    def count_transport(self):
        return self.conn.execute(
            "SELECT transport_id, COUNT(*) FROM Mobility_log GROUP BY transport_id"
        ).fetchall()

    def avg_distance(self):
        return self.conn.execute(
            "SELECT AVG(afstand) FROM Students"
        ).fetchone()[0] 
    
    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
