#include "Solenoid.h"

Solenoid::Solenoid(){ //, int state){
    this->pin = pin;
    //this->state = state;

    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    this->name[0] = '\0';
    
    pinMode(pin, OUTPUT);
    on();
}

Solenoid::Solenoid(int pin, char name[]){ //, int state){
    this->pin = pin;
    //this->state = state;

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

Solenoid::off(){
    digitalWrite(pin, HIGH);
}

Solenoid::on(){
    digitalWrite(pin, LOW);
}