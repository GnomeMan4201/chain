import os, qrcode
from pathlib import Path

BUNDLE_DIR = Path.home() / "LANIMORPH/bundles/silent"
QR_DIR = Path.home() / "LANIMORPH/flyers/qrs"
QR_DIR.mkdir(parents=True, exist_ok=True)

for zip_path in BUNDLE_DIR.glob("silent_*.zip"):
    filename = zip_path.stem
    out_png = QR_DIR / f"{filename}.png"
    qr = qrcode.make(f"file://{zip_path}")
    out_png.write_bytes(qr.tobytes())
    print(f"[+] QR saved: {out_png}")
