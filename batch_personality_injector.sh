#!/usr/bin/env bash
# LANIMORPH :: Batch Personality Injector to Reachable IPs

TAG_LOG="$HOME/LANIMORPH/logs/personality_tags.log"
INJECTOR="$HOME/LANIMORPH/chain/inject_family_runner.sh"

echo -e "\n🧠 LANIMORPH :: Batch Personality Injector\n"

while read -r line; do
  IP=$(echo "$line" | awk '{print $1}')
  FAMILY=$(echo "$line" | awk '{print $3}')

  # Skip if either is empty
  [[ -z "$IP" || -z "$FAMILY" ]] && continue

  # Skip self
  [[ "$IP" == "192.168.1.33" ]] && continue

  # Ping check
  if timeout 1 ping -c 1 "$IP" &>/dev/null; then
    echo "[✓] Host reachable: $IP ($FAMILY)"
    bash "$INJECTOR" "$FAMILY" "$IP"
    echo "--------------------------------------------------"
  else
    echo "[✗] Skipping unreachable: $IP ($FAMILY)"
  fi

done < "$TAG_LOG"
