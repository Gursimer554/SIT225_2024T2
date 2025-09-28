# firebase_week5.py
import os, time, random, datetime as dt
import firebase_admin
from firebase_admin import credentials, db

# === CHANGE THESE TWO LINES ===
SERVICE_KEY = "C:\\Users\\gursi\Downloads\\SIT225_2024T2\\week_5\\week5-e1b95-firebase-adminsdk-fbsvc-a373c25129.json"   # 
DATABASE_URL = "https://week5-e1b95-default-rtdb.firebaseio.com/"  # 

# --- Connect to Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_KEY)
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

print("Connected to:", DATABASE_URL)

# Helpers
def now_iso():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# ===========================
# Q11: DHT22 - generate & insert random data, then query all
# ===========================
dht_ref = db.reference("/sensors/DHT22/nano33iot_01")

# Insert 10 random points
for _ in range(10):
    payload = {
        "temperature": round(random.uniform(18.0, 35.0), 1),
        "humidity":    round(random.uniform(30.0, 90.0), 1),
        "unit_t": "C",
        "unit_h": "%"
    }
    dht_ref.child(now_iso()).set(payload)
    time.sleep(0.2)

print("\n[Q11] DHT22 all data:")
dht_all = dht_ref.get()
print(dht_all if dht_all else "(no data)")

# ===========================
# Q12: SR04 - generate & insert random data, then query all
# ===========================
sr04_ref = db.reference("/sensors/SR04/nano33iot_01")

# Insert 10 random distance readings (in cm)
for _ in range(10):
    payload = {
        "distance_cm": round(random.uniform(5.0, 300.0), 1)
    }
    sr04_ref.child(now_iso()).set(payload)
    time.sleep(0.2)

print("\n[Q12] SR04 all data:")
sr04_all = sr04_ref.get()
print(sr04_all if sr04_all else "(no data)")

print("\nDone. Check Firebase Console paths:")
print("  /sensors/DHT22/nano33iot_01")
print("  /sensors/SR04/nano33iot_01")
