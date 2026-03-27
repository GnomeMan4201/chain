#!/usr/bin/env python3
import os, json, time
from datetime import datetime
LOG = os.path.expanduser("~/LANIMORPH/logs/mirror/mirror_history.json")
def track_mutation(ip, payload_name):
    now = datetime.now().isoformat()
    data = {}
    if os.path.exists(LOG):
        try: data = json.load(open(LOG))
        except: data = {}
    data[ip] = {"payload": payload_name, "timestamp": now}
    with open(LOG, "w") as f: json.dump(data, f, indent=2)
