#include "Session.h"
#include <string>

Session::Session(char systemMode, int timeDelay,
    int timeTriggered,
    Sensor daySensors[12], Sensor nightSensors[12], 
    Actuator alarmActuactors[9], Actuator doorActuactors[9]){
        this->systemMode = systemMode;
        this->timeDelay = timeDelay;
        this->timeTriggered = timeTriggered;
        for (int i = 0; i < 12; ++i) {
            this->daySensors[i] = daySensors[i];
            this->nightSensors[i] = nightSensors[i];
        }
        for (int i = 0; i < 9; ++i) {
            this->alarmActuactors[i] = alarmActuactors[i];
            this->doorActuactors[i] = doorActuactors[i];
        }
    }

string Session::checkSensor(){
    return "";
}
void Session::activateAlarm(){

}
char Session::getState(){
    return systemMode;
}
void Session::setState(char desiredState){
    systemMode = desiredState;
}
void Session::writeToLog(int elapsedTime, string action, int userID, char mode){

}