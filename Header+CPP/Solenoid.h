#include <string>
#include "Actuator.h"
using namespace std;

class Solenoid: public Actuator{
    private:
        int state;
    public:
    Solenoid(int pin, string name, int state);
    void toggleState();
};