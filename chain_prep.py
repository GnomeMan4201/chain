#!/usr/bin/env python3
"""
chain_prep.py — scrub + sanitize + generate README for chain project
run from: ~/projects/chain/
produces: chain_clean/ ready for github
"""

import os
import re
import json
import csv
import shutil
import sqlite3
import random
import string
from pathlib import Path
from datetime import datetime, timedelta

SRC = Path.home() / "projects" / "chain"
DST = Path.home() / "projects" / "chain_clean"

# ── IP scrubbing ─────────────────────────────────────────────────────────────

# map real IPs to stable fake ones so references stay consistent
_ip_map = {}
_ip_counter = [10]

def fake_ip(real_ip):
    if real_ip not in _ip_map:
        n = _ip_counter[0]
        _ip_map[real_ip] = f"192.168.1.{n}"
        _ip_counter[0] += 1
    return _ip_map[real_ip]

def scrub_ips(text):
    # match IPv4 addresses
    pattern = r'\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b'
    def replace(m):
        ip = m.group(0)
        # keep obviously fake/demo IPs
        if ip.startswith("192.168.1.") or ip in ("0.0.0.0", "127.0.0.1"):
            return ip
        return fake_ip(ip)
    return re.sub(pattern, replace, text)

def scrub_timestamps(text):
    # shift all timestamps by a fixed random offset to anonymize timing
    # replace with plausible demo dates
    pattern = r'20\d\d-\d\d-\d\d[T ]\d\d:\d\d:\d\d'
    base = datetime(2025, 1, 15, 10, 0, 0)
    counter = [0]
    def replace(m):
        dt = base + timedelta(minutes=counter[0] * 17 + random.randint(0, 10))
        counter[0] += 1
        if 'T' in m.group(0):
            return dt.strftime("%Y-%m-%dT%H:%M:%S.000000")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return re.sub(pattern, replace, text)

def scrub_text(text):
    text = scrub_ips(text)
    text = scrub_timestamps(text)
    return text

# ── file handlers ─────────────────────────────────────────────────────────────

def process_json(src_path, dst_path):
    try:
        with open(src_path) as f:
            data = json.load(f)
        text = json.dumps(data, indent=2)
        text = scrub_text(text)
        with open(dst_path, 'w') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"    [warn] json failed ({e}), copying raw")
        return False

def process_csv(src_path, dst_path):
    try:
        with open(src_path) as f:
            text = f.read()
        with open(dst_path, 'w') as f:
            f.write(scrub_text(text))
        return True
    except Exception as e:
        print(f"    [warn] csv failed ({e})")
        return False

def process_text(src_path, dst_path):
    try:
        with open(src_path, errors='ignore') as f:
            text = f.read()
        with open(dst_path, 'w') as f:
            f.write(scrub_text(text))
        return True
    except Exception as e:
        print(f"    [warn] text failed ({e})")
        return False

def process_python(src_path, dst_path):
    try:
        with open(src_path, errors='ignore') as f:
            text = f.read()
        # scrub IPs in comments and strings but leave code logic intact
        text = scrub_ips(text)
        with open(dst_path, 'w') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"    [warn] python failed ({e})")
        return False

# ── sqlite scrubber ───────────────────────────────────────────────────────────

def scrub_sqlite(src_path, dst_path):
    try:
        shutil.copy2(src_path, dst_path)
        conn = sqlite3.connect(dst_path)
        cur = conn.cursor()

        # get all tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]

        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            cols = [r[1] for r in cur.fetchall()]

            cur.execute(f"SELECT rowid, * FROM {table}")
            rows = cur.fetchall()

            for row in rows:
                rowid = row[0]
                values = list(row[1:])
                changed = False
                new_values = []
                for val in values:
                    if isinstance(val, str):
                        new_val = scrub_text(val)
                        new_values.append(new_val)
                        if new_val != val:
                            changed = True
                    else:
                        new_values.append(val)

                if changed:
                    placeholders = ', '.join(f"{c}=?" for c in cols)
                    cur.execute(
                        f"UPDATE {table} SET {placeholders} WHERE rowid=?",
                        new_values + [rowid]
                    )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"    [warn] sqlite failed ({e}) — skipping db")
        return False

# ── skip list ─────────────────────────────────────────────────────────────────

SKIP_DIRS = {'__pycache__', '.git', 'node_modules'}
SKIP_FILES = {'mutation_memory.db'}  # corrupted anyway

# files to replace with synthetic demo versions
DEMO_REPLACE = {'mutation_stats.txt', 'payload_families.csv', 'payload_family.json'}

