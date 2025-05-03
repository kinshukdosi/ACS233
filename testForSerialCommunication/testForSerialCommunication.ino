
using namespace std;

const byte maxChars = 32;
char receivedMessage[maxChars];
boolean newMessage = false;
boolean accessGranted = false;
unsigned long accessTime;
unsigned short accessAttempts = 0;
char PASSCODE[4] = {'1', '2', '3', '4'};

unsigned long currentTime = millis();

// this is pseudo setup that needs to be in the setup to initialise connection to interface
void setup(){
    Serial.begin(9600);
}

// the main loop will require checking the serial regularly
void loop(){
    if(accessGranted && (accessTime + 10000) < millis()){
      accessGranted = false;
      Serial.println("timeOut");
    }
      // message check
    recvMessage();
    if(newMessage){
      if(!accessGranted){checkPasscode();}
      else{
        if(strcmp(receivedMessage, "switchDN")){
            //code for switching between day and night
            Serial.println("DNSwitched");
        }else if(strcmp(receivedMessage, "deactSys")){
            // code for deactivating system
            Serial.println("System Deactivating");
        }else if(strcmp(receivedMessage, "changePin")){
            // code for changing pin
        }else{
          Serial.println("Unrecognised message");
        }
      }
      newMessage = false;
    }
  }


void recvMessage(){
    static boolean receiving = false;
    static byte index = 0;
    char startMarker = '<';
    char endMarker = '>';
    char receivedChar;
    while(Serial.available() > 0 && newMessage == false){
        receivedChar = Serial.read();

        if(receiving == true){
            if(receivedChar != endMarker){
                receivedMessage[index] = receivedChar;
                index++;
                if(index >= maxChars){
                    index = maxChars - 1;
                }
            }
            else{
                receivedMessage[index] = '\0';
                receiving = false;
                index = 0;
                newMessage = true;
            }
        }
        else if (receivedChar == startMarker){
            receiving = true;
        }
    }
}


bool checkPasscode(){
  char currentChar = ' ';
  int i = 0;
  int correctNums = 0;
  while(currentChar != '\0'){
      currentChar = receivedMessage[i];
      if(i < 4){
          if(currentChar == PASSCODE[i]){
              correctNums++;
          }
      }
      i++;
  }
  if(correctNums == 4 && i < 6){
      accessTime = millis();
      accessGranted = true;
      Serial.println("access_granted");
  }else{
      Serial.println("access_denied");
      accessAttempts++;
      if(accessAttempts >= 3){
        Serial.println("SYSTEM_LOCK");
      }
  }
}
