#include <Arduino.h>
#include "Sensor.h"
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
        int alarmOffTime;
        unsigned long timeTriggered;
        bool alarmTriggered;
        bool prevAlarmTriggered; // Used to detect change in state

        
        // Variables for receiving messages
        bool newMessage;
        char receivedMessage[32];

        LED* alarmLEDs[5];
        Buzzer* alarmBuzzers[5];
        Sensor* daySensors[6];
        Sensor* nightSensors[6];

        void SerialWrite(char prefix, char message[]);
        void SerialRead();

        bool checkSensors(Sensor* sensorArray[], int arrLen);
        void activateAlarm();
        void deactivateAlarm();

    public:
        Session(char systemMode);
        void run();
};

#endif