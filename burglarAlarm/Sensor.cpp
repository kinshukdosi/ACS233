#include "Sensor.h"

Sensor::Sensor(){
    this->pin = 0;
    this->name[0] = '\0';
}

Sensor::Sensor(int pin, char name[], bool invertInput){
    this->pin = pin;
    this->invertInput = invertInput;
    
    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    int i = 0;
    do{
        this->name[i] = name[i];
        i++;
    } while (i<15 && name[i-1]!='\0');
    this->name[i] = '\0';

    pinMode(pin, INPUT_PULLUP);
}

bool Sensor::getState(){
    if (digitalRead(pin) != invertInput){ // equivalent to XOR gate
        return true;
    }
    else{
        return false;
    }
}