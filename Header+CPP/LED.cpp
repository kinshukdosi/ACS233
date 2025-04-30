#include "LED.h"
#include <string>

LED::LED(int pin, string name, int flashFreq){
    this->pin = pin;
    this->name = name;
    this->flashFreq = flashFreq;
}
void LED::flash(){

}