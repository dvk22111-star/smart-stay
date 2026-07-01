import sqlite3

conn = sqlite3.connect('smart_stay.db')
cursor = conn.cursor()

# Get schema of bot_registration_sessions
cursor.execute("PRAGMA table_info(bot_registration_sessions)")
print('Bot Registration Sessions Schema:')
for row in cursor.fetchall():
    print(row)

# Check foreign keys
cursor.execute("PRAGMA foreign_key_list(bot_registration_sessions)")
print('\nForeign Keys:')
for row in cursor.fetchall():
    print(row)

# Check schema of other tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print('\nAll tables:')
for row in cursor.fetchall():
    print(row[0])

# Check vacations table
cursor.execute("PRAGMA table_info(vacations)")
print('\nVacations Schema:')
for row in cursor.fetchall():
    print(row)

# Check groups table
cursor.execute("PRAGMA table_info(groups)")
print('\nGroups Schema:')
for row in cursor.fetchall():
    print(row)

conn.close()
