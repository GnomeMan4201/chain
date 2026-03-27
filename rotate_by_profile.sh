#!/data/data/com.termux/files/usr/bin/bash
vault=~/LANIMORPH/vault/payloads
log=~/LANIMORPH/logs/inject_silent.log
prof=~/LANIMORPH/profiles/assigned.txt
echo -e "\n[~] Rotating payloads based on personality profile...\n"

for line in $(cat "$prof"); do
    ip="${line%%:*}"
    profile="${line##*:}"
    case $profile in
        Scout)     pick=$(ls "$vault" | grep -E 'scan|map|fingerprint' | shuf -n1) ;;
        Leech)     pick=$(ls "$vault" | grep -E 'token|cookie|creds|exfil' | shuf -n1) ;;
        Mimic)     pick=$(ls "$vault" | grep -E 'mirror|skin|polymorph' | shuf -n1) ;;
        Prankster) pick=$(ls "$vault" | grep -E 'fake|prank|scream|flash' | shuf -n1) ;;
        Hunter)    pick=$(ls "$vault" | grep -E 'lateral|worm|crawl|chain' | shuf -n1) ;;
        *)         pick=$(ls "$vault" | shuf -n1) ;;
    esac
    echo "[~] $ip ⇨ [$profile] ⇨ $pick"
    echo "[PROFILE] [$(date '+%b %d %H:%M')] silent: Host re-injected by [$profile] using $pick @ $ip" >> "$log"
done

echo -e "\n[✓] Profile-based rotation complete. Tail log with:\n     tail -n 20 $log\n"
