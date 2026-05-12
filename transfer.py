import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

DATABASE_NAME = "database.db"


def clean_table_name(name):
    name = Path(name).stem
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name)


def import_csv_to_db(csv_files, db_name=DATABASE_NAME):
    conn = sqlite3.connect(db_name)

    for csv_file in csv_files:
        try:
            table_name = clean_table_name(csv_file)

            df = pd.read_csv(csv_file)

            df.to_sql(table_name, conn, if_exists="replace", index=False)

            print(f"[OK] Imported '{csv_file}' into table '{table_name}'")

        except Exception as e:
            print(f"[ERROR] Failed to import '{csv_file}': {e}")

    conn.close()
    print(f"\nDatabase saved as: {db_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("python csv_to_sqlite.py file1.csv file2.csv")
        print("or")
        print("python csv_to_sqlite.py folder_path")
        sys.exit(1)

    input_paths = sys.argv[1:]
    csv_files = []

    for path in input_paths:
        if os.path.isfile(path) and path.endswith(".csv"):
            csv_files.append(path)

        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".csv"):
                        csv_files.append(os.path.join(root, file))

    if not csv_files:
        print("No CSV files found.")
        sys.exit(1)

    import_csv_to_db(csv_files)
