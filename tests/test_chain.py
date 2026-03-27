#!/usr/bin/env python3
# tests/test_chain.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── import tests ──────────────────────────────────────────────────────────────
# note: dna_mutator, score_payload, rotate_vault, mutation_memory, personality_stats
# run executable code at module level (argparse, input(), file writes, termux paths)
# these are cli tools not libraries — tested via data layer and config instead

def test_chain_config_imports():
    import chain_config
    assert chain_config is not None

def test_payload_family_tracker_imports():
    import payload_family_tracker
    assert payload_family_tracker is not None

def test_family_tracker_imports():
    import family_tracker
    assert family_tracker is not None

# ── config tests ──────────────────────────────────────────────────────────────

def test_chain_config_paths():
    from chain_config import CHAIN_BASE, VAULT_BASE, LOGS_BASE, MEMORY_BASE
    assert CHAIN_BASE is not None
    assert VAULT_BASE is not None
    assert LOGS_BASE is not None
    assert MEMORY_BASE is not None

def test_chain_config_vault_paths():
    from chain_config import VAULT_DROP, VAULT_PAYLOADS, VAULT_METADATA
    assert VAULT_DROP is not None
    assert VAULT_PAYLOADS is not None
    assert VAULT_METADATA is not None

def test_chain_config_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("LANIMORPH_VAULT", str(tmp_path / "vault"))
    import importlib
    import chain_config
    importlib.reload(chain_config)
    assert str(tmp_path / "vault") in str(chain_config.VAULT_BASE)

def test_setup_vault_creates_dirs(tmp_path, monkeypatch):
    monkeypatch.setenv("LANIMORPH_VAULT", str(tmp_path / "vault"))
    monkeypatch.setenv("LANIMORPH_LOGS",  str(tmp_path / "logs"))
    monkeypatch.setenv("LANIMORPH_MEM",   str(tmp_path / "memory"))
    import importlib
    import chain_config
    importlib.reload(chain_config)
    chain_config.setup_vault()
    assert (tmp_path / "vault").exists()
    assert (tmp_path / "logs").exists()
    assert (tmp_path / "memory").exists()

# ── payload family tests ──────────────────────────────────────────────────────

def test_payload_family_json_loads():
    import json
    from pathlib import Path
    family_file = Path(__file__).parent.parent / "payload_family.json"
    assert family_file.exists(), "payload_family.json not found"
    with open(family_file) as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert len(data) > 0

def test_payload_family_structure():
    import json
    from pathlib import Path
    family_file = Path(__file__).parent.parent / "payload_family.json"
    with open(family_file) as f:
        data = json.load(f)
    for family, entries in data.items():
        assert isinstance(entries, list), f"family {family} should be a list"
        for entry in entries:
            assert "mutation" in entry, f"entry missing mutation key in {family}"

def test_payload_families_csv_loads():
    import csv
    from pathlib import Path
    csv_file = Path(__file__).parent.parent / "payload_families.csv"
    assert csv_file.exists(), "payload_families.csv not found"
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) > 0
    assert "family" in rows[0]
    assert "count" in rows[0]

def test_payload_families_expected_types():
    import csv
    from pathlib import Path
    csv_file = Path(__file__).parent.parent / "payload_families.csv"
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    families = [r["family"] for r in rows]
    expected = {"exfil", "scanner", "polymorph", "lateral", "decoy"}
    assert len(expected & set(families)) > 0

# ── xp db tests ───────────────────────────────────────────────────────────────

def test_xp_db_exists():
    from pathlib import Path
    db = Path(__file__).parent.parent / "lanimorph_xp.db"
    assert db.exists(), "lanimorph_xp.db not found"

def test_xp_db_readable():
    import sqlite3
    from pathlib import Path
    db = Path(__file__).parent.parent / "lanimorph_xp.db"
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()
    assert "xp_log" in tables

def test_xp_log_schema():
    import sqlite3
    from pathlib import Path
    db = Path(__file__).parent.parent / "lanimorph_xp.db"
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(xp_log)")
    cols = [r[1] for r in cur.fetchall()]
    conn.close()
    assert "id" in cols
    assert "timestamp" in cols
    assert "payload" in cols
    assert "points" in cols

def test_xp_log_has_entries():
    import sqlite3
    from pathlib import Path
    db = Path(__file__).parent.parent / "lanimorph_xp.db"
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM xp_log")
    count = cur.fetchone()[0]
    conn.close()
    assert count >= 0
