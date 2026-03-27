#!/usr/bin/env python3
import random, os
victim = input("Enter target IP: ").strip()
vault = os.path.expanduser("~/LANIMORPH/vault/payloads")
payloads = [f for f in os.listdir(vault) if not f.startswith('.')]
chosen = random.choice(payloads)
print(f"[*] Sending payload to {victim} → {chosen}")
os.system(f"echo 'Simulated injection: {chosen}' >> ~/LANIMORPH/logs/inject_silent.log")
