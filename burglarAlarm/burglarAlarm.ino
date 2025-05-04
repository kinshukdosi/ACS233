// INCLUDE CLASSES //
#include "Session.h"

Session MainSession('D');

// SET UP //
void setup() {
  Serial.begin(9600);
}

// MAIN LOOP //
void loop() {
    MainSession.run();
}
