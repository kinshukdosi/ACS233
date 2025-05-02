#include <Arduino.h>
//#include "Sensor.h"
#include "Actuator.h"
#include "LED.h"
#include "Buzzer.h"
using namespace std;

#ifndef SESSION_H
#define SESSION_H

class Session{
    private:
        char systemMode;
        int timeDelay;
        int timeTriggered;

        void SerialWrite();
        void SerialRead();

        LED* alarmLEDs[5];
        Buzzer* alarmBuzzers[5];

    public:
        Session(char systemMode);
        void run();
};

#endif