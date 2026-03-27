#!/usr/bin/env bash
VAULT="$HOME/LANIMORPH/vault_templates"
DST="/data/data/com.termux/files/usr/tmp/vault_drop.txt"
RAND=$(ls "$VAULT" | shuf -n1)

echo "[~] Selected: $RAND"
cat "$VAULT/$RAND" > "$DST"
echo "[✓] New mutation dropped: $DST"
