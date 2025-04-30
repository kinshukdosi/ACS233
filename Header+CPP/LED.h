#include <string>
#include "Actuator.h"
using namespace std;

class LED: public Actuator{
    private:
        int flashFreq;
    public:
    LED(int pin, string name, int flashFreq);
    void flash();
};