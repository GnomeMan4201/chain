#!/usr/bin/env bash
# LANIMORPH :: Auto Personality Fingerprinter

SUBNET="192.168.1.43/24"
SELF_IP=$(ip route get 1 | awk '{print $7; exit}')
TAG_LOG="$HOME/LANIMORPH/logs/personality_tags.log"

FAMILIES=(Scout Ghost Leech Parasite Observer Gremlin Crawler)

mkdir -p "$(dirname "$TAG_LOG")"
> "$TAG_LOG"

echo -e "\n🔍 Scanning $SUBNET...\n"

for IP in $(nmap -sn "$SUBNET" | grep "Nmap scan report" | awk '{print $5}'); do
  [[ "$IP" == "$SELF_IP" ]] && continue

  RANDOM_FAMILY="${FAMILIES[$RANDOM % ${#FAMILIES[@]}]}"
  echo "$IP 🧠 $RANDOM_FAMILY" | tee -a "$TAG_LOG"
done

echo -e "\n[✓] Personality tags saved to: $TAG_LOG"
