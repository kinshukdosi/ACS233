#include <Arduino.h>
#include "Actuator.h"
using namespace std;

class Buzzer: public Actuator{
    private:
        int pitch; // Changed tone to pitch as it cause issues with tone() function
        //int buzzerCutOffTime;
        //int buzzerActivatedTimestamp;
    public:
        Buzzer(int pin, char name[], int pitch);
        //void soundAlarm();
        on();
        off();
};