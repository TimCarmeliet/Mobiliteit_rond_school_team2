import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"


TABLES = {
    "students": {
        "csv": BASE_DIR / "students.csv",
        "columns": ("id", "naam", "klas", "afstand"),
    },
    "transport": {
        "csv": BASE_DIR / "transport.csv",
        "columns": ("id", "type"),
    },
    "mobility_log": {
        "csv": BASE_DIR / "mobility_log.csv",
        "columns": ("id", "student_id", "transport_id", "datum"),
    },
}


def read_csv_rows(csv_path, required_columns):
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"{csv_path.name} heeft geen kolomnamen.")

        missing_columns = set(required_columns) - set(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"{csv_path.name} mist deze kolommen: {missing}")

        return list(reader)


def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("DROP TABLE IF EXISTS mobility_log")
    cursor.execute("DROP TABLE IF EXISTS transport")
    cursor.execute("DROP TABLE IF EXISTS students")

    cursor.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            naam TEXT NOT NULL,
            klas TEXT NOT NULL,
            afstand REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE transport (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE mobility_log (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            transport_id INTEGER NOT NULL,
            datum TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (transport_id) REFERENCES transport (id)
        )
        """
    )

    connection.commit()


def import_students(connection):
    rows = read_csv_rows(TABLES["students"]["csv"], TABLES["students"]["columns"])
    connection.executemany(
        """
        INSERT INTO students (id, naam, klas, afstand)
        VALUES (?, ?, ?, ?)
        """,
        (
            (int(row["id"]), row["naam"], row["klas"], float(row["afstand"]))
            for row in rows
        ),
    )
    return len(rows)


def import_transport(connection):
    rows = read_csv_rows(TABLES["transport"]["csv"], TABLES["transport"]["columns"])
    connection.executemany(
        """
        INSERT INTO transport (id, type)
        VALUES (?, ?)
        """,
        ((int(row["id"]), row["type"]) for row in rows),
    )
    return len(rows)


def import_mobility_log(connection):
    rows = read_csv_rows(
        TABLES["mobility_log"]["csv"], TABLES["mobility_log"]["columns"]
    )
    connection.executemany(
        """
        INSERT INTO mobility_log (id, student_id, transport_id, datum)
        VALUES (?, ?, ?, ?)
        """,
        (
            (
                int(row["id"]),
                int(row["student_id"]),
                int(row["transport_id"]),
                row["datum"],
            )
            for row in rows
        ),
    )
    return len(rows)


def build_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        create_tables(connection)

        counts = {
            "students": import_students(connection),
            "transport": import_transport(connection),
            "mobility_log": import_mobility_log(connection),
        }
        connection.commit()

    return counts


if __name__ == "__main__":
    imported_counts = build_database()
    print(f"Database aangemaakt: {DB_PATH.name}")
    print(f"Students: {imported_counts['students']}")
    print(f"Transport: {imported_counts['transport']}")
    print(f"Mobility log: {imported_counts['mobility_log']}")
