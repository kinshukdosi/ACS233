#include "Session.h"

// LED pins
const byte pinLED_1 = 47;  // Digital
const byte pinLED_2 = 45;  // Digital
const byte pinLED_3 = 43;  // Digital
const byte pinLED_4 = 41;  // Digital
const byte pinLED_5 = 39;  // Doesn't have a physical LED

// Buzzer Pins
const byte pinBuzzer_1 = 3;  // Digital
const byte pinBuzzer_2 = 22;  // Doesn't have a physical Buzzer
const byte pinBuzzer_3 = 24;  // Doesn't have a physical Buzzer
const byte pinBuzzer_4 = 26;  // Doesn't have a physical Buzzer
const byte pinBuzzer_5 = 28;  // Doesn't have a physical Buzzer

Session::Session(char systemMode){
    this->systemMode = 'D'; // Start in day mode
    this->timeDelay = 30000; // 30 seconds im milliseconds
    this->timeTriggered = 0; // Default to 0, not used until sensor tripped

    // Instantiate LEDs
    
    
    this->alarmLEDs[0] = new LED(pinLED_1, "LED1", 500);
    this->alarmLEDs[1] = new LED(pinLED_2, "LED2", 500);
    this->alarmLEDs[2] = new LED(pinLED_3, "LED3", 500);
    this->alarmLEDs[3] = new LED(pinLED_4, "LED4", 500);
    this->alarmLEDs[4] = new LED(pinLED_5, "LED5", 500); // Doesn't exist physically
    
    // Instantiate Buzzers
    this->alarmBuzzers[0] = new Buzzer(pinBuzzer_1, "Buz1", 200);
    this->alarmBuzzers[1] = new Buzzer(pinBuzzer_2, "Buz2", 200);
    this->alarmBuzzers[2] = new Buzzer(pinBuzzer_3, "Buz3", 200);
    this->alarmBuzzers[3] = new Buzzer(pinBuzzer_4, "Buz4", 200);
    this->alarmBuzzers[4] = new Buzzer(pinBuzzer_5, "Buz5", 200);
}

void Session::run(){

    for (int i=0; i<4; i++){
      (*alarmLEDs[i]).on();
      delay(1000);
    }

    for (int i=0; i<4; i++){
      (*alarmLEDs[i]).off();
      delay(1000);
    }

    for (int i=0; i<1; i++){
      (*alarmBuzzers[i]).on();
      delay(1000);
    }

    for (int i=0; i<1; i++){
      (*alarmBuzzers[i]).off();
      delay(1000);
    }
}

void Session::SerialWrite(){

}

void Session::SerialRead(){
  
}