#!/usr/bin/env python3
import os, zipfile
from datetime import datetime
from getpass import getpass
log = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out = os.path.expanduser(f"~/LANIMORPH/bundles/silent/silent_secure_{ts}.zip")
pw = os.environ.get("LAN_ZIP_PW", "banana")
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.setpassword(pw.encode())
    z.write(log, arcname="inject_silent.log")
print("[+] Encrypted bundle:", out)
