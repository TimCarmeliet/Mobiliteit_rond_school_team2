import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"


TABLES = {
    "students": {
        "csv_pattern": "students*.csv",
        "columns": ("id", "naam", "klas", "afstand"),
    },
    "transport": {
        "csv_pattern": "transport*.csv",
        "columns": ("id", "type"),
    },
    "mobility_log": {
        "csv_pattern": "mobility_log*.csv",
        "columns": ("id", "student_id", "transport_id", "datum"),
    },
}


def find_csv_file(pattern):
    files = list(BASE_DIR.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"Geen bestand gevonden voor patroon '{pattern}'"
        )

    if len(files) > 1:
        raise FileExistsError(
            f"Meerdere bestanden gevonden voor patroon '{pattern}': "
            + ", ".join(file.name for file in files)
        )

    return files[0]


def read_csv_rows(csv_path, required_columns):
    with csv_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"{csv_path.name} heeft geen kolomnamen.")

        missing_columns = set(required_columns) - set(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"{csv_path.name} mist deze kolommen: {missing}"
            )

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
    csv_file = find_csv_file(
        TABLES["students"]["csv_pattern"]
    )

    rows = read_csv_rows(
        csv_file,
        TABLES["students"]["columns"]
    )

    connection.executemany(
        """
        INSERT INTO students (id, naam, klas, afstand)
        VALUES (?, ?, ?, ?)
        """,
        (
            (
                int(row["id"]),
                row["naam"],
                row["klas"],
                float(row["afstand"])
            )
            for row in rows
        ),
    )

    return len(rows)


def import_transport(connection):
    csv_file = find_csv_file(
        TABLES["transport"]["csv_pattern"]
    )

    rows = read_csv_rows(
        csv_file,
        TABLES["transport"]["columns"]
    )

    connection.executemany(
        """
        INSERT INTO transport (id, type)
        VALUES (?, ?)
        """,
        (
            (
                int(row["id"]),
                row["type"]
            )
            for row in rows
        ),
    )

    return len(rows)


def import_mobility_log(connection):
    csv_file = find_csv_file(
        TABLES["mobility_log"]["csv_pattern"]
    )

    rows = read_csv_rows(
        csv_file,
        TABLES["mobility_log"]["columns"]
    )

    connection.executemany(
        """
        INSERT INTO mobility_log (
            id,
            student_id,
            transport_id,
            datum
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            (
                int(row["id"]),
                int(row["student_id"]),
                int(row["transport_id"]),
                row["datum"]
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