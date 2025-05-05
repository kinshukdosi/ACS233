#include "Actuator.h"

// Default Constructor //
Actuator::Actuator(){
  this->pin = 0;
  this->name[0] = '\0';
  
  pinMode(pin, OUTPUT);
  off();
}

// Constructor
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

// Turn Actuator Off //
Actuator::off(){
  digitalWrite(pin, LOW);
}

// Turn Actuator On //
Actuator::on(){
  digitalWrite(pin, HIGH);
}

// Write Actuator Name to given Address //
Actuator::getName(char* outputStr){
  for (int i=0; i<16; i++){
    outputStr[i] = name[i];
  }
}
