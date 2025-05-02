#include <Arduino.h>
#include "Actuator.h"
using namespace std;

class LED: public Actuator{
    private:
        int flashFreq;
    public:
        LED();
        LED(int pin, char name[], int flashFreq);
        void flash();
};