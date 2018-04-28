/*************************
Joel Bartlett
SparkFun Electronics
December 27, 2012

This code controls a stepper motor with the 
EasyDriver board. It spins forwards and backwards
***************************/
int dirpin = 23;
int steppin = 25;

int dirpin2 = 33;
int steppin2 = 31;

const byte numChars = 32;
char receivedChars[numChars];
String btcValueString;
double btcValueFloat;
boolean newData = false;
int counterData = 0;
int motorSpeeds[] = {1000, 1400, 1800, 2200, 2600, 3000};
int speedId = 0;

void setup() 
{
pinMode(dirpin, OUTPUT);
pinMode(steppin, OUTPUT);

pinMode(dirpin2, OUTPUT);
pinMode(steppin2, OUTPUT);

Serial.begin(9600);
}


void loop()
{ 
  recvWithStartEndMarkers();
  doStep();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
 // if (Serial.available() > 0) {
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void doStep() {
    if (newData == true) {
        counterData += 1;
        
        int numStep = atof(receivedChars);
        int motorSpeed = motorSpeeds[speedId];
        
        speedId += 1;
        
        if(speedId > 5) {
         speedId = 0;
        }
        
        /*
        int numStep;
        if(btcValueFloat < 1) {
         numStep = abs(btcValueFloat * 1000); 
        } else {
         numStep = abs(btcValueFloat); 
        }
        */
        Serial.println(numStep);
//        Serial.println(counterData);
        
        int i;
      
        digitalWrite(dirpin, LOW);     // Set the direction.
        digitalWrite(dirpin2, LOW);     // Set the direction.
      
        for (i = 0; i< numStep; i++)       // Iterate for 4000 microsteps.
        {
          digitalWrite(steppin, LOW);  // This LOW to HIGH change is what creates the
          digitalWrite(steppin, HIGH); // "Rising Edge" so the easydriver knows to when to step.
          
          digitalWrite(steppin2, LOW);  // This LOW to HIGH change is what creates the
          digitalWrite(steppin2, HIGH); // "Rising Edge" so the easydriver knows to when to step.
          
          delayMicroseconds(motorSpeed);      // This delay time is close to top speed for this
        }
        
        newData = false;
    }
}
