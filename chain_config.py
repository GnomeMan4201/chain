# chain_config.py
# central path configuration for chain / LANIMORPH
# clone this repo, edit these paths, everything else reads from here

import os
from pathlib import Path

# ── base paths ────────────────────────────────────────────────────────────────
# change CHAIN_BASE to wherever you cloned this repo
# change VAULT_BASE to wherever your LANIMORPH vault lives
# if you keep the default layout (vault next to chain), nothing needs changing

CHAIN_BASE   = Path(__file__).parent
VAULT_BASE   = Path(os.environ.get("LANIMORPH_VAULT", "~/LANIMORPH/vault")).expanduser()
LOGS_BASE    = Path(os.environ.get("LANIMORPH_LOGS",  "~/LANIMORPH/logs")).expanduser()
MEMORY_BASE  = Path(os.environ.get("LANIMORPH_MEM",   "~/LANIMORPH/memory")).expanduser()

# ── vault paths ───────────────────────────────────────────────────────────────
VAULT_DROP       = VAULT_BASE / "vault_drop.txt"
VAULT_PAYLOADS   = VAULT_BASE / "payloads"
VAULT_METADATA   = VAULT_BASE / "metadata"
VAULT_TEMPLATES  = VAULT_BASE.parent / "vault_templates"
VAULT_XP_GRAPH   = VAULT_BASE / "vault_xp_graph.svg"

# ── log paths ─────────────────────────────────────────────────────────────────
INJECT_LOG       = LOGS_BASE / "inject_silent.log"
SILENT_LOG       = LOGS_BASE / "silent" / "inject_silent.log"
DIAGNOSTIC_LOG   = LOGS_BASE / "diagnostic"

# ── chain paths ───────────────────────────────────────────────────────────────
MUTATION_DB      = MEMORY_BASE / "mutation_memory.db"
MIRROR_RING      = CHAIN_BASE / "mirror" / "mirror_ring.txt"
REPLAY_EXPORT    = CHAIN_BASE / "replay_export.txt"

# ── quick setup ───────────────────────────────────────────────────────────────
def setup_vault():
    """create vault directory structure if it doesn't exist"""
    dirs = [
        VAULT_BASE,
        VAULT_PAYLOADS,
        VAULT_METADATA,
        VAULT_TEMPLATES,
        LOGS_BASE,
        LOGS_BASE / "silent",
        DIAGNOSTIC_LOG,
        MEMORY_BASE,
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    # touch log files
    for f in [VAULT_DROP, INJECT_LOG, SILENT_LOG]:
        if not f.exists():
            f.touch()
    print(f"[+] vault initialized at {VAULT_BASE}")

if __name__ == "__main__":
    setup_vault()
