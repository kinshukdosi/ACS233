#include "Session.h"

// LED pins //
const byte pinLED_1 = 47;  // Digital
const byte pinLED_2 = 45;  // Digital
const byte pinLED_3 = 43;  // Digital
const byte pinLED_4 = 41;  // Digital
const byte pinLED_5 = 39;  // Doesn't have a physical LED

// Buzzer Pins //
const byte pinBuzzer_1 = 5;  // Digital
const byte pinBuzzer_2 = 6;  // Doesn't have a physical Buzzer
const byte pinBuzzer_3 = 7;//25;  // Doesn't have a physical Buzzer
const byte pinBuzzer_4 = 8;  // Doesn't have a physical Buzzer
const byte pinBuzzer_5 = 9;//27;  // Doesn't have a physical Buzzer

// Solenoid Pin //
const byte pinSolenoid_1 = 2; // Digital

// Day Sensor Pins //
const byte pinButton_1 = 49;  // Digital
const byte pinMagnetic_1 = 22; // Digital
const byte pinMagnetic_2 = 24; // Doesn't physically exist
const byte pinMagnetic_3 = 26; // Doesn't physically exist
const byte pinMagnetic_4 = 28; // Doesn't physically exist
const byte pinMagnetic_5 = 30; // Doesn't physically exist

// Night Sensor Pins
const byte pinMagnetic_6 = 10; // Doesn't physically exist
const byte pinMagnetic_7 = 29; // Doesn't physically exist
const byte pinMagnetic_8 = 12; // Doesn't physically exist
const byte pinMagnetic_9 = 13; // Doesn't physically exist
const byte pinPIR_1 = 53; // Digital
const byte pinPIR_2 = 52; // Doesn't physically exist


Session::Session(char systemMode){
    // System state variables
    this->systemMode = systemMode; // Start in day mode
    this->accessLevel = 0;

    // Alarm variables
    this->alarmTriggered = false;
    this->prevAlarmTriggered = false;

    // Delay before triggering alarm on entering building
    this->timeDelay = 5000; // (5s for testing) 60s to turn off alarm
    this->timeEntered = 0;
    this->awaitingPIN = false;
    this->prevAwaitingPIN = false;

    // Delay before triggering alarm on exiting the building
    this->timeExited = 0;
    this->awaitingExit = false;

    // Buzzer cut off variables
    this->alarmOffTime = 4000; // 4s limit for the buzzer. 30*60*1,000=1,800,000 for 30 mins in a real life system
    this->timeTriggered = 0; // Default to 0, not used until sensor tripped
    
    // Variables for receiving messages
    this->newMessage = false;
    this->receivedMessage[32];
    this->sendDelay = 80;
    this->lastMessageTime = 0;

    // Variables for dealing with PIN
    const char tempPIN[4] = {'1', '2', '3', '4'};
    memcpy(this->correctPIN, tempPIN, 4);
    this->pinAttempt[5] = "    ";
    this->pinAttempts = 0;

    // Instantiate Solenoid
    this->doorLock = new Solenoid(pinSolenoid_1, "REC_SOL_1");

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
    this->daySensors[1] = new Sensor(pinMagnetic_2, "GAL_CAS_2", true); // Doesn't exist physically
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
    this->nightSensors[5] = new Sensor(pinPIR_2, "GAL_PIR_1", false);
}

boolean Session::checkPin(char correctPIN[], char enteredPIN[]){
  boolean comparePINs = true;
  for (int i=0; i<4; i++){
      if (correctPIN[i] != enteredPIN[i+1]){
        boolean comparePINs = false;
      }
  }

  return comparePINs;
}

