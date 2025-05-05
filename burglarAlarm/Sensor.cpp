#include "Sensor.h"

// Default Constructor //
Sensor::Sensor(){
    this->pin = 0;
    this->name[0] = '\0';
    this->debounceTimer = 0;
    this->prevState = getState();

    pinMode(pin, INPUT);
}

// Constructor //
Sensor::Sensor(int pin, char name[], bool invertInput){
    this->pin = pin;
    this->invertInput = invertInput;
    this->debounceTimer = 0;
    this->prevState = getState();
    
    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    int i = 0;
    do{
        this->name[i] = name[i];
        i++;
    } while (i<15 && name[i-1]!='\0');
    this->name[i] = '\0';
    
    pinMode(pin, INPUT);
}

// Gets the current value of the sensor //
bool Sensor::getState(){
    if (digitalRead(pin) != invertInput){ // equivalent to XOR gate
        return true;
    }
    else{
        return false;
    }
}

// Writes Sensor Name to Given Address
Sensor::getName(char* outputStr){
  for (int i=0; i<16; i++){
      outputStr[i] = name[i];
  }
}

// Returns when sensor is first activated //
bool Sensor::isTriggered(){
    bool currentState = getState();
    // Take rising edge and debounce signal
    if (currentState != prevState && millis()>debounceTimer+100){
        debounceTimer = millis();
        prevState = currentState;
        return currentState;
    }
    else{
        return false;
    }
}