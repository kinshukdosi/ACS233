#include <Arduino.h>
using namespace std;
#ifndef ACTUATOR_H
#define ACTUATOR_H

// Define Actuator Class
class Actuator{
    protected:
        // Private Attributes //
        int pin;
        char name[16];
        
    public:
        // Constructors //
        Actuator();
        Actuator(int pin, char name[]);

        // Methods //
        getName(char* outputStr);
        on();
        off();
};

#endif