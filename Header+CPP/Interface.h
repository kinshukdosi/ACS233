#include <string>
using namespace std;
#ifndef INTERFACE_H
#define INTERFACE_H
class Interface{
    protected:
        int accessLevel;
    public:
    Interface();
    void changeMode(char mode);
    void logout();
};

#endif