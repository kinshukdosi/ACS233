#include <Arduino.h>
#include "Sensor.h"
#include "Actuator.h"
#include "LED.h"
#include "Buzzer.h"
#include "Solenoid.h"
using namespace std;

#ifndef SESSION_H
#define SESSION_H

// Define Session Class //
class Session{
    private:
        // System state variables //
        char systemMode;
        int accessLevel;

        // Alarm variables //
        bool alarmTriggered;
        bool prevAlarmTriggered; // Used to detect change in state

        // Delay before triggering alarm on entering building
        int timeDelay;
        unsigned long timeEntered;
        bool awaitingPIN;
        bool prevAwaitingPIN;

        // Delay before triggering alarm on exiting the building
        unsigned long timeExited;
        bool awaitingExit;

        // Buzzer cut off variables //
        int alarmOffTime;
        unsigned long timeTriggered;

        // Variables for receiving messages //
        bool newMessage;
        char receivedMessage[32];
        unsigned long sendDelay;
        unsigned long lastMessageTime;

        // Variables for dealing with PIN //
        char correctPIN[4];
        char pinAttempt[5];
        int pinAttempts;

        // Arrays of Sensors and Actuators //
        LED* alarmLEDs[5];
        Buzzer* alarmBuzzers[5];
        Sensor* daySensors[6];
        Sensor* nightSensors[6];
        Solenoid* doorLock;

        // Serial Communication Methods //
        void SerialWrite(char prefix, char message[]);
        void SerialRead();

        // Take Inputs //
        bool checkSensors(Sensor* sensorArray[], int arrLen);
        boolean checkPin(char correctPIN[], char enteredPIN[]);

        // Turn Alarm on and Off //
        void activateAlarm();
        void deactivateAlarm();

    public:
        // Constructor //
        Session(char systemMode);

        // Main Porgram //
        void run();
};

#endif
