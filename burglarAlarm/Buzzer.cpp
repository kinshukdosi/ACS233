#include "Buzzer.h"

Buzzer::Buzzer(){
    this->pin = 0;
    this->pitch = 200;
    //this->buzzerCutOffTime = 0;
    //this->buzzerActivatedTimestamp = 0;

    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    this->name[0] = '\0';
    
    pinMode(pin, OUTPUT);
    off();
}

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
    tone(pin, pitch);
    Serial.print(pin);
    Serial.print(", ");
    Serial.println(pitch);
}

Buzzer::off(){
    noTone(pin);
}

/*
void Buzzer::soundAlarm(){

}
*/
