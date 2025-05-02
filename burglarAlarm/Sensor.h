#include <Arduino.h>
using namespace std;
#ifndef SENSOR_H
#define SENSOR_H

class Sensor{
    private:
        int pin; 
        char name[16];
        bool invertInput;
    public:
        Sensor();
        Sensor(int pin, char name[], bool invertInput);
        bool getState();
};

#endif