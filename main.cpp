#include <iostream>
#include <string>
using namespace std;


int main(){
    return 0;
}

class Sensor{
    private:
        int pin; 
        string name;
        string area;
    public:
    Sensor(){
        pin = 0;
        name = "NULL";
        area = "NULL";
    }
    Sensor(int pin, string name, string area){
        pin = pin;
        name = name;
        area = area;
    }
    int getState(){
        // Function to get the state of the sensor (high/low)
        return 0;
    }
};

class Actuator{
    private:
        int pin;
        string name;
    public:
    Actuator(){
        pin = 0;
        name = "NULL";
    }
    Actuator(int pin, string name){
        pin = pin;
        name = name;
    }
    void setActuator(int val){
        // Function to set the actuator on/off
    }
};

class Session{
    private:
        char systemMode;
        int accessLevel;
        int timeDelay;
        int timeTriggered;
        int alarmLength;
        int timeAlarmActivated;

        // We need to define the size of these lists more accurately
        Sensor daySensors[12]; 
        Sensor nightSensors[12];
        Actuator alarmActuactors[9];
        Actuator doorActuactors[9];


    string checkSensor(){
        // Not sure what this function is for?

        // NOTE that according to class diagram it should return a 
        // list of strings but I couldn't figure out how to code 
        // that, might need to use a struct
        return "";
    }
    
    void activateAlarm(){
        // Code to activate alarm
    }

    void activateActuators(Actuator actuatorArray[9]){
        // Code to activate the actuators passed in
    }

    void deactivateActuators(Actuator actuatorArray[9]){
        // Code to deactivate the actuators passed in
    }

    void removeExpiredLogs(){
        // Code to remove expired logs
    }

    public:
    Session(char systemMode, int accessLevel, int timeDelay,
        int timeTriggered, int alarmLength, int timeAlarmActivated,
        Sensor daySensors[12], Sensor nightSensors[12], 
        Actuator alarmActuactors[9], Actuator doorActuactors[9]){
            systemMode = systemMode;
            accessLevel = accessLevel;
            timeDelay = timeDelay;
            timeTriggered = timeTriggered;
            alarmLength = alarmLength;
            timeAlarmActivated = timeAlarmActivated;
            daySensors[12] = daySensors[12];
            nightSensors[12] = nightSensors[12];
            alarmActuactors[9] = alarmActuactors[9];
            doorActuactors[9] = doorActuactors[9];
    }

    void runSession(){
        // Code to start session
    }

    char getState(){
        return systemMode;
    }

    void setState(char desiredState){
        systemMode = desiredState;
    }

    void writeToLog(int elapsedTime, string action, int userID, char mode){
        // Code to write to audit log
    }
};

