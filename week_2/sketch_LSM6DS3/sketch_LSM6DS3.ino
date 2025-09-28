// ==== LSM6DS3 Accelerometer on Arduino Nano 33 IoT ====
// Library: "Arduino_LSM6DS3" (by Arduino)
#include <Arduino_LSM6DS3.h>

const unsigned long SAMPLE_MS = 100; // 10 Hz is fine for general motion

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  if (!IMU.begin()) {
    Serial.println("#ERROR:IMU");
    while (1) { delay(100); }
  }
  Serial.println("#LSM6DS3,ax_g,ay_g,az_g");
}

void loop() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az); // g units
    Serial.print(ax, 3); Serial.print(",");
    Serial.print(ay, 3); Serial.print(",");
    Serial.println(az, 3);
  }
  delay(SAMPLE_MS);
}
