#!/usr/bin/env python3
import socket, os, time, threading
from datetime import datetime

SCAN_TIMEOUT = 0.5
SUBNET_THREADS = 60
INFECT_LOG = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.168.1.45", 80))
        return s.getsockname()[0]
    except:
        return "unknown"

def get_infected_hosts(log_path):
    infected = set()
    if os.path.exists(log_path):
        with open(log_path) as f:
            for line in f:
                if "silent: Host compromised" in line:
                    parts = line.strip().split("[")
                    if len(parts) > 1:
                        ip = parts[-1].replace("]", "").strip()
                        infected.add(ip)
    return infected

def check_ip(ip, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SCAN_TIMEOUT)
        s.connect((ip, 80))
        s.close()
        results[ip] = True
    except:
        results[ip] = False

def scan_subnet(subnet):
    results = {}
    threads = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        t = threading.Thread(target=check_ip, args=(ip, results))
        threads.append(t)
        t.start()
        if len(threads) >= SUBNET_THREADS:
            for t in threads:
                t.join()
            threads.clear()
    for t in threads:
        t.join()
    return results

def draw_map(active, infected, local_ip):
    os.system("clear")
    print("🗺️  LANIMORPH :: LIVE SUBNET MAP")
    print("="*50)
    for ip in sorted(active):
        status = "🟢" if active[ip] else "🔴"
        tag = "[INFECTED]" if ip in infected else ""
        you = "(you)" if ip == local_ip else ""
        print(f"{status} {ip} {tag} {you}")
    print("="*50)
    print(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
    print("Press Ctrl+C to exit.")

def main():
    local_ip = get_local_ip()
    subnet = ".".join(local_ip.split(".")[:3])
    infected = get_infected_hosts(INFECT_LOG)

    while True:
        active = scan_subnet(subnet)
        draw_map(active, infected, local_ip)
        time.sleep(10)

if __name__ == "__main__":
    main()
