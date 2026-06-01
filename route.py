import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "school.db"


class Route:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Travel_time_estimation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            transport_id INTEGER,
            geschatte_reistijd REAL,
            datum TEXT,
            FOREIGN KEY (student_id) REFERENCES Students(id),
            FOREIGN KEY (transport_id) REFERENCES Transport(id)
        )
        """)
        self.conn.commit()
