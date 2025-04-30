#include <string>
#include "Actuator.h"
using namespace std;

class Buzzer: public Actuator{
    private:
        int tone;
        int buzzerCutOffTime;
        int buzzerActivatedTimestamp;
    public:
    Buzzer(int pin, string name, int tone);
    void soundAlarm();
};