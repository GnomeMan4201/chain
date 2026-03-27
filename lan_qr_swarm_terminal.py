import os
from pathlib import Path
import qrcode
from qrcode.console_scripts import main as qr_terminal

BUNDLE_DIR = Path.home() / "LANIMORPH/bundles/silent"
ZIP_FILES = list(BUNDLE_DIR.glob("silent_*.zip"))

if not ZIP_FILES:
    print("[x] No payload ZIPs found.")
    exit(1)

for zip_file in ZIP_FILES:
    print("=" * 60)
    print(f"[+] QR for: {zip_file.name}")
    print("=" * 60)
    qr = qrcode.QRCode(border=1)
    qr.add_data(f"file://{zip_file}")
    qr.make(fit=True)
    qr.print_ascii(invert=True)  # Terminal-safe ASCII QR
    print()
