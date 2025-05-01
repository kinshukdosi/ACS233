#include "Actuator.h"
#include "LED.h"
#include "Buzzer.h"
#include "Solenoid.h"

const byte pinSolenoid = 2; // Digital
const byte pinBuzzer = 3;   // Digital

const byte pinLED_R1 = 47;  // Digital
const byte pinLED_R2 = 45;  // Digital
const byte pinLED_Y = 43;   // Digital
const byte pinLED_G = 41;   // Digital

Buzzer Buzzer_1(pinBuzzer, "B1", 200);
Solenoid Solenoid_1(pinSolenoid, "S1");

LED LED_R1(pinLED_R1, "R1", 200);
LED LED_R2(pinLED_R2, "R2", 400);
LED LED_Y(pinLED_Y, "Y1", 600);
LED LED_G(pinLED_G, "G1", 800);

void setup() {
  Serial.begin(9600);
}

void loop() {
  //testLEDs();
  //testBuzzer();
  testSolenoid();
}

void testLEDs() {
  LED_R1.on();
  delay(200);
  LED_R2.on();
  delay(200);
  LED_Y.on();
  delay(200);
  LED_G.on();
  delay(1000);

  LED_R1.off();
  delay(200);
  LED_R2.off();
  delay(200);
  LED_Y.off();
  delay(200);
  LED_G.off();
  delay(1000);

  LED_R1.flash();
  LED_R2.flash();
  LED_Y.flash();
  LED_G.flash();
  delay(1000);
}

void testBuzzer(){
  Buzzer_1.on();
  delay(1000);
  Buzzer_1.off();
  delay(1000);
}

void testSolenoid(){
    Solenoid_1.on();
    delay(3000);
    Solenoid_1.off();
    delay(1000);
}