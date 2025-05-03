// INCLUDE CLASSES //
#include "Session.h"

Session MainSession('N');

// SET UP //
void setup() {
  Serial.begin(9600);
}

// MAIN LOOP //
void loop() {
    MainSession.run();
}
