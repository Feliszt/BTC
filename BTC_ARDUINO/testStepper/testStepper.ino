/* 
 Stepper Motor Control - speed control
 
 This program drives a unipolar or bipolar stepper motor. 
 The motor is attached to digital pins 8 - 11 of the Arduino.
 A potentiometer is connected to analog input 0.
 
 The motor will rotate in a clockwise direction. The higher the potentiometer value,
 the faster the motor speed. Because setSpeed() sets the delay between steps, 
 you may notice the motor is less responsive to changes in the sensor value at
 low speeds.
 
 Created 30 Nov. 2009
 Modified 28 Oct 2010
 by Tom Igoe
 
 */

#include <Stepper.h>

const int stepsPerRevolution = 200 * 64;  // change this to fit the number of steps per revolution
// for your motor


// initialize the stepper library on pins 8 through 11:
Stepper stepperDir1(stepsPerRevolution, 33, 31);
Stepper stepperDir2(stepsPerRevolution, 31, 33);
Stepper stepperDir3(stepsPerRevolution, 33, 31);

int motorSpeed = 5;

// SERIAL TRANSMISSION
char receivedChar;
boolean newData = false;

int countStep = 0;

int stepPerCoin = 1400;

void setup() {
  // nothing to do inside the setup
  //stepperDir1.setSpeed(motorSpeed);
  //stepperDir2.setSpeed(motorSpeed);
  

  
      //Serial
  Serial.begin(9600);
}

void loop() {
   //recvOneChar();
   //setMotorSpeed();
   
   stepperDir3.setSpeed(motorSpeed);
     
   //stepperDir1.step(stepsPerRevolution);
   stepperDir3.step(stepsPerRevolution);
   
   delay(1000);
}

void recvOneChar() {
    if (Serial.available() > 0) {
        receivedChar = Serial.read();
        newData = true;
    }
}

void setMotorSpeed() {
    if (newData == true) {
      //Serial.println(receivedChar);
        
        if(receivedChar == '<') {
//         motorSpeed -= 5;
         stepperDir1.step(50);
        }        
        if(receivedChar == '>') {
         //motorSpeed += 5; 
         stepperDir2.step(50);
         countStep += 50;
        }
        
        if(receivedChar == 'r') {
         stepperDir2.step(stepPerCoin);
        }
//        motorSpeed = constrain(motorSpeed, motorSpeedMIN, motorSpeedMAX);     
        
        newData = false;
    }
}


