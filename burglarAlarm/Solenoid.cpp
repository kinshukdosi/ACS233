#include "Solenoid.h"

// Default Constructor //
Solenoid::Solenoid(){
    this->pin = pin;
    this->name[0] = '\0';
    
    pinMode(pin, OUTPUT);
    on();
}

// Constructor //
Solenoid::Solenoid(int pin, char name[]){
    this->pin = pin;

    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    int i = 0;
    do{
        this->name[i] = name[i];
        i++;
    } while (i<15 && name[i-1]!='\0');
    this->name[i] = '\0';
    
    pinMode(pin, OUTPUT);
    on();
}

// Unlock Door //
Solenoid::off(){
    digitalWrite(pin, HIGH);
}

// Lock Door //
Solenoid::on(){
    digitalWrite(pin, LOW);
}