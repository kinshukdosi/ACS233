
using namespace std;

const byte maxChars = 32;
char receivedMessage[maxChars];
boolean newMessage = false;
boolean access_granted = false;
char PASSCODE[4] = {'1', '2', '3', '4'};

// this is pseudo setup that needs to be in the setup to initialise connection to interface
void setup(){
    Serial.begin(9600);
}

// the main loop will require checking the serial regularly
void loop(){
    // main loop code

    // message check
   recvMessage();
   if(newMessage){
        if(!access_granted){checkPasscode();}
        else{Serial.println(String(receivedMessage));}
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
      access_granted = true;
      Serial.println("access_granted");
  }else{
      Serial.println(String(receivedMessage));
  }
}
