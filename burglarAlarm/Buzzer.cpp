#include "Buzzer.h"

// Default Constructor //
Buzzer::Buzzer(){
    this->pin = 0;
    this->pitch = 200;
    this->name[0] = '\0';
    
    pinMode(pin, OUTPUT);
    off();
}

// Constructor //
Buzzer::Buzzer(int pin, char name[], int pitch){
    this->pin = pin;
    this->pitch = pitch;

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

// Sound Buzzer //
Buzzer::on(){
    tone(pin, pitch);
}

// Silence Buzzer //
Buzzer::off(){
    noTone(pin);
}
