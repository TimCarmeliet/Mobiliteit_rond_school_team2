import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"

class ModelSQL:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.maak_tabellen()

    # maakt de 3 tabellen aan als ze nog niet bestaan
    def maak_tabellen(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY,
            naam TEXT NOT NULL,
            klas TEXT NOT NULL,
            afstand REAL NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transport (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mobility_log (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            transport_id INTEGER NOT NULL,
            datum TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (transport_id) REFERENCES Transport(id)
        )
        """)

        self.conn.commit()

    # laadt transport.csv in de tabel Transport
    def import_transport(self):
        csv_path = BASE_DIR / "transport.csv"
        ingevoegd = 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # sla over als het id al bestaat
                bestaat = self.conn.execute(
                    "SELECT id FROM Transport WHERE id = ?", (int(row["id"]),)
                ).fetchone()

                if not bestaat:
                    self.conn.execute(
                        "INSERT INTO Transport (id, type) VALUES (?, ?)",
                        (int(row["id"]), row["type"])
                    )
                    ingevoegd += 1

        self.conn.commit()
        print(f"Transport: {ingevoegd} rijen ingevoegd")

    # laadt students.csv in de tabel Students
    def import_students(self):
        csv_path = BASE_DIR / "students.csv"
        ingevoegd = 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # sla over als het id al bestaat
                bestaat = self.conn.execute(
                    "SELECT id FROM Students WHERE id = ?", (int(row["id"]),)
                ).fetchone()

                if not bestaat:
                    self.conn.execute(
                        "INSERT INTO Students (id, naam, klas, afstand) VALUES (?, ?, ?, ?)",
                        (int(row["id"]), row["naam"], row["klas"], float(row["afstand"]))
                    )
                    ingevoegd += 1

        self.conn.commit()
        print(f"Students: {ingevoegd} rijen ingevoegd")

    # laadt mobility_log.csv in de tabel Mobility_log
    def import_mobility_logs(self):
        csv_path = BASE_DIR / "mobility_log.csv"
        ingevoegd = 0
        overgeslagen = 0

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # controleer of student_id bestaat
                student_bestaat = self.conn.execute(
                    "SELECT id FROM Students WHERE id = ?", (row["student_id"],)
                ).fetchone()

                # controleer of transport_id bestaat
                transport_bestaat = self.conn.execute(
                    "SELECT id FROM Transport WHERE id = ?", (row["transport_id"],)
                ).fetchone()

                if not student_bestaat or not transport_bestaat:
                    print(f"  overgeslagen: student_id={row['student_id']} transport_id={row['transport_id']} bestaat niet")
                    overgeslagen += 1
                    continue

                # sla over als deze log al bestaat
                bestaat = self.conn.execute(
                    "SELECT id FROM Mobility_log WHERE student_id = ? AND transport_id = ? AND datum = ?",
                    (row["student_id"], row["transport_id"], row["datum"])
                ).fetchone()

                if not bestaat:
                    self.conn.execute(
                        "INSERT INTO Mobility_log (student_id, transport_id, datum) VALUES (?, ?, ?)",
                        (row["student_id"], row["transport_id"], row["datum"])
                    )
                    ingevoegd += 1

        self.conn.commit()
        print(f"Mobility_log: {ingevoegd} rijen ingevoegd, {overgeslagen} overgeslagen")

    # voegt testdata toe van het projectteam
    def import_testdata(self):
        # voeg elk teamlid toe als student als die nog niet bestaat
        testdata_students = [
            ("Viggo DE KING", "6ADB", 3.5),
            ("Marouane Booty", "6ADB", 7.2),
            ("Loick Mbala", "6ADB", 5.0),
        ]

        for naam, klas, afstand in testdata_students:
            bestaat = self.conn.execute(
                "SELECT id FROM Students WHERE naam = ? AND klas = ?", (naam, klas)
            ).fetchone()

            if not bestaat:
                self.conn.execute(
                    "INSERT INTO Students (naam, klas, afstand) VALUES (?, ?, ?)",
                    (naam, klas, afstand)
                )

        self.conn.commit()

        # haal de ids op van de testdata studenten
        ids = []
        for naam, klas, _ in testdata_students:
            rij = self.conn.execute(
                "SELECT id FROM Students WHERE naam = ? AND klas = ?", (naam, klas)
            ).fetchone()
            if rij:
                ids.append(rij[0])

        # voeg een verplaatsing toe per teamlid.0   
        testdata_logs = [
            (ids[0], 1, "2026-05-13"),
            (ids[1], 2, "2026-05-13"),
            (ids[2], 3, "2026-05-13"),
        ]

        for student_id, transport_id, datum in testdata_logs:
            bestaat = self.conn.execute(
                "SELECT id FROM Mobility_log WHERE student_id = ? AND transport_id = ? AND datum = ?",
                (student_id, transport_id, datum)
            ).fetchone()

            if not bestaat:
                self.conn.execute(
                    "INSERT INTO Mobility_log (student_id, transport_id, datum) VALUES (?, ?, ?)",
                    (student_id, transport_id, datum)
                )

        self.conn.commit()
        print(f"Testdata: {len(ids)} teamleden toegevoegd")

    # voert de volledige import uit in de juiste volgorde
    def run_import(self):
        print("--- import gestart ---")
        # volgorde is belangrijk
        self.import_transport()
        self.import_students()
        self.import_mobility_logs()
        self.import_testdata()
        print("--- import klaar ---")


if __name__ == "__main__":
    model = ModelSQL()
    model.run_import()