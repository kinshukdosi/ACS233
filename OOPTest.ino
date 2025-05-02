// INCLUDE CLASSES //
// #include "Actuator.h"
#include "LED.h"
#include "Buzzer.h"
#include "Solenoid.h"
#include "Sensor.h"

// PINS //
const byte pinMagnetic = 5; // Digital
const byte pinButton = 49;  // Digital
const byte pinPIR = 53;     // Digital

const byte pinSolenoid = 2; // Digital
const byte pinBuzzer = 3;   // Digital

const byte pinLED_R1 = 47;  // Digital
const byte pinLED_R2 = 45;  // Digital
const byte pinLED_Y = 43;   // Digital
const byte pinLED_G = 41;   // Digital

// INSTANTIATE OBJECTS //
Sensor Magnetic_1(pinMagnetic, "Rec_Mag_1", true);
Sensor Button_1(pinButton, "Rec_But_1", false);
Sensor PIR_1(pinPIR, "Rec_PIR_1", false);

Buzzer Buzzer_1(pinBuzzer, "Rec_Buz_1", 200);
Solenoid Solenoid_1(pinSolenoid, "Rec_Sol_1");

LED LED_R1(pinLED_R1, "Rec_LED_1", 200);
LED LED_R2(pinLED_R2, "Rec_LED_2", 400);
LED LED_Y(pinLED_Y, "Gal_LED_1", 600);
LED LED_G(pinLED_G, "Gal_LED_2", 800);

// SET UP //
void setup() {
  Serial.begin(9600);
}

// MAIN LOOP //
void loop() {
  //testLEDs();
  //testBuzzer();
  //testSolenoid();
  testMagnetic();
  testButton();
  testPIR();
}

// TEST FUNCTIONS //
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

void testMagnetic(){
    if (Magnetic_1.getState()){
      LED_R1.on();
    }
    else{
      LED_R1.off();
    }
}

void testButton(){
    if (Button_1.getState()){
      LED_R2.on();
    }
    else{
      LED_R2.off();
    }
}

void testPIR(){
  if (PIR_1.getState()){
    LED_Y.on();
  }
  else{
    LED_Y.off();
  }
}