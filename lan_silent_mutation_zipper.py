#!/usr/bin/env python3
import os
import zipfile
from datetime import datetime

LOG = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
DROP = os.path.expanduser("/data/data/com.termux/files/usr/tmp/vault_drop.txt")
OUTDIR = os.path.expanduser("~/LANIMORPH/bundles/silent/")

os.makedirs(OUTDIR, exist_ok=True)

if not os.path.exists(LOG):
    print("[!] No inject_silent.log found.")
    exit(1)

with open(LOG, "r") as f:
    lines = [l.strip() for l in f if "Host compromised" in l]

for line in lines:
    try:
        ts, meta = line.split("::", 1)
        ip = meta.split("[")[1].split("]")[0].strip()
        stamp = datetime.strptime(ts.strip(), "%Y-%m-%d_%H:%M:%S").strftime("%Y%m%d_%H%M%S")
        zipname = os.path.join(OUTDIR, f"silent_{ip.replace('.','_')}_{stamp}.zip")

        with zipfile.ZipFile(zipname, 'w') as z:
            z.write(LOG, arcname="inject_silent.log")
            if os.path.exists(DROP):
                z.write(DROP, arcname="vault_drop.txt")

        print(f"[+] Bundled: {zipname}")
    except Exception as e:
        print(f"[!] Failed to zip line: {line[:60]}... :: {e}")
