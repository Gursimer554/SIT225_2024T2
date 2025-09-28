// File: dht22_logger.ino
// Board: Arduino Nano 33 IoT
// Libs: "DHT sensor library" + "Adafruit Unified Sensor"
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  while (!Serial) {;}
  dht.begin();
  Serial.println("timestamp_ms,temperature_c,humidity_pct"); // CSV header
}

void loop() {
  static unsigned long t0 = millis();

  float h = dht.readHumidity();
  float t = dht.readTemperature(); // Celsius

  if (isnan(h) || isnan(t)) {
    // If sensor read fails, skip this sample
    delay(2000);
    return;
  }

  unsigned long ts = millis() - t0;

  Serial.print(ts); Serial.print(",");
  Serial.print(t, 2); Serial.print(",");
  Serial.println(h, 2);

  delay(2000); // every ~2 seconds (adjust as you like)
}
