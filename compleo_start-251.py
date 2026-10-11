# compleo_start.py
# Aufruf aus Home Assistant mit Argumenten: vehicle_type = "private" oder "business"

#!/usr/bin/env python3
import sys
import requests
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: compleo_start.py <vehicle_type>")
    sys.exit(1)

vehicle_type = sys.argv[1]

RFID_IDS = {
    "private": "xxx_YOUR_PRIVATE_RFID",
    "business": "xxx_YOUR_BUSINESS_RFID"
}

LOGIN_URL = "https://ebox.fritz.box/cgi_c_login"
START_URL = "https://ebox.fritz.box/cgi_c_ldp1.remote_control"
USERNAME = "admin"
PASSWORD = "xxx_YOUR_ADMIN_PASSWORD"

if vehicle_type not in RFID_IDS:
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} – Unknown vehicle_type: {vehicle_type}")
    sys.exit(1)

rfid = RFID_IDS[vehicle_type]

session = requests.Session()
login_payload = {"username": USERNAME, "password": PASSWORD}
resp = session.post(LOGIN_URL, data=login_payload, verify=False)
if resp.status_code != 200:
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} – Login fehlgeschlagen: {resp.status_code}")
    sys.exit(1)
    
payload = {
    "waittime": "0",
    "chargetime": "0",
    "contractID": rfid,
    "rfid_uid": rfid,
    "start_stop": "0",
    "currentByContract": "50",
    "userfreetextl": "",
    "userfreetext2": "",
    "sessionUUlD": "",
    "esid": ""
}
    
resp2 = session.post(START_URL, data=payload, verify=False)
if resp2.status_code == 200:
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} – Ladevorgang für {vehicle_type} gestartet")
else:
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} – Start fehlgeschlagen: {resp2.status_code}, {resp2.text}")
