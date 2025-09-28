#include <Arduino_LSM6DS3.h>   // Built-in IMU on Nano 33 IoT

// Choose a safe sampling rate for Serial + Python + Firebase.
// 50 Hz = every 20 ms. Good quality, low drops.
const unsigned long SAMPLE_PERIOD_MS = 20;

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }  // wait for Serial on native USB boards

  if (!IMU.begin()) {
    Serial.println("ERR: IMU not found");
    while (1) { delay(1000); }
  }
  // Print a CSV header once (PC script can also ignore the header)
  Serial.println("timestamp_ms,gx_dps,gy_dps,gz_dps");
}

void loop() {
  static unsigned long last = 0;
  if (millis() - last >= SAMPLE_PERIOD_MS) {
    last += SAMPLE_PERIOD_MS;

    float gx, gy, gz;
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(gx, gy, gz); // degrees/second
      unsigned long t = millis();
      // CSV line: t,gx,gy,gz  (timestamp is device ms since boot)
      Serial.print(t); Serial.print(",");
      Serial.print(gx, 4); Serial.print(",");
      Serial.print(gy, 4); Serial.print(",");
      Serial.println(gz, 4);
    }
  }
}
