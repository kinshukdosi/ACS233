#include <Arduino.h>
using namespace std;
#ifndef ACTUATOR_H
#define ACTUATOR_H

class Actuator{
    protected:
        int pin;
        char name[16];
        
    public:
        Actuator();
        Actuator(int pin, char name[]);
        getName(char* outputStr);
        on();
        off();
};

#endif