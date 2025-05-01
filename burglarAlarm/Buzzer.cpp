#include "Buzzer.h"

Buzzer::Buzzer(int pin, char name[], int pitch){
    this->pin = pin;
    this->pitch = pitch;
    //this->buzzerCutOffTime = 0;
    //this->buzzerActivatedTimestamp = 0;

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

Buzzer::on(){
    tone(pin, tone);
}

Buzzer::off(){
    noTone(pin);
}

/*
void Buzzer::soundAlarm(){

}
*/
