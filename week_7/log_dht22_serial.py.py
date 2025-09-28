# File: log_dht22_serial.py
# Usage: python log_dht22_serial.py COM5 115200
# Linux/macOS port example: /dev/ttyACM0
import sys, csv, serial

port = sys.argv[1] if len(sys.argv) > 1 else "COM5"
baud = int(sys.argv[2]) if len(sys.argv) > 2 else 115200
out_csv = "dht22.csv"

with serial.Serial(port, baud, timeout=3) as ser, open(out_csv, "w", newline="") as f:
    wr = csv.writer(f)
    header_written = False
    print(f"Reading {port} at {baud}… Ctrl+C to stop. Writing -> {out_csv}")
    try:
        while True:
            line = ser.readline().decode("utf-8", "ignore").strip()
            if not line:
                continue
            # First line from Arduino is a header; write as-is
            if not header_written:
                if "timestamp_ms" in line:
                    wr.writerow(line.split(","))
                else:
                    # if Arduino header got missed, force our header:
                    wr.writerow(["timestamp_ms","temperature_c","humidity_pct"])
                    wr.writerow(line.split(","))
                header_written = True
            else:
                parts = line.split(",")
                if len(parts) == 3:
                    wr.writerow(parts)
    except KeyboardInterrupt:
        print("\nStopped. CSV saved:", out_csv)
