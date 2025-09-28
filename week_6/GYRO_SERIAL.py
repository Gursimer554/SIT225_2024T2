# File: log_gyro_serial.py
# pip install pyserial pandas

import serial, csv, time
from datetime import datetime

PORT = "COM5"       # <-- change this
BAUD = 115200
OUT_CSV = "gyro.csv"

with serial.Serial(PORT, BAUD, timeout=2) as ser, open(OUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    header_written = False
    print("Reading serial... Ctrl+C to stop.")
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            # Expect header or "t,x,y,z"
            if not header_written:
                if "timestamp_ms" in line:
                    writer.writerow(line.split(","))
                else:
                    writer.writerow(["timestamp_ms","x","y","z"])
                    # then treat current as data if it looks numeric
                    if line.replace(",","").replace(".","").replace("-","").isdigit():
                        writer.writerow(line.split(","))
                header_written = True
            else:
                parts = line.split(",")
                if len(parts) == 4:
                    writer.writerow(parts)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Skip line:", e)

print("Saved to", OUT_CSV)
