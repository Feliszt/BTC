/*************************
Felix Cote
  Script that drives the stepper motor
  for Collectif TOAST's BTC installation
***************************/

// MOTOR 1
int dirpin1 = 23;
int steppin1 = 25;
unsigned long previousMotorMicros1 = 0;
int motorSpeed1 = 8000;
int steps1 = 0;

boolean vibrate = false;
unsigned long previousVibrationMotor = 0;
int vibrationMotor = 2000;

// MTOTOR2
int dirpin2 = 33;
int steppin2 = 31;
unsigned long previousMotorMicros2 = 0;
int motorSpeed2 = 4000;
int steps2 = 0;

// TIME
unsigned long currentMicros = 0;
unsigned long currentMillis = 0;

// DEBUG LED
int ledpin = 2;

// DATA
const byte numChars = 32;
char receivedChars[numChars];
String btcValueString;
double btcValueFloat;
boolean newData = false;
int counterData = 0;

void setup()
{
pinMode(dirpin1, OUTPUT);
pinMode(steppin1, OUTPUT);

pinMode(dirpin2, OUTPUT);
pinMode(steppin2, OUTPUT);

pinMode(ledpin, OUTPUT);

Serial.begin(9600);
Serial.println("Serial port ready");
}


void loop()
{
  // switch on debug led
  digitalWrite(ledpin, HIGH);

  /*
  receiveData();
  processData();
  */

  // get current time
  currentMicros = micros();
  currentMillis = millis();
  
    
  // step loop for motor 1
  if(currentMillis - previousVibrationMotor >= vibrationMotor) {
    vibrate = !vibrate;
    previousVibrationMotor += vibrationMotor;
        Serial.println(previousVibrationMotor);
  }
  
  // step loop for motor 1
  if(currentMicros - previousMotorMicros1 >= motorSpeed1) {
    if(vibrate) {
      doStep(steppin1, dirpin1, true);
    }

    previousMotorMicros1 += motorSpeed1;
  }
  
  // step loop for motor 1
  if(currentMicros - previousMotorMicros2 >= motorSpeed2) {
    doStep(steppin2, dirpin2, false);
    steps2 -= 1;
    previousMotorMicros2 += motorSpeed2;
  } 
}

/*
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

        diffStep = numStep - steps;
        if(diffStep > 0) {
          steps += diffStep;
        }

        counterData += 1;
        newData = false;

        Serial.println("data #" + String(counterData) + " " + String(steps) + " steps " + String(motorSpeed) + " speed.");
    }
}
*/

void doStep(int STEP_PIN, int DIR_PIN, boolean DIR) {
    DIR ? LOW : HIGH;
    digitalWrite(DIR_PIN, DIR);
    digitalWrite(STEP_PIN, LOW);
    digitalWrite(STEP_PIN, HIGH);
}
