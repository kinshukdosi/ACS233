#include <Arduino.h>
using namespace std;
#ifndef SENSOR_H
#define SENSOR_H

// Define Sensor Class //
class Sensor{
    private:
        // Private Attributes //
        int pin; 
        char name[16];
        bool invertInput;
        unsigned long debounceTimer;
        bool prevState;
    public:
        // Constructors //
        Sensor();
        Sensor(int pin, char name[], bool invertInput);
        
        // Methods //
        getName(char* outputStr);
        bool getState();
        bool isTriggered();
};

#endif