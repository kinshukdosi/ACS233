#include "LED.h"

LED::LED(int pin, char name[], int flashFreq){
    this->pin = pin;
    this->flashFreq = flashFreq;

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

// Flash function needs reworking
void LED::flash(){
    on();
    delay(flashFreq);
    off();
}