#!/usr/bin/env python3
import os, re
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
PROFILE_PATH = os.path.expanduser("~/.lanimorph_profile")

def parse_log():
    if not os.path.exists(LOG):
        print("No mutation log found.")
        return []

    entries = []
    with open(LOG) as f:
        for line in f:
            match = re.match(r"\[(.*?)\]\s+(.*?)\s+->\s+(mut_\d+)\s+::\s+PORT\s+(\d+)", line)
            if match:
                ts, ip, mut_id, port = match.groups()
                entries.append({
                    "timestamp": ts,
                    "ip": ip.strip(),
                    "mutation": mut_id,
                    "port": port.strip()
                })
    return entries

def load_persona():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH) as f:
            try:
                import json
                data = json.load(f)
                return data.get("personality", "scout")
            except: pass
    return "unknown"

def print_table(entries):
    if not entries:
        print("No entries to display.")
        return

    persona = load_persona()
    print("\n== LANIMORPH :: Mutation History Viewer ==")
    print(f"Current Personality: {persona.upper()}")
    print("-" * 64)
    print("{:<20} {:<15} {:<12} {:<10}".format("Timestamp", "IP", "Mutation", "Port"))
    print("-" * 64)
    for e in entries[-20:]:  # show latest 20
        print("{:<20} {:<15} {:<12} {:<10}".format(
            e['timestamp'], e['ip'], e['mutation'], e['port']
        ))
    print("-" * 64)

if __name__ == "__main__":
    data = parse_log()
    print_table(data)
