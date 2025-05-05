#include <Arduino.h>
#include "Sensor.h"
#include "Actuator.h"
#include "LED.h"
#include "Buzzer.h"
#include "Solenoid.h"
using namespace std;

#ifndef SESSION_H
#define SESSION_H

class Session{
    private:
        char systemMode;
        int accessLevel;

        bool alarmTriggered;
        bool prevAlarmTriggered; // Used to detect change in state

        int timeDelay;
        unsigned long timeEntered;
        bool awaitingPIN;
        bool prevAwaitingPIN;

        unsigned long timeExited;
        bool awaitingExit;

        int alarmOffTime;
        unsigned long timeTriggered;
        

        // Variables for receiving messages
        bool newMessage;
        char receivedMessage[32];
        unsigned long sendDelay;
        unsigned long lastMessageTime;

        // Variables for checking the PIN
        char correctPIN[4];
        char pinAttempt[5];
        int pinAttempts;

        LED* alarmLEDs[5];
        Buzzer* alarmBuzzers[5];
        Sensor* daySensors[6];
        Sensor* nightSensors[6];
        Solenoid* doorLock;

        void SerialWrite(char prefix, char message[]);
        void SerialRead();

        bool checkSensors(Sensor* sensorArray[], int arrLen);
        void activateAlarm();
        void deactivateAlarm();

        boolean checkPin(char correctPIN[], char enteredPIN[]);

    public:
        Session(char systemMode);
        void run();
};

#endif
