#!/usr/bin/env bash
# LANIMORPH :: Real Payload Injector by Personality

FAMILY="$1"
TARGET="$2"

VAULT="$HOME/LANIMORPH/vault"

declare -A map
map["Scout"]="lan_worm.py"
map["Ghost"]="dns_beacon.sh"
map["Leech"]="clip_sniff.py"
map["Parasite"]="rev_shell.sh"
map["Observer"]="fingerprint_dump.py"
map["Gremlin"]="mic_drop_termux.sh"
map["Crawler"]="lanimals_roguescan.py"

# Validate
[[ -z "$FAMILY" || -z "$TARGET" ]] && { echo "[!] Usage: $0 <FAMILY> <TARGET_IP>"; exit 1; }

PAYLOAD="${map[$FAMILY]}"
PAYLOAD_PATH="$VAULT/$PAYLOAD"

if [[ ! -f "$PAYLOAD_PATH" ]]; then
  echo "[!] Payload file not found: $PAYLOAD_PATH"
  exit 1
fi

# Display injection info
echo -e "\n[+] Injecting payload family: $FAMILY"
echo "[+] Target IP: $TARGET"
echo "[+] Payload file: $PAYLOAD_PATH"

# Real injection simulation (replace with curl/wget/ssh later)
if timeout 1 ping -c 1 "$TARGET" &>/dev/null; then
  echo "[~] Simulated delivery: (POST $PAYLOAD_PATH → http://$TARGET:8080/inject)"
  echo "[✓] Delivered successfully to $TARGET"
else
  echo "[✗] Payload failed to deliver (host unreachable)."
fi
