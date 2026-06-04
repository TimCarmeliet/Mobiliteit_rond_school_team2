import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"


class Model:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
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

    # ── ANALYSE PER KLAS ─────────────────────────────────────────────────────

    def get_studenten_per_klas(self):
        """
        Geeft per klas het aantal studenten en de gemiddelde afstand.
        Eén eenvoudige SQL-query met GROUP BY (geen JOIN nodig).

        Resultaat: lijst van tuples (klas, aantal, gem_afstand)
        """
        return self.fetch_all("""
            SELECT klas, COUNT(*) AS aantal, ROUND(AVG(afstand), 2) AS gem_afstand
            FROM Students
            GROUP BY klas
            ORDER BY klas
        """)

    def get_vervoer_per_klas(self):
        """
        Geeft de verdeling van vervoersmiddelen per klas.

        Gebruikt GEEN JOIN, maar drie aparte queries en Python-logica
        (aanbevolen aanpak uit de projectfiche):

        Stap 1: studenten ophalen  (id -> klas)
        Stap 2: verplaatsingen ophalen (student_id -> transport_id)
        Stap 3: transportnamen ophalen (id -> type)
        Stap 4: combineren in Python met een teller per klas per vervoer

        Resultaat: dict { klas: { transport_type: aantal_verplaatsingen } }
        """
        # Stap 1: welke klas heeft elke student?
        students = self.fetch_all("SELECT id, klas FROM Students")
        student_klas = {row[0]: row[1] for row in students}

        # Stap 2: alle verplaatsingen (student_id, transport_id)
        mobility = self.fetch_all("SELECT student_id, transport_id FROM Mobility_log")

        # Stap 3: naam van elk transporttype opzoeken
        transport = self.fetch_all("SELECT id, type FROM Transport")
        transport_naam = {row[0]: row[1] for row in transport}

        # Stap 4: tellen per klas per vervoersmiddel
        klas_vervoer = {}
        for student_id, transport_id in mobility:
            klas = student_klas.get(student_id, "Onbekend")
            transport_type = transport_naam.get(transport_id, "Onbekend")
            if klas not in klas_vervoer:
                klas_vervoer[klas] = {}
            klas_vervoer[klas][transport_type] = klas_vervoer[klas].get(transport_type, 0) + 1

        return klas_vervoer

    # ANALYSE
    def count_transport(self):
        return self.conn.execute(
            "SELECT transport_id, COUNT(*) FROM Mobility_log GROUP BY transport_id"
        ).fetchall()

    def get_transport_verdeling(self):
        transport = self.conn.execute("SELECT id, type FROM Transport").fetchall()
        counts = self.conn.execute(
            "SELECT transport_id, COUNT(*) FROM Mobility_log GROUP BY transport_id"
        ).fetchall()
        counts_dict = {row[0]: row[1] for row in counts}

        resultaat = []
        for transport_id, transport_type in transport:
            aantal = counts_dict.get(transport_id, 0)
            resultaat.append((transport_type, aantal))

        return resultaat

    def avg_distance(self):
        return self.conn.execute(
            "SELECT AVG(afstand) FROM Students"
        ).fetchone()[0]
        
    # gemiddelde afstand per vervoersmiddel
    def avg_distance_per_transport(self):
        # haal alle transport types op
        transporten = self.conn.execute("SELECT id, type FROM Transport").fetchall()

        resultaat = []
        for transport_id, transport_type in transporten:
            # haal alle student ids op die dit transport gebruiken
            logs = self.conn.execute(
                "SELECT DISTINCT student_id FROM Mobility_log WHERE transport_id = ?",
                (transport_id,)
            ).fetchall()

            if not logs:
                continue

            student_ids = [log[0] for log in logs]

            # bereken de gemiddelde afstand voor deze studenten
            placeholders = ",".join("?" * len(student_ids))
            gemiddelde = self.conn.execute(
                f"SELECT AVG(afstand) FROM Students WHERE id IN ({placeholders})",
                student_ids
            ).fetchone()[0]

            if gemiddelde is not None:
                resultaat.append((transport_type, round(gemiddelde, 2)))

        return resultaat

    def get_avg_distance_overall(self):
        """
        Berekent de gemiddelde afstand tot school van alle studenten.
        Geeft een afgerond getal terug, of 0.0 als er geen data is.
        """
        row = self.conn.execute("SELECT AVG(afstand) FROM Students").fetchone()
        return round(row[0], 2) if row and row[0] is not None else 0.0

    def get_avg_distance_per_transport(self):
        """
        Berekent de gemiddelde afstand tot school per gebruikt vervoersmiddel.
        Gebruikt GEEN SQL JOINs om te voldoen aan de projectfiche richtlijnen,
        maar combineert de data in Python.
        """
        # Stap 1: studenten ophalen (id -> afstand)
        students = self.fetch_all("SELECT id, afstand FROM Students")
        student_distances = {row[0]: row[1] for row in students}

        # Stap 2: transporttypen ophalen (id -> type)
        transports = self.fetch_all("SELECT id, type FROM Transport")
        transport_types = {row[0]: row[1] for row in transports}

        # Stap 3: alle verplaatsingen ophalen (student_id, transport_id)
        logs = self.fetch_all("SELECT student_id, transport_id FROM Mobility_log")

        # Stap 4: tellers en sommen bijhouden per type vervoer
        vervoer_stats = {} # {type: [som_afstand, aantal_verplaatsingen]}
        for student_id, transport_id in logs:
            dist = student_distances.get(student_id)
            t_type = transport_types.get(transport_id)
            if dist is not None and t_type is not None:
                if t_type not in vervoer_stats:
                    vervoer_stats[t_type] = [0.0, 0]
                vervoer_stats[t_type][0] += dist
                vervoer_stats[t_type][1] += 1

        # Stap 5: gemiddelde berekenen per type
        resultaat = []
        for t_type, stats in sorted(vervoer_stats.items()):
            gem = round(stats[0] / stats[1], 2) if stats[1] > 0 else 0.0
            resultaat.append((t_type, gem))
        return resultaat


    def fetch_all(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ SQL ERROR in fetch_all:\nQuery: {query}\nParams: {params}\nFout: {e}")
            raise e

    def fetch_one(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"❌ SQL ERROR in fetch_one:\nQuery: {query}\nParams: {params}\nFout: {e}")
            raise e

    def execute(self, query, params=()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"❌ SQL ERROR in execute:\nQuery: {query}\nParams: {params}\nFout: {e}")
            raise e


    # ── CO2-UITBREIDING (uitbreiding Ouadie) ──────────────────────────────────

    def get_co2_data(self):
        """
        Haalt alle data op die nodig is voor de CO2-berekening.
        Gebruikt GEEN SQL JOINs om te voldoen aan de projectrichtlijnen,
        maar combineert de data in Python.
        """
        # 1. Studenten ophalen
        students = self.fetch_all("SELECT id, naam, klas, afstand FROM Students")
        student_dict = {
            row[0]: {"naam": row[1], "klas": row[2], "afstand": row[3]}
            for row in students
        }

        # 2. Transporttypes ophalen
        transports = self.fetch_all("SELECT id, type FROM Transport")
        transport_dict = {row[0]: row[1] for row in transports}

        # 3. Mobility logs ophalen
        logs = self.fetch_all("SELECT id, student_id, transport_id, datum FROM Mobility_log")

        # 4. Combineren
        result = []
        for log_id, student_id, transport_id, datum in logs:
            student = student_dict.get(student_id)
            t_type = transport_dict.get(transport_id)
            if student and t_type:
                result.append({
                    "log_id": log_id,
                    "student": student["naam"],
                    "klas": student["klas"],
                    "transport": t_type,
                    "afstand": student["afstand"],
                    "datum": datum
                })
        return result

