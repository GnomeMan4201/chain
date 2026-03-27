#!/usr/bin/env bash
# LANIMORPH :: Listener Port + Payload Timeline

PORT_FILE="$HOME/LANIMORPH/chain/current_port.txt"
INJECT_DIR="$HOME/LANIMORPH/injections"

clear
echo "=========== LANIMORPH LISTENER DASHBOARD ==========="
echo -n "[+] Current Port     : "
[[ -f "$PORT_FILE" ]] && cat "$PORT_FILE" || echo "(none)"
echo -n "[+] Listener Status  : "
pgrep -f inject_listener.sh > /dev/null && echo "RUNNING" || echo "NOT RUNNING"
echo "-----------------------------------------------------"
echo "Recent Payloads:"
ls -lt "$INJECT_DIR" 2>/dev/null | head -n 10 | awk '{print "[✓] " $9, $6, $7, $8}'
echo "====================================================="
