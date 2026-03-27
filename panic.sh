#!/data/data/com.termux/files/usr/bin/bash
echo -e "\n[!] PANIC MODE ACTIVATED — Scrubbing traces..."
shred -u ~/LANIMORPH/logs/inject_silent.log 2>/dev/null
shred -u ~/LANIMORPH/logs/rotate_loop.log 2>/dev/null
shred -uzn5 ~/LANIMORPH/vault/payloads/* 2>/dev/null
echo "[✓] Logs and payloads wiped."
