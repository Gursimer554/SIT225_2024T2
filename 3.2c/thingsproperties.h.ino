#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

// ---- WIFI ----
const char SSID[] = "Test24";
const char PASS[] = "sam123456";

// ---- CLOUD VARIABLES ----
float sensorValue;   // 
bool  alarmOn;       // 

void onAlarmOnChange();  // 

void initProperties() {
  ArduinoCloud.addProperty(sensorValue, READ, 1 * SECONDS, NULL);
  ArduinoCloud.addProperty(alarmOn, READWRITE, ON_CHANGE, onAlarmOnChange);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
