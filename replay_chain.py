#!/usr/bin/env python3
import time
log = [
    "[Sep 06 03:48] Host compromised → 192.168.1.47",
    "[Sep 06 03:52] Screenshot exfiltrated → 192.168.1.40",
    "[Sep 06 03:54] Token dump received → 192.168.1.48",
    "[Sep 06 03:59] Silent beacon → 192.168.1.49",
]
print("\n🧬  LANIMORPH :: INFECTION REPLAY\n")
for entry in log:
    print(f" ↪ {entry}")
    time.sleep(0.6)
input("\n[Press Enter to return to dashboard]")
