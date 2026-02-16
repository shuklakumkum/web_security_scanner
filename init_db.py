import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path("scan_history.db")

# Connect (this will create the file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the scan_history table if it doesn't exist
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

print(f"Database created at: {DB_PATH.resolve()}")
