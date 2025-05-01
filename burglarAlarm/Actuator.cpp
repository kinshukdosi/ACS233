#include "Actuator.h"

Actuator::Actuator(){
    pin = 0;
    name[0] = '\0';
    pinMode(pin, OUTPUT);
    off();
}

Actuator::Actuator(int pin, char name[]){
    this->pin = pin;
    
    // Write a string, ensuring it doesn't execeed 15 chars + '\0'
    int i = 0;
    do{
        this->name[i] = name[i];
        i++;
    } while (i<15 && name[i-1]!='\0');
    this->name[i] = '\0';
    
    pinMode(pin, OUTPUT);
    off();
}

Actuator::off(){
  digitalWrite(pin, LOW);
}

Actuator::on(){
  digitalWrite(pin, HIGH);
}

Actuator::getName(char* outputStr){
  for (int i=0; i<16; i++){
      outputStr[i] = name[i];
  }
}
