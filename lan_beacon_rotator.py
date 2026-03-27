#!/usr/bin/env python3
import os, random, time
VAULT_DIR = os.path.expanduser("~/LANIMORPH/vault_templates")
DROP_PATH = "/data/data/com.termux/files/usr/tmp/vault_drop.txt"

def rotate():
    if not os.path.isdir(VAULT_DIR):
        print("[x] Vault not found:", VAULT_DIR)
        return
    files = [f for f in os.listdir(VAULT_DIR) if f.endswith(".txt")]
    if not files:
        print("[x] No .txt templates in vault.")
        return
    pick = random.choice(files)
    with open(os.path.join(VAULT_DIR, pick)) as f:
        content = f.read()
    with open(DROP_PATH, "w") as out:
        out.write(content)
    print(f"[✓] Beacon rotated to: {pick}")

while True:
    rotate()
    time.sleep(1800)  # every 30 min
