import sqlite3

# Connect to your database
conn = sqlite3.connect("scan_history.db")
cursor = conn.cursor()

# Show tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# See all scan records
cursor.execute("SELECT * FROM scan_history;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
