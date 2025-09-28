import serial
import time
import random
from datetime import datetime

# Change this to the correct port for your Arduino (check Arduino IDE > Tools > Port)
PORT = "COM3"       # e.g., "COM3" on Windows, "/dev/ttyUSB0" on Linux, "/dev/cu.usbmodemXXXX" on Mac
BAUD_RATE = 9600

# Open serial connection
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # wait for Arduino to reset

print("Python-Arduino communication started...")

while True:
    # 1. Send random number to Arduino
    num_to_send = random.randint(1, 5)  # e.g., blink LED 1–5 times
    ser.write(str(num_to_send).encode())
    print(f"[{datetime.now()}] Sent to Arduino: {num_to_send}")

    # 2. Wait for Arduino response
    line = ser.readline().decode().strip()
    if line:
        try:
            received_num = int(line)
            print(f"[{datetime.now()}] Received from Arduino: {received_num}")

            # 3. Sleep that many seconds
            print(f"Sleeping {received_num} seconds...")
            time.sleep(received_num)
            print(f"[{datetime.now()}] Done sleeping.")
        except ValueError:
            print(f"[{datetime.now()}] Invalid data received: {line}")

    time.sleep(1)  
