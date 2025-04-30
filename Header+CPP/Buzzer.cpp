#include "Buzzer.h"
#include <string>

Buzzer::Buzzer(int pin, string name, int tone){
    this->pin = pin;
    this->name = name;
    this->tone = tone;
    this->buzzerCutOffTime = 0;
    this->buzzerActivatedTimestamp = 0;
}

void Buzzer::soundAlarm(){

}
