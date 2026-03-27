#!/usr/bin/env python3
import os, time
from datetime import datetime

logfile = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
seen = set()
def parse_line(line):
    if "::" in line:
        parts = line.strip().split("::")
        ts = parts[-1].split("=")[-1]
        host = parts[0].split(":")[1]
        mut = parts[1].split("=")[-1]
        return int(ts), host, mut
    return None

def draw(lines):
    print("="*60)
    print("LANIMORPH :: MUTATION TIMELINE MAP")
    print("="*60)
    for ts, host, mut in sorted(lines):
        tstr = datetime.fromtimestamp(ts).strftime("%H:%M")
        print(f"[{tstr}] {host:<15} => {mut}")
    print("="*60)

def watch():
    while True:
        if os.path.exists(logfile):
            with open(logfile) as f:
                lines = f.readlines()
            parsed = []
            for l in lines:
                if l not in seen:
                    seen.add(l)
                    parsed.append(parse_line(l))
            parsed = [p for p in parsed if p]
            os.system("clear")
            draw(parsed)
        time.sleep(5)

if __name__ == "__main__":
    watch()
