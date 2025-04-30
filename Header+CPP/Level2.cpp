#include "Level2.h"
#include <string>

Level2::Level2(string name){
    this->accessLevel = 1;
    this->name = name;
}

void Level2::addFace(float face[100][100]){ // Change this input to however the face is stored
    // Code to add face to database
}
void Level2::deleteFace(int userID){
    // Code to remove face from database
}
void Level2::deactivateSystem(){
    // Code to deactivate system
}
int Level2::changePin(int newPin){
    // Code to change pin
    return 0;
}