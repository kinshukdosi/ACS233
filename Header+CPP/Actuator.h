#include <string>
using namespace std;
#ifndef ACTUATOR_H
#define ACTUATOR_H

class Actuator{
    protected:
        int pin; 
        string name;
    public:
    Actuator();
    Actuator(int pin, string name);
};

#endif