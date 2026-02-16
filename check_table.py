import sqlite3

conn = sqlite3.connect("scan_history.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Check if table is empty
cursor.execute("SELECT * FROM scan_history;")
rows = cursor.fetchall()
print("Scan history rows:", rows)

conn.close()
