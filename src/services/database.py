import sqlite3
import json
from pathlib import Path
from typing import List, Dict

# ----------------------------
# Database path
# ----------------------------
DB_PATH = Path("scan_history.db")  # Uses the file we just created

# ----------------------------
# Initialize database (creates table if not exists)
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            domain TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            warnings TEXT,
            recommendations TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize once when imported
init_db()

# ----------------------------
# Save scan result
# ----------------------------
def save_scan_result(
    url: str,
    domain: str,
    risk_score: int,
    risk_level: str,
    warnings: List[str],
    recommendations: List[str],
    timestamp: str
) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_history
        (url, domain, risk_score, risk_level, warnings, recommendations, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        url,
        domain,
        risk_score,
        risk_level,
        json.dumps(warnings),
        json.dumps(recommendations),
        timestamp
    ))
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

# ----------------------------
# Get recent scans
# ----------------------------
def get_recent_scans(limit: int = 20) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, url, domain, risk_score, risk_level, warnings, recommendations, timestamp
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    scans = []
    for row in rows:
        scans.append({
            "id": row[0],
            "url": row[1],
            "domain": row[2],
            "risk_score": row[3],
            "risk_level": row[4],
            "warnings": json.loads(row[5]) if row[5] else [],
            "recommendations": json.loads(row[6]) if row[6] else [],
            "scan_timestamp": row[7]
        })
    return scans

# ----------------------------
# Get scan by ID
# ----------------------------
def get_scan_by_id(scan_id: int) -> Dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, url, domain, risk_score, risk_level, warnings, recommendations, timestamp
        FROM scan_history
        WHERE id = ?
    """, (scan_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "url": row[1],
        "domain": row[2],
        "risk_score": row[3],
        "risk_level": row[4],
        "warnings": json.loads(row[5]) if row[5] else [],
        "recommendations": json.loads(row[6]) if row[6] else [],
        "scan_timestamp": row[7]
    }

# ----------------------------
# Get scans by domain
# ----------------------------
def get_scans_by_domain(domain: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, url, domain, risk_score, risk_level, warnings, recommendations, timestamp
        FROM scan_history
        WHERE domain = ?
        ORDER BY id DESC
    """, (domain,))
    rows = cursor.fetchall()
    conn.close()

    scans = []
    for row in rows:
        scans.append({
            "id": row[0],
            "url": row[1],
            "domain": row[2],
            "risk_score": row[3],
            "risk_level": row[4],
            "warnings": json.loads(row[5]) if row[5] else [],
            "recommendations": json.loads(row[6]) if row[6] else [],
            "scan_timestamp": row[7]
        })
    return scans
