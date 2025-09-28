v// ==== DHT22 on Arduino Nano 33 IoT ====
// Library: "DHT sensor library" by Adafruit (Library Manager)
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
#define SAMPLE_MS 5000  // 5 seconds is reasonable for DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  dht.begin();
  // Optional: print a simple banner
  Serial.println("#DHT22,tempC,humidity");
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // Celsius

  if (isnan(h) || isnan(t)) {
    // Print nothing if bad read (keeps CSV clean), or print "NaN,NaN"
    Serial.println("NaN,NaN");
  } else {
    // CSV values only; Python will prepend timestamp
    Serial.print(t, 2);
    Serial.print(",");
    Serial.println(h, 2);
  }
  delay(SAMPLE_MS);
}
