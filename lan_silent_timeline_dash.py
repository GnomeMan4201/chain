#!/usr/bin/env python3
import os
from datetime import datetime

logfile = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
if not os.path.exists(logfile):
    print("[!] No silent log found at:", logfile)
    exit(1)

print("=" * 60)
print("LANIMORPH :: SILENT TIMELINE DASHBOARD")
print("=" * 60)

with open(logfile, 'r') as f:
    entries = f.readlines()

if not entries:
    print("(no entries yet)")
    exit(0)

for entry in entries[-30:]:
    try:
        time, event = entry.strip().split("::", 1)
        ts = datetime.strptime(time.strip(), "%Y-%m-%d_%H:%M:%S")
        print(f"[{ts.strftime('%b %d %H:%M')}] {event.strip()}")
    except:
        print(entry.strip())
