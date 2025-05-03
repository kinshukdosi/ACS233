#include <Arduino.h>
#include "Actuator.h"
using namespace std;

class Solenoid: public Actuator{
    //private:
        //int state;
    public:
        Solenoid();
        Solenoid(int pin, char name[]); //, int state);
        on();
        off();
        //void toggleState();
};