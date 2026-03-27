#!/data/data/com.termux/files/usr/bin/bash
echo
echo "[~] Starting autonomous chain rotation daemon..."
while true; do
    NOW="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[*] [$NOW] Rotating LAN payloads..." >> ~/LANIMORPH/logs/rotate_loop.log
    bash ~/LANIMORPH/chain/rotate_chain.sh >> ~/LANIMORPH/logs/rotate_loop.log 2>&1
    echo "[✓] [$NOW] Round complete." >> ~/LANIMORPH/logs/rotate_loop.log
    sleep 3600  # rotate every hour
done
