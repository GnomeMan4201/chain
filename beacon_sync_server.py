#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, os
LOG = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
class BeaconHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/sync"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            msg = query.get("msg", [""])[0]
            if msg:
                with open(LOG, "a") as f:
                    f.write(msg + "\n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
PORT = 7172
print(f"[~] BeaconSync listening on port {PORT}")
HTTPServer(("", PORT), BeaconHandler).serve_forever()
