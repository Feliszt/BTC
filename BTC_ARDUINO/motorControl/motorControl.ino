/*************************
Felix Cote
  Script that drives the stepper motor
  for Collectif TOAST's BTC installation
***************************/

int dirpin = 23;
int steppin = 25;

int dirpin2 = 33;
int steppin2 = 31;

int ledpin = 2;

const byte numChars = 32;
char receivedChars[numChars];
String btcValueString;
double btcValueFloat;
boolean newData = false;
int counterData = 0;

unsigned long currentMicros = 0;  
unsigned long previousMotorMicros = 0;
int numStep = 0;
int motorSpeed = 1000;

int steps = 0;

void setup() 
{
pinMode(dirpin, OUTPUT);
pinMode(steppin, OUTPUT);

pinMode(dirpin2, OUTPUT);
pinMode(steppin2, OUTPUT);

pinMode(ledpin, OUTPUT);

Serial.begin(9600);
Serial.println("Serial port ready");
}


void loop()
{ 
  digitalWrite(ledpin, HIGH);
 
  receiveData();
  processData();
  
  currentMicros = micros();
  motorSpeed = 1000;
  if(currentMicros - previousMotorMicros >= motorSpeed) {
    if(steps > 0) {
      doStep(steppin2, dirpin2);
      doStep(steppin, dirpin);
      steps -= 1;      
    } 
    previousMotorMicros += motorSpeed;
  }
}

void receiveData() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char seperateMarker = '-';
    char rc;
 
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

        else if (rc == startMarker ) {
            recvInProgress = true;
        }

    }
}

void processData() {
    if (newData == true) {      
        numStep = atoi(strtok(receivedChars, "-"));           
        motorSpeed = atoi(strtok(NULL, "-"));
        
        steps += numStep;
        
        /*
        int diffStep = numStep - steps;
        
        if(diffStep > 0) {
          steps += diffStep;          
        } 
        */
        
         /*
        int i;
        for(i = 0; i < numStep; i++) {
          doStep(steppin2, dirpin2);
          doStep(steppin, dirpin);
          delayMicroseconds(motorSpeed);
        }
        */
        
        counterData += 1;
        newData = false;
        
        Serial.println("data #" + String(counterData) + " " + String(steps) + " steps " + String(motorSpeed) + " speed.");
    }
}

void doStep(int STEP_PIN, int DIR_PIN) {
    digitalWrite(DIR_PIN, LOW);
    digitalWrite(STEP_PIN, LOW);
    digitalWrite(STEP_PIN, HIGH);
}
