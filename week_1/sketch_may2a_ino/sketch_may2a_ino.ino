int ledPin = LED_BUILTIN;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);  // standard baud rate for communication
  randomSeed(analogRead(0)); // seed randomness
}

void loop() {
  if (Serial.available() > 0) {
    // Step 1: Read number from Python
    int blinkCount = Serial.parseInt();
    
    // Step 2: Blink LED that many times (1 sec interval)
    for (int i = 0; i < blinkCount; i++) {
      digitalWrite(ledPin, HIGH);
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
    }

    // Step 3: Send random number back to Python
    int rnd = random(1, 6);   // random 1–5 seconds
    Serial.println(rnd);
  }
}



