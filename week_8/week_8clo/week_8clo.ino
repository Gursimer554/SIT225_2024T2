from arduino_iot_cloud import ArduinoCloudClient
from datetime import datetime

# 1. Connect to Arduino Cloud
client = ArduinoCloudClient(device_id="YOUR_DEVICE_ID", secret_key="YOUR_SECRET_KEY")

# 2. Define variables
accel_x = client.register("accel_x")
accel_y = client.register("accel_y")
accel_z = client.register("accel_z")

# 3. Open CSV files for writing
file_x = open("accel_x.csv", "a")
file_y = open("accel_y.csv", "a")
file_z = open("accel_z.csv", "a")

def callback_x(value):
    ts = datetime.now().isoformat()
    file_x.write(f"{ts},{value}\n")
    file_x.flush()

def callback_y(value):
    ts = datetime.now().isoformat()
    file_y.write(f"{ts},{value}\n")
    file_y.flush()

def callback_z(value):
    ts = datetime.now().isoformat()
    file_z.write(f"{ts},{value}\n")
    file_z.flush()

# 4. Attach callbacks
accel_x.on_update(callback_x)
accel_y.on_update(callback_y)
accel_z.on_update(callback_z)

# 5. Keep listening
client.start()
