#!/usr/bin/env bash
# LANIMORPH :: XP Vault Status (Minimal, Accurate)

DB="$HOME/LANIMORPH/chain/xp_log.db"
declare -A THRESHOLDS=( ["Scout"]=5 ["Exfil"]=3 ["Recon"]=5 ["Persist"]=4 )

# Validate XP table exists
sqlite3 "$DB" "SELECT 1 FROM xp LIMIT 1;" 2>/dev/null || {
  echo "[!] XP table not found. Run: patch_xp_table.py"
  exit 1
}

echo -e "\n🧠 XP VAULT STATUS (No Gamification)\n"

for fam in "${!THRESHOLDS[@]}"; do
  count=$(sqlite3 "$DB" "SELECT COALESCE(SUM(points), 0) FROM xp WHERE payload_family='$fam';")
  target=${THRESHOLDS[$fam]}
  printf "%-8s %2s / %s XP\n" "$fam" "$count" "$target"
done