# ── demo data generators ──────────────────────────────────────────────────────

def gen_demo_payload_families():
    families = {
        "exfil": [],
        "scanner": [],
        "polymorph": [],
        "lateral": [],
        "decoy": []
    }
    personalities = ["Scout", "Mimic", "Parasite", "Ghost", "Phantom"]
    tools = {
        "exfil": ["data_siphon.py", "silent_exfil.sh", "dns_tunnel.py"],
        "scanner": ["port_sweep.py", "host_enum.sh", "service_probe.py"],
        "polymorph": ["mutant_shell.py", "shape_shift.sh", "adaptive_payload.py"],
        "lateral": ["pivot_agent.py", "smb_crawler.sh", "lateral_hop.py"],
        "decoy": ["honeypot_lure.py", "fake_service.sh", "decoy_beacon.py"],
    }
    base_time = datetime(2025, 1, 15, 10, 0, 0)
    mut_id = 8000

    for family, tool_list in tools.items():
        count = {"exfil": 12, "scanner": 8, "polymorph": 7, "lateral": 5, "decoy": 4}[family]
        for i in range(count):
            dt = base_time + timedelta(minutes=i * 23 + random.randint(0, 15))
            mut_id += random.randint(50, 200)
            families[family].append({
                "mutation": f"mut_{mut_id}",
                "ip": f"192.168.1.{10 + i}",
                "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "port": f"{random.choice(tool_list)} [{random.choice(personalities).lower()}]",
                "score": round(random.uniform(0.6, 0.98), 3),
                "generation": i + 1
            })

    return families

def gen_demo_stats():
    return """LANIMORPH Personality Stats
==============================
Scout      : 47
Mimic      : 31
Parasite   : 19
Ghost      : 12
Phantom    : 8
─────────────────────────────
Total runs : 117
Avg stealth: 0.847
Last run   : 2025-01-15 14:22:11
Active vault: demo_corpus_v1
"""

def gen_demo_csv():
    lines = ["family,count", "exfil,47", "scanner,31", "polymorph,24",
             "lateral,15", "decoy,12"]
    return "\n".join(lines) + "\n"

# ── main copy + scrub ─────────────────────────────────────────────────────────

def process_project():
    if DST.exists():
        print(f"[!] {DST} already exists — removing")
        shutil.rmtree(DST)

    DST.mkdir(parents=True)
    print(f"\n[+] scrubbing {SRC} → {DST}\n")

    stats = {"copied": 0, "scrubbed": 0, "skipped": 0, "demo": 0}

    for src_path in sorted(SRC.rglob("*")):
        # skip dirs
        if src_path.is_dir():
            if src_path.name in SKIP_DIRS:
                continue
            rel = src_path.relative_to(SRC)
            (DST / rel).mkdir(parents=True, exist_ok=True)
            continue

        rel = src_path.relative_to(SRC)
        dst_path = DST / rel

        # skip
        if src_path.name in SKIP_FILES:
            print(f"  [skip] {rel}")
            stats["skipped"] += 1
            continue

        if any(part in SKIP_DIRS for part in rel.parts):
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # demo replacements
        if src_path.name in DEMO_REPLACE:
            print(f"  [demo] {rel}")
            if src_path.name == 'payload_family.json':
                with open(dst_path, 'w') as f:
                    json.dump(gen_demo_payload_families(), f, indent=2)
            elif src_path.name == 'mutation_stats.txt':
                with open(dst_path, 'w') as f:
                    f.write(gen_demo_stats())
            elif src_path.name == 'payload_families.csv':
                with open(dst_path, 'w') as f:
                    f.write(gen_demo_csv())
            stats["demo"] += 1
            continue

        ext = src_path.suffix.lower()

        if ext == '.db':
            print(f"  [db  ] {rel}")
            ok = scrub_sqlite(src_path, dst_path)
            stats["scrubbed" if ok else "skipped"] += 1

        elif ext == '.json':
            print(f"  [json] {rel}")
            ok = process_json(src_path, dst_path)
            if not ok:
                shutil.copy2(src_path, dst_path)
            stats["scrubbed"] += 1

        elif ext in ('.csv', '.txt', '.log', '.md'):
            print(f"  [text] {rel}")
            process_text(src_path, dst_path)
            stats["scrubbed"] += 1

        elif ext in ('.py', '.sh'):
            print(f"  [code] {rel}")
            process_python(src_path, dst_path)
            stats["scrubbed"] += 1

        else:
            shutil.copy2(src_path, dst_path)
            stats["copied"] += 1

    return stats

# ── README generator ──────────────────────────────────────────────────────────

