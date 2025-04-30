#include <string>
#include "Sensor.h"
#include "Actuator.h"
using namespace std;


class Session{
    private:
        char systemMode;
        int timeDelay;
        int timeTriggered;
       // We need to define the size of these lists more accurately
        Sensor daySensors[12]; 
        Sensor nightSensors[12];
        Actuator alarmActuactors[9];
        Actuator doorActuactors[9];
    string checkSensor();
    void activateAlarm();
    public:
    Session(char systemMode, int timeDelay,
        int timeTriggered,
        Sensor daySensors[12], Sensor nightSensors[12], 
        Actuator alarmActuactors[9], Actuator doorActuactors[9]);
    char getState();
    void setState(char desiredState);
    void writeToLog(int elapsedTime, string action, int userID, char mode);
};

