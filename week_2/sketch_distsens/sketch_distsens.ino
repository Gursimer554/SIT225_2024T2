
const int TRIG_PIN = 3;
const int ECHO_PIN = 4;
const unsigned long SAMPLE_MS = 1000; // ~1 Hz

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.println("#HCSR04,distance_cm");
}

void loop() {
  // Trigger ultrasonic burst
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo time (timeout 25ms ~ 4.3m)
  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 25000UL);

  if (duration == 0) {
    Serial.println("NaN");
  } else {
    // distance in cm: duration/2 / 29.1
    float cm = (duration * 0.5f) / 29.1f;
    Serial.println(cm, 2);
  }
  delay(SAMPLE_MS);
}