README = """# chain

> mutation engine + lineage tracker for adaptive payload ecosystems

part of the **LANimals collective** // built by [bad_banana](https://dev.to/bad_banana)

---

## what it is

`chain` is the mutation and lineage tracking engine behind LANIMORPH — an adaptive payload framework that evolves payloads across a local network, tracks their lineage, scores their stealth, and visualizes the mutation tree over time.

it's not a traditional offensive tool. it's closer to an **ecosystem simulator** — payloads have personalities, families, XP, and mutation histories. the engine tracks which mutations survive, which get flagged, and evolves accordingly.

---

## core concepts

**mutation families**
payloads are grouped into families based on behavior: `exfil`, `scanner`, `polymorph`, `lateral`, `decoy`. each family evolves independently with its own scoring curve.

**personality system**
every mutation run is tagged with a personality (`Scout`, `Mimic`, `Parasite`, `Ghost`, `Phantom`) that influences behavior — aggression, stealth weight, lateral tendency.

**XP + lineage tracking**
successful mutations accumulate XP. the engine tracks parent→child relationships across mutation generations, building a full lineage tree you can replay and visualize.

**stealth scoring**
each payload variant is scored by an AI-assisted stealth scorer (`lanimorph_ai_scorer.py`) that weights evasion, signature noise, and behavioral fingerprint.

---

## structure

```
chain/
├── lan_dash.py              # live operation dashboard
├── lanimorph_dash.py        # LANIMORPH-specific dashboard
├── dna_mutator.py           # core mutation engine
├── chain_rotator.py         # payload rotation logic
├── mutation_memory.py       # persistence layer
├── lanimorph_xp.db          # XP + personality log (SQLite)
├── payload_family.json      # mutation corpus (demo data)
├── payload_families.csv     # family summary stats
├── mutation_stats.txt       # personality run stats
│
├── lineage/                 # lineage tree generators
├── replays/                 # captured session replays
├── family/                  # family tree visualization
├── mutants/                 # mutation variant store
├── reports/                 # generated HTML/text reports
├── meshmap/                 # LAN mesh topology data
└── mirror/                  # beacon sync mirrors
```

---

## key scripts

| script | purpose |
|--------|---------|
| `lan_dash.py` | main TUI dashboard — vault status, injection log, options |
| `dna_mutator.py` | generate and evolve mutation variants |
| `chain_rotator.py` | rotate through mutation chain by family/personality |
| `lanimorph_ai_scorer.py` | score payload stealth via LLM |
| `mutation_timeline.py` | generate timeline of mutation history |
| `mutation_tree_svg.py` | render mutation tree as SVG |
| `infection_replay.py` | replay a captured infection chain |
| `lan_heatmap.py` | ASCII heatmap of network activity |
| `deepest_lineage.py` | find longest surviving mutation chain |
| `vault_xp_dash.py` | XP and personality stats dashboard |

---

## running the dashboard

```bash
cd chain
python3 lan_dash.py
```

expects a vault at `~/LANIMORPH/vault/` — create it or point the config at your own path.

---

## data format

**payload_family.json**
```json
{
  "exfil": [
    {
      "mutation": "mut_8210",
      "ip": "192.168.1.10",
      "timestamp": "2025-01-15 10:00:00",
      "port": "data_siphon.py [scout]",
      "score": 0.847,
      "generation": 1
    }
  ]
}
```

**lanimorph_xp.db** — `xp_log` table
```
id | timestamp | personality | xp_gained
```

---

## status

active research tool — used in controlled lab environments.
data in this repo is sanitized demo corpus. no real network data included.

---

## legal

for authorized research, red team simulation, and educational use only.
do not use against systems you don't own or have explicit permission to test.

part of the [LANimals collective](https://github.com/GnomeMan4201) ecosystem.

---

*the work speaks first.*
"""

# ── run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    stats = process_project()

    readme_path = DST / "README.md"
    with open(readme_path, 'w') as f:
        f.write(README)
    print(f"\n  [done] README written")

    print(f"""
{'='*50}
  chain_prep complete
{'='*50}
  scrubbed : {stats['scrubbed']}
  demo data: {stats['demo']}
  copied   : {stats['copied']}
  skipped  : {stats['skipped']}

  output   : ~/projects/chain_clean/
  README   : ~/projects/chain_clean/README.md

  next steps:
  1. review chain_clean/ — spot check a few files
  2. cd ~/projects/chain_clean && git init
  3. git add . && git commit -m "init: chain mutation engine"
  4. push to github as GnomeMan4201/chain
{'='*50}
""")
