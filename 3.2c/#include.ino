#include "thingProperties.h"


float ax, ay; 
// float az;   

void setup() {
  Serial.begin(9600);
  delay(1500);
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  // init your sensor here (DHT/Ultrasonic/IMU)
}

void loop() {
  ArduinoCloud.update();

  // 1) read sensor into sensorValue
  // sensorValue = ...;

  // 2) alarm logic (example threshold)
  // e.g., temperature > 40 or distance < 10
  if (sensorValue > 40.0) {
    alarmOn = true;    // device triggers alarm
  }
  // you can clear from dashboard by toggling alarmOn = false
}

void onAlarmOnChange() {
  }
