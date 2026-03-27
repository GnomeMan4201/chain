#!/usr/bin/env python3
def pulse(attacker, target):
    print(f"\033[95m → Infecting {target} from {attacker}...\033[0m")
    time.sleep(0.1)
    print("\033[90m   .\033[0m"); time.sleep(0.1)
    print("\033[90m   .\033[0m"); time.sleep(0.1)
    print("\033[92m   ✓\033[0m"); time.sleep(0.1)
def load_lines():
    try:
        with open("inject_silent.log") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def pulse(attacker, target):
    print(f"\033[95m → Infecting {target} from {attacker}...\033[0m")
    time.sleep(0.1)
    print("\033[90m   .\033[0m"); time.sleep(0.1)
    print("\033[90m   .\033[0m"); time.sleep(0.1)
    print("\033[92m   ✓\033[0m"); time.sleep(0.1)
def load_lines():
    try:
        with open("inject_silent.log") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

#!/usr/bin/env python3
import time, os, sys

LOG = os.path.expanduser('~/LANIMORPH/logs/inject_silent.log')
PULSE_DELAY = 0.05
ENTRY_DELAY = 0.3

LIVE = '--live' in sys.argv
EXPORT = '--export' in sys.argv
EXPORT_FILE = os.path.expanduser('~/LANIMORPH/chain/replay_export.txt') if EXPORT else None

seen = set()
history = []

def parse_line(line):
    try:
        ts = line.split("[")[1].split("]")[0].strip()
        attacker = line.split("by ")[1].split(" [")[0].strip()
        target = line.split(" [")[1].split(" ]")[0].strip()
        return ts, attacker, target
    except Exception:
        return "", "", ""
def get_extra(ip):
    vault = os.path.expanduser('~/LANIMORPH/memory/mutation_memory.db')
    if not os.path.exists(vault): return ""
    try:
        import sqlite3
        con = sqlite3.connect(vault)
        cur = con.cursor()
        cur.execute("SELECT payload, personality, gen FROM mutations WHERE host=?", (ip,))
        row = cur.fetchone()
        if row:
            return f"[{row[0]} | {row[1]} | gen{row[2]}]"
    except:
        pass
    return ""

def replay():
    lines = load_lines()
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        ts, attacker, target = parse_line(line)
        if not attacker or not target:
            continue
        pulse(attacker, target)
        meta = get_extra(target)
        out = f"\033[92m[✓] {ts} :: {attacker} → {target} {meta}\033[0m"
        print(out)
        history.append(out)
        if EXPORT:
            with open(EXPORT_FILE, 'a') as f:
                f.write(out + '\n')
        time.sleep(ENTRY_DELAY)

print("\033[1;34mLANIMORPH :: ADVANCED ASCII REPLAY\n" + "="*42 + "\033[0m")

try:
    if EXPORT:
        open(EXPORT_FILE, 'w').close()
    if LIVE:
        while True:
            replay()
            time.sleep(1)
    else:
        replay()
        print(f"\n\033[1;34m[✓] Replay complete. Total: {len(history)}\033[0m")
except KeyboardInterrupt:
    print("\n\033[1;31m[!] Interrupted by user.\033[0m")

# === Summary Stats ===
from collections import defaultdict

def print_summary(lines):
    infect_count = 0
    unique_targets = set()
    unique_attackers = set()
    chain_depth = defaultdict(int)

    for line in lines:
        try:
            ts = line.split("[")[1].split("]")[0].strip()
            attacker = line.split("by ")[1].split(" [")[0].strip()
            target = line.split(" [")[1].split(" ]")[0].strip()
            unique_targets.add(target)
            unique_attackers.add(attacker)
            infect_count += 1
            chain_depth[attacker] += 1
        except:
            continue

    print("\n" + "="*60)
    print(f"\033[92m[✓] Total Infections: {infect_count}")
    print(f"[✓] Unique Hosts Infected: {len(unique_targets)}")
    print(f"[✓] Attackers Involved: {len(unique_attackers)}")
    print(f"[✓] Max Infections from One Host: {max(chain_depth.values(), default=0)}\033[0m")
    print("="*60 + "\n")

# === Hook into replay ===
if __name__ == "__main__":
    replay()
    print_summary(load_lines())

# === Horizontal Bar Graph (Infection Impact) ===
def print_infection_bars(lines):
    from collections import defaultdict

    infectors = defaultdict(int)
    for line in lines:
        try:
            attacker = line.split("by ")[1].split(" [")[0].strip()
            infectors[attacker] += 1
        except:
            continue

    if not infectors:
        print("\n(no infection data)\n")
        return

    print("\n\033[1;33mINFECTORS :: PAYLOAD IMPACT\033[0m")
    print("="*30)
    max_val = max(infectors.values())
    for attacker, count in sorted(infectors.items(), key=lambda x: -x[1]):
        bar = "█" * int((count / max_val) * 30)
        print(f"{attacker.ljust(15)} | {bar} ({count})")

# === Final display hook ===
    print_infection_bars(lines)
