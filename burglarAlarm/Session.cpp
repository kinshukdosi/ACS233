#include "Session.h"

// LED pins //
const byte pinLED_1 = 47;  // Digital
const byte pinLED_2 = 45;  // Digital
const byte pinLED_3 = 43;  // Digital
const byte pinLED_4 = 41;  // Digital
const byte pinLED_5 = 39;  // Doesn't have a physical LED

// Buzzer Pins //
const byte pinBuzzer_1 = 3;  // Digital
const byte pinBuzzer_2 = 22;  // Doesn't have a physical Buzzer
const byte pinBuzzer_3 = 24;  // Doesn't have a physical Buzzer
const byte pinBuzzer_4 = 26;  // Doesn't have a physical Buzzer
const byte pinBuzzer_5 = 28;  // Doesn't have a physical Buzzer

// Solenoid Pin //
const byte pinSolenoid_1 = 2; // Digital

// Day Sensor Pins //
const byte pinButton_1 = 49;  // Digital
const byte pinMagnetic_1 = 5; // Digital
const byte pinMagnetic_2 = 6; // Doesn't physically exist
const byte pinMagnetic_3 = 7; // Doesn't physically exist
const byte pinMagnetic_4 = 8; // Doesn't physically exist
const byte pinMagnetic_5 = 9; // Doesn't physically exist

// Night Sensor Pins
const byte pinMagnetic_6 = 10; // Doesn't physically exist
const byte pinMagnetic_7 = 11; // Doesn't physically exist
const byte pinMagnetic_8 = 12; // Doesn't physically exist
const byte pinMagnetic_9 = 13; // Doesn't physically exist
const byte pinPIR_1 = 53; // Digital
const byte pinPIR_2 = 51; // Doesn't physically exist


Session::Session(char systemMode){
    this->systemMode = systemMode; // Start in day mode
    this->timeDelay = 30000; // 30s to turn off alarm
    this->alarmOffTime = 10000; // 10s limit for the buzzer. 30*60*1,000=1,800,000 for 30 mins in a real life system
    this->timeTriggered = 0; // Default to 0, not used until sensor tripped
    this->alarmTriggered = false;
    this->prevAlarmTriggered = false;
    
    // Variables for receiving messages
    this->newMessage = false;
    this->receivedMessage[32];

    // Instantiate LEDs
    this->alarmLEDs[0] = new LED(pinLED_1, "REC_LED_1", 500);
    this->alarmLEDs[1] = new LED(pinLED_2, "REC_LED_2", 500);
    this->alarmLEDs[2] = new LED(pinLED_3, "GAL_LED_1", 500);
    this->alarmLEDs[3] = new LED(pinLED_4, "GAL_LED_2", 500);
    this->alarmLEDs[4] = new LED(pinLED_5, "GAL_LED_3", 500); // Doesn't exist physically
    
    // Instantiate Buzzers
    this->alarmBuzzers[0] = new Buzzer(pinBuzzer_1, "REC_BUZ_1", 200);
    this->alarmBuzzers[1] = new Buzzer(pinBuzzer_2, "REC_BUZ_2", 200); // Doesn't exist physically
    this->alarmBuzzers[2] = new Buzzer(pinBuzzer_3, "GAL_BUZ_1", 200); // Doesn't exist physically
    this->alarmBuzzers[3] = new Buzzer(pinBuzzer_4, "GAL_BUZ_2", 200); // Doesn't exist physically
    this->alarmBuzzers[4] = new Buzzer(pinBuzzer_5, "GAL_BUZ_3", 200); // Doesn't exist physically

    // Instantiate Day Sensors
    this->daySensors[0] = new Sensor(pinMagnetic_1, "GAL_CAS_1", true); 
    this->daySensors[1] = new Sensor(pinMagnetic_2, "GAL_CAS_3", true); // Doesn't exist physically
    this->daySensors[2] = new Sensor(pinMagnetic_3, "GAL_PAI_1", true);
    this->daySensors[3] = new Sensor(pinMagnetic_4, "GAL_PAI_2", true);
    this->daySensors[4] = new Sensor(pinMagnetic_5, "GAL_PAI_3", true);
    this->daySensors[5] = new Sensor(pinButton_1, "REC_BUT_1", false);

    // Instantiate Night Sensors
    this->nightSensors[0] = new Sensor(pinMagnetic_6, "REC_DOO_1", true);
    this->nightSensors[1] = new Sensor(pinMagnetic_7, "REC_DOO_2", true);
    this->nightSensors[2] = new Sensor(pinMagnetic_8, "GAL_WIN_1", true);
    this->nightSensors[3] = new Sensor(pinMagnetic_9, "GAL_WIN_2", true);
    this->nightSensors[4] = new Sensor(pinPIR_1, "REC_PIR_1", false);
    this->nightSensors[5] = new Sensor(pinPIR_2, "REC_PIR_2", false);
}

