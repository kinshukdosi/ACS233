#include <Arduino.h>
#include "Actuator.h"
using namespace std;

// Define Solenoid Class as a Child of Actuator //
class Solenoid: public Actuator{
    public:
        // Constructors
        Solenoid();
        Solenoid(int pin, char name[]);

        // redefine on() and off() to make more sense
        on();
        off();
};