#include "LED.h"

// Default Constructor //
LED::LED(){
    this->pin = 0;
    this->flashFreq = 200;
    this->flashTimer = 0;
    this->prevState = false;
    this->name[0] = '\0';

    pinMode(pin, OUTPUT);
    off();
}

// Constructor //
LED::LED(int pin, char name[], int flashFreq){
    this->pin = pin;
    this->flashFreq = flashFreq;
    this->flashTimer = 0;
    this->prevState = false;

    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    int i = 0;
    do{
        this->name[i] = name[i];
        i++;
    } while (i<15 && name[i-1]!='\0');
    this->name[i] = '\0';

    pinMode(pin, OUTPUT);
    off();
}

// Flashes LED //
void LED::on(){
    if (millis() > flashTimer+flashFreq){
        flashTimer = millis();
        if (prevState){
            digitalWrite(pin, LOW);
            prevState = false;
        }
        else{
            digitalWrite(pin, HIGH);
            prevState = true;
        }
    }
}