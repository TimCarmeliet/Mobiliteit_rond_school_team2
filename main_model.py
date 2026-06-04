import sqlite3
from pathlib import Path

from logging_model import (
    add_action_log,
    create_logging_table,
    get_action_count_by_type,
    get_action_count_by_user,
    get_action_logs,
    get_most_active_users,
)


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

        # Uitbreiding Viggo: nieuwe tabel voor aanwezigheidsregistratie.
        # Bestaande tabellen worden NIET aangepast (vereiste uit de projectfiche).
        # Status kan zijn: 'aanwezig', 'afwezig' of 'laat'.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            datum TEXT,
            status TEXT
        )
        """)
        create_logging_table(self.conn)

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

    # ── ATTENDANCE / AFWEZIGHEID (uitbreiding Viggo) ─────────────────────────

    def add_attendance(self, student_id, datum, status):
        """Voeg een nieuw aanwezigheidsrecord toe aan de databank."""
        self.conn.execute(
            "INSERT INTO Attendance (student_id, datum, status) VALUES (?, ?, ?)",
            (student_id, datum, status)
        )
        self.conn.commit()

    def get_attendance(self):
        """Haal alle aanwezigheidsrecords op als ruwe data (id, student_id, datum, status)."""
        return self.conn.execute("SELECT * FROM Attendance").fetchall()

    def get_attendance_overview(self):
        """
        Haal aanwezigheidsrecords op met studentnaam en klas voor weergave in de tabel.
        Gebruikt een JOIN om de naam op te zoeken in de Students-tabel.
        """
        return self.conn.execute("""
            SELECT Attendance.id, Students.naam, Students.klas, Attendance.datum, Attendance.status
            FROM Attendance
            JOIN Students ON Attendance.student_id = Students.id
            ORDER BY Attendance.datum DESC, Students.naam
        """).fetchall()

    def update_attendance(self, attendance_id, student_id, datum, status):
        """Pas een bestaand aanwezigheidsrecord aan op basis van het id."""
        self.conn.execute(
            "UPDATE Attendance SET student_id=?, datum=?, status=? WHERE id=?",
            (student_id, datum, status, attendance_id)
        )
        self.conn.commit()

    def delete_attendance(self, attendance_id):
        """Verwijder een aanwezigheidsrecord uit de databank op basis van het id."""
        self.conn.execute("DELETE FROM Attendance WHERE id=?", (attendance_id,))
        self.conn.commit()

    # ── ANALYSES AFWEZIGHEID ──────────────────────────────────────────────────

    def get_afwezigheid_per_klas(self):
        """
        Bereken het aantal aanwezig/afwezig/laat per klas.
        Gebruikt GEEN JOIN, maar combineert twee aparte queries via Python
        (aanbevolen aanpak uit de projectfiche).

        Stap 1: haal alle studenten op (id -> klas)
        Stap 2: haal alle aanwezigheidsrecords op
        Stap 3: combineer de data in Python met een teller per klas

        Geeft een dict terug: { klas: { "aanwezig": n, "afwezig": n, "laat": n } }
        """
        # Stap 1: studenten ophalen zodat we weten welke klas elke student heeft
        students = self.fetch_all("SELECT id, klas FROM Students")
        student_klas = {row[0]: row[1] for row in students}  # {student_id: klas}

        # Stap 2: alle aanwezigheidsrecords ophalen
        records = self.fetch_all("SELECT student_id, status FROM Attendance")

        # Stap 3: in Python de tellers per klas bijhouden
        klas_data = {}
        for student_id, status in records:
            klas = student_klas.get(student_id, "Onbekend")
            if klas not in klas_data:
                # initialiseer de teller voor een nieuwe klas
                klas_data[klas] = {"aanwezig": 0, "afwezig": 0, "laat": 0}
            klas_data[klas][status] = klas_data[klas].get(status, 0) + 1

        return klas_data

    def get_aanwezigheid_percentage_per_klas(self):
        """
        Bereken het aanwezigheidspercentage per klas.
        Bouwt verder op get_afwezigheid_per_klas().

        Geeft een lijst van tuples terug:
        (klas, aanwezig, afwezig, laat, totaal, percentage)
        """
        klas_data = self.get_afwezigheid_per_klas()
        resultaat = []

        for klas, counts in sorted(klas_data.items()):
            totaal = sum(counts.values())
            aanwezig = counts.get("aanwezig", 0)
            afwezig = counts.get("afwezig", 0)
            laat = counts.get("laat", 0)
            # procentuele aanwezigheid: hoeveel % van de registraties is 'aanwezig'
            percentage = round(aanwezig / totaal * 100, 1) if totaal > 0 else 0
            resultaat.append((klas, aanwezig, afwezig, laat, totaal, percentage))

        return resultaat

    def get_vervoer_vs_aanwezigheid(self):
        """
        Analyseert de relatie tussen vervoersmiddel en aanwezigheid.

        Voor elke dag waarop een student zowel een mobility_log-entry als een
        aanwezigheidsrecord heeft, koppelen we het vervoersmiddel aan de status.

        Gebruikt GEEN JOIN maar drie aparte queries en Python-logica:
        Stap 1: mobility_log ophalen -> (student_id, datum) koppelt aan transport_id
        Stap 2: transportnamen ophalen
        Stap 3: aanwezigheidsrecords ophalen
        Stap 4: de drie datasets combineren in Python

        Geeft een dict terug:
        { transport_type: { "aanwezig": n, "afwezig": n, "laat": n } }
        """
        # Stap 1: verplaatsingen ophalen: (student_id, datum) -> transport_id
        mobility = self.fetch_all("SELECT student_id, datum, transport_id FROM Mobility_log")
        # opzoektabel zodat we snel transport_id vinden voor een (student, datum)-combinatie
        vervoer_per_student_dag = {(row[0], row[1]): row[2] for row in mobility}

        # Stap 2: transportnamen ophalen: transport_id -> type
        transport = self.fetch_all("SELECT id, type FROM Transport")
        transport_naam = {row[0]: row[1] for row in transport}

        # Stap 3: alle aanwezigheidsrecords ophalen
        records = self.fetch_all("SELECT student_id, datum, status FROM Attendance")

        # Stap 4: voor elke aanwezigheid het bijhorende vervoersmiddel opzoeken
        vervoer_status = {}
        for student_id, datum, status in records:
            transport_id = vervoer_per_student_dag.get((student_id, datum))
            if transport_id:
                # deze student had op deze dag ook een verplaatsingsregistratie
                transport_type = transport_naam.get(transport_id, "Onbekend")
                if transport_type not in vervoer_status:
                    vervoer_status[transport_type] = {"aanwezig": 0, "afwezig": 0, "laat": 0}
                vervoer_status[transport_type][status] = vervoer_status[transport_type].get(status, 0) + 1

        return vervoer_status

    # LOGGING UITBREIDING
    def add_action_log(self, user_id, action_type):
        add_action_log(self.conn, user_id, action_type)

    def get_action_logs(self):
        return get_action_logs(self.conn)

    def get_action_count_by_user(self):
        return get_action_count_by_user(self.conn)

    def get_action_count_by_type(self):
        return get_action_count_by_type(self.conn)

    def get_most_active_users(self):
        return get_most_active_users(self.conn)
