"""
data/importeer_csv.py
-------------------
Hulpprogramma om de 3 CSV-bestanden in de SQLite-databank te laden.
Voer dit éénmalig uit vóór de eerste start van de applicatie.

Gebruik:
    python data/importeer_csv.py
"""

import csv
import os
import sys

# Zorg dat we de root van het project kunnen vinden
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from model_sql import database as db

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def importeer():
    print("🗄️  Databank initialiseren …")
    db.initialize_database()

    # ── Transport ────────────────────────────────────────────────────────────
    transport_pad = os.path.join(DATA_DIR, "transports.csv")
    transport_map: dict[int, int] = {}   # csv-id → db-id

    with open(transport_pad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rijen = list(reader)

    # Leeg de tabel eerst (idempotent importeren)
    import sqlite3
    conn = sqlite3.connect(db.DB_PATH)
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("DELETE FROM Mobility_log")
    conn.execute("DELETE FROM Students")
    conn.execute("DELETE FROM Transport")
    conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('Students','Transport','Mobility_log')")
    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON")
    conn.close()

    for rij in rijen:
        nieuw_id = db.transport_create(rij["type"])
        transport_map[int(rij["id"])] = nieuw_id

    print(f"   ✅ {len(rijen)} vervoersmiddelen geladen.")

    # ── Students ─────────────────────────────────────────────────────────────
    students_pad = os.path.join(DATA_DIR, "students.csv")
    student_map: dict[int, int] = {}   # csv-id → db-id

    with open(students_pad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rijen = list(reader)

    for rij in rijen:
        nieuw_id = db.student_create(rij["naam"], rij["klas"], float(rij["afstand"]))
        student_map[int(rij["id"])] = nieuw_id

    print(f"   ✅ {len(rijen)} studenten geladen.")

    # ── Mobility logs ─────────────────────────────────────────────────────────
    logs_pad = os.path.join(DATA_DIR, "mobility_logs.csv")

    with open(logs_pad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rijen = list(reader)

    geladen = 0
    for rij in rijen:
        csv_sid = int(rij["student_id"])
        csv_tid = int(rij["transport_id"])
        sid = student_map.get(csv_sid)
        tid = transport_map.get(csv_tid)
        if sid is None or tid is None:
            print(f"   ⚠️  Log rij {rij['id']}: onbekende student_id={csv_sid} of transport_id={csv_tid}, overgeslagen.")
            continue
        db.log_create(sid, tid, rij["datum"])
        geladen += 1

    print(f"   ✅ {geladen} verplaatsingen geladen.")

    # ── Testdata projectteam (manueel toevoegen) ──────────────────────────────
    print("\n📝  Testdata projectteam toevoegen …")

    teamleden = [
        {"naam": "Ouadie F",    "klas": "6ADB", "afstand": 0.4},
        {"naam": "Marouane A", "klas": "6ADB", "afstand": 7.8},
        {"naam": "Bjarne B",  "klas": "6ADB", "afstand": 10.5},
        {"naam": "Viggo dV",  "klas": "6ADB", "afstand": 5.0},
    ]

    # Haal transport IDs op
    transporten = {t["type"]: t["id"] for t in db.transport_read_all()}

    from datetime import date, timedelta
    test_datums = [
        date(2026, 4, 14).strftime("%Y-%m-%d"),
        date(2026, 4, 15).strftime("%Y-%m-%d"),
        date(2026, 4, 16).strftime("%Y-%m-%d"),
    ]
    test_transport_types = ["Fiets", "Bus", "Auto", "Te voet"]

    for i, lid in enumerate(teamleden):
        sid = db.student_create(lid["naam"], lid["klas"], lid["afstand"])
        transport_type = test_transport_types[i % len(test_transport_types)]
        tid = transporten.get(transport_type)
        if tid:
            for datum in test_datums:
                db.log_create(sid, tid, datum)
        print(f"   ✅ {lid['naam']} toegevoegd met {len(test_datums)} verplaatsingen ({transport_type}).")

    print("\n🎉  Import voltooid!")


if __name__ == "__main__":
    importeer()
