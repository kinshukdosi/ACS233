#include "Solenoid.h"
#include <string>

Solenoid::Solenoid(int pin, string name, int state){
    this->pin = pin;
    this->name = name;
    this->state = state;
}

void Solenoid::toggleState(){

}
