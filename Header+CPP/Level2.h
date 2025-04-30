#include <string>
#include "Interface.h"
using namespace std;

class Level2: public Interface{
    private:
        string name;
    public:
    Level2(string name);
    void addFace(float face[100][100]);
    void deleteFace(int userID);
    void deactivateSystem();
    int changePin(int newPin);
    
};