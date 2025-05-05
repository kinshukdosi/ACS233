#include <Arduino.h>
#include "Actuator.h"
using namespace std;

// Define LED Class as Child of Actuator //
class LED: public Actuator{
    private:
        // Private Attributes //
        int flashFreq;
        unsigned long flashTimer;
        bool prevState;
    public:
        // Constructors //
        LED();
        LED(int pin, char name[], int flashFreq);

        // Redefine on() Method with Polymorphism //
        void on();
};