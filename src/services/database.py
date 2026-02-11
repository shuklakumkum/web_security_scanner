import sqlite3
import json
from datetime import datetime
from pathlib import Path

# SQLite database file
DB_PATH = Path("scan_history.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


# ---------------------------------------------------
# 1. init_database()
# ---------------------------------------------------
def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            domain TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            is_suspicious BOOLEAN,
            scan_timestamp DATETIME,
            results_json TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------
# 2. save_scan()
# ---------------------------------------------------
def save_scan(scan_result: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history (
            url,
            domain,
            risk_score,
            risk_level,
            is_suspicious,
            scan_timestamp,
            results_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_result.get("url"),
        scan_result.get("domain"),
        scan_result.get("risk_score"),
        scan_result.get("risk_level"),
        scan_result.get("is_suspicious"),
        datetime.utcnow().isoformat(),
        json.dumps(scan_result)
    ))

    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()

    return scan_id


# ---------------------------------------------------
# 3. get_scan_by_id()
# ---------------------------------------------------
def get_scan_by_id(scan_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT results_json FROM scan_history WHERE id=?",
        (scan_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return json.loads(row[0]) if row else None


# ---------------------------------------------------
# 4. get_recent_scans()
# ---------------------------------------------------
def get_recent_scans(limit: int = 10) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, results_json
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    scans = []
    for row in rows:
        data = json.loads(row[1])
        data["scan_id"] = row[0]
        scans.append(data)

    return scans


# ---------------------------------------------------
# 5. get_scans_by_domain()
# ---------------------------------------------------
def get_scans_by_domain(domain: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, results_json
        FROM scan_history
        WHERE domain=?
        ORDER BY id DESC
    """, (domain,))

    rows = cursor.fetchall()
    conn.close()

    scans = []
    for row in rows:
        data = json.loads(row[1])
        data["scan_id"] = row[0]
        scans.append(data)

    return scans
