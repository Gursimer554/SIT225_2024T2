

#include <Arduino_LSM6DS3.h>

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }              // wait for serial to be ready
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1) { ; }
  }
  Serial.println("timestamp_ms,x,y,z"); // CSV header
}

void loop() {
  float gx, gy, gz;
  static unsigned long t0 = millis();

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);     // deg/s
    unsigned long t = millis() - t0;   // relative ms since start

    // CSV line
    Serial.print(t); Serial.print(",");
    Serial.print(gx, 6); Serial.print(",");
    Serial.print(gy, 6); Serial.print(",");
    Serial.println(gz, 6);
  }
  delay(100); // ~10 Hz
}

