#include "Sensor.h"
#include <string>


Sensor::Sensor(){
    this->pin = 0;
    this->name = "NULL";
}

Sensor::Sensor(int pin, string name){
    this->pin = pin;
    this->name = name;
}

int Sensor::getState(){
    return 0;
}