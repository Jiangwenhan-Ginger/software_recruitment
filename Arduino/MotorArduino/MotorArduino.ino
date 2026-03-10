#include <Arduino.h>

const int JOYSTICK_PIN = A2;
const unsigned long INTERVAL = 100;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(19200);
  pinMode(JOYSTICK_PIN, INPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= INTERVAL) {
    previousMillis = currentMillis;

    int joystickValue = analogRead(JOYSTICK_PIN);

    int goalPosition = map(joystickValue, 0, 1023, 818, 511);

    byte instruction = 0x1E;
    
    byte lowBytePos = goalPosition & 0xFF;
    byte highBytePos = (goalPosition >> 8) & 0xFF;

    Serial.write(instruction);
    Serial.write(lowBytePos);
    Serial.write(highBytePos);
  }
}
