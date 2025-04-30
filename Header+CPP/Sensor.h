#include <string>
using namespace std;
#ifndef SENSOR_H
#define SENSOR_H

class Sensor{
    private:
        int pin; 
        string name;
    public:
    Sensor();
    Sensor(int pin, string name);
    int getState();
};

#endif