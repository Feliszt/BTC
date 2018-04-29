// ConstantSpeed.pde
// -*- mode: C++ -*-
//
// Shows how to run AccelStepper in the simplest,
// fixed speed mode with no accelerations
/// \author  Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2009 Mike McCauley
// $Id: ConstantSpeed.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $
#include <AccelStepper.h>


AccelStepper stepper(2, 33, 31); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
int motorSpeed = 12000;

void setup()
{  
   stepper.setMaxSpeed(10000);
   stepper.setSpeed(10000);
   stepper.setAcceleration(20000);
   stepper.setCurrentPosition(0);
   stepper.move(6400);
   
   Serial.begin(9600);     
}

void loop()
{      
   stepper.runSpeed();
}
