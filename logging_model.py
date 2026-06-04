from datetime import datetime


def create_logging_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Action_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        detail TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    kolommen = [row[1] for row in conn.execute("PRAGMA table_info(Action_logs)").fetchall()]
    if "detail" not in kolommen:
        conn.execute("ALTER TABLE Action_logs ADD COLUMN detail TEXT")


def add_action_log(conn, user_id, action_type, detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """
        INSERT INTO Action_logs (user_id, action_type, detail, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, action_type, detail, timestamp),
    )
    conn.commit()


def get_action_logs(conn):
    return conn.execute(
        """
        SELECT id, user_id, action_type, COALESCE(detail, ''), timestamp
        FROM Action_logs
        ORDER BY id DESC
        """
    ).fetchall()


def get_action_count_by_user(conn):
    return conn.execute(
        """
        SELECT user_id, COUNT(*) AS aantal
        FROM Action_logs
        GROUP BY user_id
        ORDER BY aantal DESC, user_id
        """
    ).fetchall()


def get_action_count_by_type(conn):
    return conn.execute(
        """
        SELECT action_type, COUNT(*) AS aantal
        FROM Action_logs
        GROUP BY action_type
        ORDER BY aantal DESC, action_type
        """
    ).fetchall()


def get_most_active_users(conn):
    rows = get_action_count_by_user(conn)
    if not rows:
        return []

    hoogste_aantal = rows[0][1]
    return [row for row in rows if row[1] == hoogste_aantal]
