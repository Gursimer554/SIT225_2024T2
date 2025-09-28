
import argparse
import os
import sys
from datetime import datetime
import serial
import time

# plotting deps (only needed for --plot)
import pandas as pd
import matplotlib.pyplot as plt

SENSOR_CHOICES = ["dht22", "hcsr04", "lsm6ds3"]

def ts_compact():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def make_filename(sensor):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{sensor}_{ts}.csv"

def log_from_serial(sensor, port, baud=115200, outdir="."):
    fn = os.path.join(outdir, make_filename(sensor))
    print(f"[INFO] Opening {port} @ {baud} …")
    ser = serial.Serial(port, baudrate=baud, timeout=2)
    time.sleep(2.0)  # give the port/bootloader a moment

    print(f"[INFO] Writing to {fn}")
    with open(fn, "a", encoding="utf-8") as f:
        # header row (optional)
        if sensor == "dht22":
            f.write("#timestamp,tempC,humidity\n")
        elif sensor == "hcsr04":
            f.write("#timestamp,distance_cm\n")
        elif sensor == "lsm6ds3":
            f.write("#timestamp,ax_g,ay_g,az_g\n")

        try:
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line:
                    continue
                if line.startswith("#"):  # ignore Arduino banner/header
                    continue

                # Clean spaces; keep CSV commas
                data = line.replace(" ", "")
                stamp = ts_compact()
                f.write(f"{stamp},{data}\n")
                f.flush()
                # Live echo for user
                print(f"{stamp},{data}")
        except KeyboardInterrupt:
            print("\n[INFO] Stopping logging (Ctrl+C).")
        finally:
            ser.close()
            print(f"[INFO] Saved: {fn}")

def plot_csv(path):
    # Heuristics: read header line; skip comments
    df = pd.read_csv(path, comment="#", header=None)
    # Detect column count
    if df.shape[1] == 3:
        # timestamp, tempC, humidity (DHT22)
        df.columns = ["timestamp", "tempC", "humidity"]
        x = range(len(df))
        plt.figure()
        plt.plot(x, df["tempC"]); plt.plot(x, df["humidity"])
        plt.title("DHT22: Temperature & Humidity vs Sample Index")
        plt.xlabel("Sample"); plt.ylabel("Value")
        plt.legend(["tempC", "humidity"])
        plt.tight_layout()
        plt.show()

    elif df.shape[1] == 2:
        # timestamp, distance (HC-SR04)
        df.columns = ["timestamp", "distance_cm"]
        x = range(len(df))
        plt.figure()
        plt.plot(x, df["distance_cm"])
        plt.title("HC-SR04: Distance vs Sample Index")
        plt.xlabel("Sample"); plt.ylabel("Distance (cm)")
        plt.tight_layout()
        plt.show()

    elif df.shape[1] == 4:
        # timestamp, ax, ay, az (LSM6DS3)
        df.columns = ["timestamp", "ax_g", "ay_g", "az_g"]
        x = range(len(df))
        plt.figure()
        plt.plot(x, df["ax_g"]); plt.plot(x, df["ay_g"]); plt.plot(x, df["az_g"])
        plt.title("LSM6DS3: Acceleration (g) vs Sample Index")
        plt.xlabel("Sample"); plt.ylabel("Acceleration (g)")
        plt.legend(["ax_g", "ay_g", "az_g"])
        plt.tight_layout()
        plt.show()
    else:
        print(f"[WARN] Unexpected column count {df.shape[1]}. First rows:\n", df.head())

def main():
    ap = argparse.ArgumentParser(description="SIT225 serial logger & plotter")
    ap.add_argument("--sensor", choices=SENSOR_CHOICES, help="which sensor you’re logging")
    ap.add_argument("--port", help="serial port (e.g., COM5 or /dev/ttyACM0)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--plot", help="path to a CSV to plot (skips logging)")
    args = ap.parse_args()

    if args.plot:
        plot_csv(args.plot)
        return

    if not (args.sensor and args.port):
        print("ERROR: For logging you must provide --sensor and --port. Use --help for examples.")
        sys.exit(1)

    log_from_serial(args.sensor, args.port, args.baud, args.outdir)

if __name__ == "__main__":
    main()
