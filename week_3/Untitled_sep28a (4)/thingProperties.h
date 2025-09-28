#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

void onRandomtemperatureChange();

float randomtemperature;

void initProperties() {
  ArduinoCloud.addProperty(randomtemperature, READWRITE, ON_CHANGE, onRandomtemperatureChange);
}

const char SSID[] = "Test24";      // e.g. "OnePlus_10R_5G"
const char PASS[] = "sam123456";         // e.g. "sam123456"

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

