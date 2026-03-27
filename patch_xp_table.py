#!/usr/bin/env python3
import sqlite3
from pathlib import Path

# Path to XP DB
db_path = Path.home() / "LANIMORPH" / "chain" / "xp_log.db"
conn = sqlite3.connect(db_path)

# Ensure the XP table exists
conn.execute('''
CREATE TABLE IF NOT EXISTS xp (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  payload_family TEXT NOT NULL,
  points INTEGER DEFAULT 1
);
''')

conn.commit()
conn.close()

print(f"[✓] XP table patched at: {db_path}")
