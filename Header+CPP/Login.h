#include <string>
using namespace std;

class Login{
    private:
        string pinFile;
    bool checkPin();
    void facialRecognition();
    public:
    Login(string pinFile);
    int login();

};