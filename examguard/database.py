import os
import sqlite3

# ------------------------------------------------------------
# DATABASE LOCATION
# ------------------------------------------------------------
# NOTE: earlier this pointed at "database/examguard.db" while a
# leftover "database.db" sat in the project root and was never
# actually used. The app now consistently reads/writes the same
# file everywhere via this module.
DATABASE_DIR = "database"
DATABASE = os.path.join(DATABASE_DIR, "examguard.db")


def get_db():
    """Open a connection to the ExamGuard database."""

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    """Create every table the platform needs, if it doesn't exist yet."""

    connection = get_db()

    # ------------------------------------------------
    # CANDIDATES
    # ------------------------------------------------
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS candidates (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name TEXT NOT NULL,
    #         email TEXT UNIQUE NOT NULL,
    #         password TEXT NOT NULL,
    #         photo TEXT,
    #         created_at TEXT DEFAULT (datetime('now'))
    #     )
    # """)

    # ------------------------------------------------
    # EXAM SESSION LIFECYCLE (start / pause / submit)
    # ------------------------------------------------
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS exam_sessions (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         candidate_id INTEGER NOT NULL,
    #         session_id TEXT UNIQUE NOT NULL,
    #         status TEXT NOT NULL DEFAULT 'in_progress',
    #         started_at TEXT NOT NULL,
    #         paused_at TEXT,
    #         resumed_at TEXT,
    #         submitted_at TEXT,
    #         FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    #     )
    # """)

    # ------------------------------------------------
    # FACE PRESENCE MONITORING EVENTS
    # ------------------------------------------------
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS face_events (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         candidate_id INTEGER NOT NULL,
    #         session_id TEXT NOT NULL,
    #         event_type TEXT NOT NULL,
    #         started_at TEXT NOT NULL,
    #         ended_at TEXT,
    #         duration_seconds REAL,
    #         FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    #     )
    # """)

    # ------------------------------------------------
    # BROWSER ACTIVITY EVENTS
    # ------------------------------------------------
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS browser_events (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         candidate_id INTEGER NOT NULL,
    #         session_id TEXT NOT NULL,
    #         event_type TEXT NOT NULL,
    #         event_time TEXT NOT NULL,
    #         details TEXT,
    #         FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    #     )
    # """)

    # ------------------------------------------------
    # SUSPICIOUS / FLAGGED EVENTS (rule engine output)
    # ------------------------------------------------
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS suspicious_events (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         candidate_id INTEGER NOT NULL,
    #         session_id TEXT NOT NULL,
    #         event_type TEXT NOT NULL,
    #         reason TEXT NOT NULL,
    #         event_time TEXT NOT NULL,
    #         severity TEXT NOT NULL,
    #         FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    #     )
    # """)
    
    # connection.execute("""
    #     CREATE TABLE IF NOT EXISTS exam_sessions (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         candidate_id INTEGER NOT NULL,
    #         session_id TEXT UNIQUE NOT NULL,
    #         status TEXT NOT NULL DEFAULT 'in_progress',
    #         started_at TEXT NOT NULL,
    #         paused_at TEXT,
    #         resumed_at TEXT,
    #         submitted_at TEXT,
    #         FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    #     )
    # """)

    connection.commit()
    connection.close()
