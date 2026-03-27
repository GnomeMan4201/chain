# chain

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
