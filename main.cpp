#include <iostream>
#include <string>
using namespace std;

// this is pseudo setup that needs to be in the setup to initialise connection to interface
void pseudoSetup(){
    Serial.begin(9600);
    Serial.setTimeout(1);
}

// the main loop will require checking the serial regularly
void loop(){
    // main loop code

    // message check
    if(Serial.available() > 0){ // checks if serial has been used
        message = Serial.readString();
        Serial.print("Message received");
    }
}

int main(){
    return 0;
}

class Sensor{
    private:
        int pin; 
        string name;
    public:
    Sensor(){
        pin = 0;
        name = "NULL";
    }
    Sensor(int pin, string name){
        pin = pin;
        name = name;
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
};

class Solenoid: public Actuator{

    private:
        int state;
    public:
    Solenoid(int pin, string name, int state){
        pin = pin;
        name = name;
        state = state;
    }
    void toggleState(){
        // Code to toggle state
    }
};

class Buzzer: public Actuator{

    private:
        int tone;
        int buzzerCutOffTime;
        int buzzerActivatedTimestamp;
    public:
    Buzzer(int pin, string name, int tone){
        pin = pin;
        name = name;
        tone = tone;
    }
    void soundAlarm(){
        // Code to sound alarm
    }
};

class LED: public Actuator{

    private:
        int flashFreq;
    public:
    LED(int pin, string name, int flashFreq){
        pin = pin;
        name = name;
        flashFreq = flashFreq;
    }
    void flash(){
        // Code to flash LED
    }
};

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

    public:
    Session(char systemMode, int timeDelay,
        int timeTriggered,
        Sensor daySensors[12], Sensor nightSensors[12], 
        Actuator alarmActuactors[9], Actuator doorActuactors[9]){
            systemMode = systemMode;
            timeDelay = timeDelay;
            timeTriggered = timeTriggered;
            daySensors[12] = daySensors[12];
            nightSensors[12] = nightSensors[12];
            alarmActuactors[9] = alarmActuactors[9];
            doorActuactors[9] = doorActuactors[9];
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

class Interface{
    private:
        int accessLevel;
    public:
    Interface(){}
    void changeMode(char mode){
        // code to change system mode
    }

    void logout(){
        // code to log out of system
    }
};

class Level1: public Interface{
    public:
    Level1(){}
    void changeLevel(){
        // Code to change level
    }
};

class Level2: public Interface{
    private:
        string name;
    public:
    Level2(string name){
        name = name;
    }
    void addFace(float face[100][100]){ // Change this input to however the face is stored
        // Code to add face to database
    }
    void deleteFace(int userID){
        // Code to remove face from database
    }
    void deactivateSystem(){
        // Code to deactivate system
    }
    int changePin(int newPin){
        // Code to change pin
        return 0;
    }
};

class Login{
    private:
        string pinFile;
    bool checkPin(){
        // code to check pin
        return false;
    }
    void facialRecognition(){
        // Facial recognition code - link to python
    }
    public:
    Login(string pinFile){
        pinFile = pinFile;
    }
    int login(){
        // Code to login and return pin entered
        return 0;
    }
};