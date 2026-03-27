#!/usr/bin/env python3
import os, zipfile, time
from datetime import datetime
log = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
outdir = os.path.expanduser("~/LANIMORPH/bundles/silent")

def bundle():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(outdir, f"silent_auto_{ts}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(log, arcname="inject_silent.log")
    print("[+] Auto-bundled log to:", zip_path)

if __name__ == "__main__":
    while True:
        bundle()
        time.sleep(3600)
