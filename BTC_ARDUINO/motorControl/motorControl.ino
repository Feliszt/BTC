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
int vibrationMotor = 10000;

// MOTOR2
int dirpin2 = 33;
int steppin2 = 31;
unsigned long previousMotorMicros2 = 0;
int motorSpeed2 = 4000;
int steps2 = 0;
int numStep = 0;
int diffStep = 0;

// UPDATE OF MOTOR2's SPEED
float acceleration = 0.95;
unsigned long previousSpeedUpdate = 0;
int speedUpdate = 16;


// TIME
unsigned long currentMicros = 0;
unsigned long currentMillis = 0;

// DEBUG LED
int ledpin = 2;

// DATA
const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;
int counterData = 0;
int commandStep1 = 0;
int commandStep2 = 0;
int commandSpeed = 0;

void setup()
{
  pinMode(dirpin1, OUTPUT);
  pinMode(steppin1, OUTPUT);
  
  pinMode(dirpin2, OUTPUT);
  pinMode(steppin2, OUTPUT);
  
  pinMode(ledpin, OUTPUT);
  
  Serial.begin(115200);
  Serial.println("Serial port ready");
}


void loop()
{  
   // switch on debug led
  digitalWrite(ledpin, HIGH);

  // get and process data
  receiveData();
  processData();
  

  // get current time
  currentMicros = micros();
  currentMillis = millis();
  
  // step loop for motor 1
  if(currentMicros - previousMotorMicros1 >= motorSpeed1) {
    if(steps1 > 0) {
      doStep(steppin1, dirpin1, false);
      steps1 -= 1;
    }
    previousMotorMicros1 += motorSpeed1;
  }
  
  // step loop for motor 1
  if(currentMicros - previousMotorMicros2 >= motorSpeed2) {
    if(steps2 > 0) {
      doStep(steppin2, dirpin2, true);
      steps2 -= 1;
      //delayMicroseconds(motorSpeed2);
    }
    previousMotorMicros2 += motorSpeed2;
  } 
}

void receiveData() {
 static byte ndx = 0;
 char endMarker = '>';
 char rc;
 
 while (Serial.available() > 0 && newData == false) {
   rc = Serial.read();
  
   if (rc != endMarker) {
     receivedChars[ndx] = rc;
     ndx++;
     if (ndx >= numChars) {
       ndx = numChars - 1;
     }
   }
   else {
     receivedChars[ndx] = '\0'; // terminate the string
     ndx = 0;
     newData = true;
   }
 }
}

void processData() {
    if (newData == true) {
      
      Serial.println(receivedChars);
      
        // process data
        counterData += 1;
        commandStep2 = atoi(strtok(receivedChars, "-"));
        commandSpeed = atoi(strtok(NULL, "-"));
        commandStep1 = atoi(strtok(NULL, "-"));
        motorSpeed2 = commandSpeed;
        
        //
        steps1 += commandStep1;
        
        // increment steps for coin releasing motor
        diffStep = commandStep2 - steps2;
        if(diffStep > 0) {
          steps2 += diffStep;
        }
        
        // display
        //Serial.println(String(counterData) + "\t" + String(commandStep2) + "\t" + String(commandSpeed));
        newData = false;        
    }
}

void doStep(int STEP_PIN, int DIR_PIN, boolean DIR) {
    digitalWrite(DIR_PIN, (DIR ? LOW : HIGH));
    digitalWrite(STEP_PIN, LOW);
    digitalWrite(STEP_PIN, HIGH);
}
