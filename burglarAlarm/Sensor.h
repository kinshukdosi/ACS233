#include <Arduino.h>
using namespace std;
#ifndef SENSOR_H
#define SENSOR_H

class Sensor{
    private:
        int pin; 
        char name[16];
        bool invertInput;
        unsigned long debounceTimer;
        bool prevState;
    public:
        Sensor();
        Sensor(int pin, char name[], bool invertInput);
        getName(char* outputStr);
        bool getState();
        bool isTriggered();
};

#endif