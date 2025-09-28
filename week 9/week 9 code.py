// Smart Occupancy Logger: PIR + HC-SR04 (Arduino Uno/Nano)
// Pins: PIR OUT->D2, HC-SR04 TRIG->D3, ECHO->D4, +5V/GND to both
#define PIR_PIN 2
#define TRIG_PIN 3
#define ECHO_PIN 4

long readDistCM(){
  long v[5];
  for(int i=0;i<5;i++){
    digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    long us = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms
    v[i] = (us==0)? 9999 : (long)(us*0.034/2); // cm
    delay(10);
  }
  // median-of-5
  for(int i=0;i<5;i++) for(int j=i+1;j<5;j++) if(v[j]<v[i]){ long t=v[i]; v[i]=v[j]; v[j]=t; }
  return v[2];
}

unsigned long last_t=0; long last_d=0;

void setup(){
  pinMode(PIR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  Serial.begin(9600);
  Serial.println("time_ms,PIR,distance_cm,presence,event");
  last_d = readDistCM(); last_t = millis();
}

void loop(){
  int pir = digitalRead(PIR_PIN);
  long d  = readDistCM();
  int presence = (pir==HIGH && d < 120) ? 1 : 0;

  String event = "";
  long dd = last_d - d; // +ve = approaching
  if(pir==HIGH){
    if(dd > 20) event = "enter";
    else if(dd < -20) event = "exit";
    else if(presence) event = "dwell";
  }

  Serial.print(millis()); Serial.print(",");
  Serial.print(pir);     Serial.print(",");
  Serial.print(d);       Serial.print(",");
  Serial.print(presence);Serial.print(",");
  Serial.println(event);

  last_d = d; last_t = millis();
  delay(500);
}
