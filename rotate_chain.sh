#!/data/data/com.termux/files/usr/bin/bash
vault=~/LANIMORPH/vault/payloads
log=~/LANIMORPH/logs/inject_silent.log
echo -e "\n[~] Rotating payload mutations across infected subnet...\n"
ips=$(grep 'Host compromised' "$log" | grep -oP '\d+\.\d+\.\d+\.\d+' | sort -u)

for ip in $ips; do
    p=$(ls "$vault" | shuf -n1)
    echo "[~] $ip ⇨ $p"
    echo "[ROTATE] [$(date '+%b %d %H:%M')] silent: Host RE-injected by you [ $ip ] using $p" >> "$log"
done

echo -e "\n[✓] Rotation complete. View updated log with: tail -n 20 $log\n"