void Session::run(){
  // Send data to python
  /*
  char tempString[2] = "x";
  if (millis() > lastMessageTime + sendDelay){
      lastMessageTime = millis();

      // Send Access Level
      tempString[0] = accessLevel + 48; // add ASCII code for 0
      SerialWrite('a', tempString);

      // Send System Mode
      tempString[0] = systemMode;
      SerialWrite('m', tempString);

      // Send alarmTriggered
      if (alarmTriggered){
        SerialWrite('t', "T");
      }
      else{
        SerialWrite('t', "F");
      }
  }
  */

  // Check day mode sensors //
  if (systemMode == 'D'){
    (*doorLock).off();
    if (checkSensors(daySensors, 6)){
      alarmTriggered = true;
    }
  }
  
  // Check night mode sensors//
  if (systemMode == 'N'){
    (*doorLock).on();

    // Code for delay entering the PIN
    if (checkSensors(nightSensors, 6)){
      awaitingPIN = true;
    }

    if (!prevAwaitingPIN && awaitingPIN){
      timeEntered = millis();
    }
    prevAwaitingPIN = awaitingPIN;

    if (awaitingPIN && millis() > timeEntered + timeDelay){
        alarmTriggered = true;
    }

    if (awaitingExit && millis()> timeExited + timeDelay){
      awaitingExit = false;
    }

    if (checkSensors(daySensors, 6) && !awaitingExit){ // Need to change 5 to 6 to include panic button. Button currently used as PIN code successful
      alarmTriggered = true;
    }
  }

  if (systemMode == 'I'){
    alarmTriggered = false;
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
  if(newMessage){

    // Switches between Day ('D'), Night ('N') and Idle ('I') modes
    if (receivedMessage[0] == 'm'){
        if (systemMode == 'D' && receivedMessage[1] == 'N'){
          awaitingExit = true;
          timeExited = millis();
          accessLevel = 0;
        }
        systemMode = receivedMessage[1];
    }

    // Change to access level 2 if facial recognition is successful
    else if (receivedMessage[0] == 'f'){
        accessLevel = 2;
    }

    // Deal with PIN input
    else if (receivedMessage[0] == 'p')
    {
        // Checks if the entered PIN matches
        bool PINsMatch = checkPin(correctPIN, receivedMessage);
        //SerialWrite(receivedMessage[i+1], correctPIN);

        // If PIN is correct, log in and reset alarm
        if (PINsMatch){
            accessLevel = 1;
            pinAttempts = 0;
            awaitingPIN = false;
            alarmTriggered = false;
            SerialWrite('p', "s");
        }
        // If PIN is wrong
        else {
            pinAttempts +=1;
            if (pinAttempts == 3){
                alarmTriggered = true;
                SerialWrite('p', "F");
            } else {
                SerialWrite('p', "f");
            }
        }
    }
    // Changes the access level
    else if (receivedMessage[0] == 'a'){
      char tempAccessLevel = receivedMessage[1] - 48; // Subtract the ASCII code for 0
      if (tempAccessLevel <= accessLevel){
        accessLevel = tempAccessLevel;
      }
    }

    newMessage = false;
  }
}

void Session::SerialWrite(char prefix, char string[]){
    char message[17];
    message[0] = prefix;
    for (int i=0; i<16; i++){
      message[i+1] = string[i];
    }
    message[16] = '\0';

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
        SerialWrite('s', sensorName);
      }
    }
    return sensorTripped;
}

void Session::activateAlarm(){
  // Log out of GUI
  accessLevel = 0;

  // Activate LEDs
  for (int i=0; i<5; i++){ // Change 3 to 5 when ready to use buzzer
    (*alarmLEDs[i]).on();
  }

  // Take time when alarm is first activated
  if (!prevAlarmTriggered){
    timeTriggered = millis();
  }

  for (int i=0; i<5; i++){ // change 1 to 5 when ready to use buzzer
    (*alarmBuzzers[i]).on();
  }

  /*
  if (millis() < timeTriggered + alarmOffTime){
    for (int i=0; i<5; i++){ // change 1 to 5 when ready to use buzzer
      (*alarmBuzzers[i]).on();
    }
  }
  else {
    for (int i=0; i<5; i++){ // change 1 to 5 when ready to use buzzer
      (*alarmBuzzers[i]).off();
    }
  }
  prevAlarmTriggered = true;
  */
}

void Session::deactivateAlarm(){
  for (int i=0; i<5; i++){
    (*alarmLEDs[i]).off();
    (*alarmBuzzers[i]).off();
  }
  prevAlarmTriggered= false;
}
