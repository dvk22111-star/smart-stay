import os
import shutil
import sqlite3
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT, 'smart_stay.db')

def backup_db(db_path: str):
    if not os.path.exists(db_path):
        print('DB not found at', db_path)
        return None
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    bak = db_path + f'.bak.{ts}'
    shutil.copy2(db_path, bak)
    print('Backup created:', bak)
    return bak

def ensure_accessibility_preference(conn: sqlite3.Connection):
    cur = conn.cursor()
    # check preferences table
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preferences';")
    if not cur.fetchone():
        print('Table `preferences` does not exist — skipping insertion.')
        return

    cur.execute("SELECT PreferenceType FROM preferences WHERE PreferenceType = 'ACCESSIBILITY' LIMIT 1;")
    if cur.fetchone():
        print('ACCESSIBILITY preference already exists')
        return

    cur.execute("INSERT INTO preferences (PreferenceType) VALUES ('ACCESSIBILITY');")
    conn.commit()
    print('Inserted ACCESSIBILITY into preferences')

def ensure_accessible_column(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(rooms);")
    cols = [r[1] for r in cur.fetchall()]
    if 'Accessible' in cols:
        print('rooms.Accessible column already exists')
        return
    try:
        cur.execute('ALTER TABLE rooms ADD COLUMN Accessible INTEGER DEFAULT 0;')
        conn.commit()
        print('Added Accessible column to rooms')
    except Exception as e:
        print('Failed to add Accessible column:', e)

def main():
    print('Running migration: ensure ACCESSIBILITY preference and Accessible column')
    bak = backup_db(DB_PATH)
    if not os.path.exists(DB_PATH):
        print('Database file does not exist; aborting.')
        return
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_accessibility_preference(conn)
        ensure_accessible_column(conn)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