void Session::run(){
  // Check day mode sensors //
  if (systemMode == 'D' or systemMode == 'N')
  {
    if (checkSensors(daySensors, 5)) // Need to change 5 to 6 to include panic button. Button currently used as PIN code successful
    {
      alarmTriggered = true;
    }
  }
  
  // Check night mode sensors//
  if (systemMode == 'N')
  {
    if (checkSensors(nightSensors, 6))
    {
      alarmTriggered = true;
    }
  }
  
  // Check for pin //
  char sensorName[16];
  // Use button as PIN correct
    if ((*daySensors[5]).isTriggered()){
        alarmTriggered = false;
        (*daySensors[5]).getName(sensorName);
        Serial.println(sensorName);
    }
  
  // Activate alarm if necessary
  if (alarmTriggered){
      activateAlarm();
  }
  else {
      deactivateAlarm();
  }

  // Checks for a new message
  SerialRead();
  // Handles messages once received
  if(newMessage){
    SerialWrite('M', receivedMessage);
  }
}

void Session::SerialWrite(char prefix, char string[]){
    char message[17];
    message[0] = prefix;
    for (int i=0; i<16; i++){
      message[i+1] = string[i];
    }

    Serial.println(message);
}

void Session::SerialRead(){
  static boolean receiving = false;
  static byte index = 0;
  char startMarker = '<';
  char endMarker = '>';
  char receivedChar;
  int maxChars = 32;
    while(Serial.available() > 0 && newMessage == false){
        receivedChar = Serial.read();

        if(receiving == true){
            if(receivedChar != endMarker){
                receivedMessage[index] = receivedChar;
                index++;
                if(index >= maxChars){
                    index = maxChars - 1;
                }
            }
            else{
                receivedMessage[index] = '\0';
                receiving = false;
                index = 0;
                newMessage = true;
            }
        }
        else if (receivedChar == startMarker){
            receiving = true;
        }
    }
}

bool Session::checkSensors(Sensor* sensorArray[], int arrLen){
    char sensorName[16];
    bool sensorTripped = false;
    for (int i=0; i<arrLen; i++){
      if ((*sensorArray[i]).isTriggered()){
        sensorTripped = true;
        (*sensorArray[i]).getName(sensorName);
        SerialWrite('S', sensorName);
      }
    }
    return sensorTripped;
}

void Session::activateAlarm(){
  // Activate LEDs
  for (int i=0; i<3; i++){ // Change 3 to 5 when ready to use buzzer
    (*alarmLEDs[i]).on();
  }

  // Take time when alarm is first activated
  if (!prevAlarmTriggered){
    timeTriggered = millis();
  }

  if (millis() < timeTriggered + alarmOffTime){
    for (int i=0; i<1; i++){ // change 1 to 5 when ready to use buzzer
      (*alarmLEDs[3]).on(); // Green LED instead of buzzer
      // (*alarmBuzzers[i]).on();
    }
  }
  else {
    for (int i=0; i<1; i++){ // change 1 to 5 when ready to use buzzer
      (*alarmLEDs[3]).off(); // Green LED instead of buzzer
      // (*alarmBuzzers[i]).off();
    }
  }
  prevAlarmTriggered = true;
}

void Session::deactivateAlarm(){
  for (int i=0; i<5; i++){
    (*alarmLEDs[i]).off();
    (*alarmBuzzers[i]).off();
  }
  prevAlarmTriggered= false;
}
