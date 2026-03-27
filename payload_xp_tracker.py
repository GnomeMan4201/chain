#!/usr/bin/env python3
# LANIMORPH :: XP Tracker (Disabled Mode)

import sys
from pathlib import Path
from datetime import datetime

payload_family = input("[?] Payload family to log (optional): ").strip()
if not payload_family:
    sys.exit(0)

# Optional plaintext log (no SQLite)
log_path = Path.home() / "LANIMORPH" / "logs" / "xp_changelog.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
with open(log_path, "a") as f:
    f.write(f"[{datetime.now().isoformat()}] Logged → {payload_family}\n")

print(f"[✓] Log entry saved (no XP tracking)")
