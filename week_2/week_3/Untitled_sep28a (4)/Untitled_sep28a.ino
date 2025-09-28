#include "arduino_secrets.h"
#include "thingProperties.h"

void setup() {
  Serial.begin(9600);
  delay(1500);

  // Register Cloud properties and start the Cloud/Wi-Fi connection
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Optional: show connection diagnostics in Serial Monitor
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  // Keep the Cloud session alive
  ArduinoCloud.update();

  // Simulate a temperature every ~5 seconds and print it
  static unsigned long last = 0;
  if (millis() - last >= 5000) {
    randomtemperature = random(1, 101);   // 1..100
    Serial.print("randomTemperature = ");
    Serial.println(randomtemperature, 2);
    last = millis();
  }
}

// Callback required by the property (kept empty)
void onRandomtemperatureChange() { }
