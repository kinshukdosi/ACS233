#include "Actuator.h"
#include <string>


Actuator::Actuator(){
    pin = 0;
    name = "NULL";
}

Actuator::Actuator(int pin, string name){
    this->pin = pin;
    this->name = name;
}

