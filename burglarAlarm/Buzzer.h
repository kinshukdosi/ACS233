#include <Arduino.h>
#include "Actuator.h"
using namespace std;

// Define Buzzer Class as a Child of Actuator //
class Buzzer: public Actuator{
    private:
        // Private Atributes //
        int pitch;
    public:
        // Constructors //
        Buzzer();
        Buzzer(int pin, char name[], int pitch);

        // Redefine on() and off() methods to use tone() function
        on();
        off();
};