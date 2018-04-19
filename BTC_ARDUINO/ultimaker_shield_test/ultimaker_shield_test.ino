int xstepperPin =25;
int xdirPin =23;
int xenable =27 ;

int ystepperPin =31;
int ydirPin =33;
int yenable =29;

int zstepperPin =37;
int zdirPin =39;
int zenable =35 ;

int estepperPin =43;
int edirPin =45;
int eenable =41 ;

int astepperPin =49;
int adirPin =47;
int aenable =48;


int heater1=2;
int heater2=3;
int heater3=4;
int heater4=7;

// MOTOR SPEED
int motorSpeed = 400;
int motorSpeedMIN = 5;
int motorSpeedMAX = 800;

// SERIAL TRANSMISSION
char receivedChar;
boolean newData = false;

void setup() 
{
 pinMode(xdirPin, OUTPUT);
 pinMode(xstepperPin, OUTPUT);
  pinMode(xenable, OUTPUT);
  digitalWrite(xenable, LOW);
  
  pinMode(ydirPin, OUTPUT);
 pinMode(ystepperPin, OUTPUT);
  pinMode(yenable, OUTPUT);
  digitalWrite(yenable, LOW);
  
  pinMode(zdirPin, OUTPUT);
 pinMode(zstepperPin, OUTPUT);
  pinMode(zenable, OUTPUT);
  digitalWrite(zenable, LOW);
  
  pinMode(edirPin, OUTPUT);
 pinMode(estepperPin, OUTPUT);
  pinMode(eenable, OUTPUT);
  digitalWrite(eenable, LOW);
  
  pinMode(adirPin, OUTPUT);
 pinMode(astepperPin, OUTPUT);
  pinMode(aenable, OUTPUT);
  digitalWrite(aenable, LOW);
  
  
  pinMode(heater1, OUTPUT);
 pinMode(heater2, OUTPUT);
  pinMode(heater3, OUTPUT);
  digitalWrite(heater4, OUTPUT);
  
    //Serial
  Serial.begin(9600);
}

void step(boolean dir,int steps, int delaySpeed)
 {
 digitalWrite(xdirPin,dir);
 digitalWrite(ydirPin,dir);
 digitalWrite(zdirPin,dir);
 digitalWrite(edirPin,dir);
 digitalWrite(adirPin,dir);
 
  digitalWrite(heater1,dir);
 digitalWrite(heater2,dir);
 digitalWrite(heater3,dir);
 digitalWrite(heater4,dir);

 //delay(50);
 for(int i=0;i<steps;i++){
   digitalWrite(xstepperPin, HIGH);
   digitalWrite(ystepperPin, HIGH);
   digitalWrite(zstepperPin, HIGH);
   digitalWrite(estepperPin, HIGH);
   digitalWrite(astepperPin, HIGH);
  delayMicroseconds(delaySpeed);
  digitalWrite(xstepperPin, LOW);
  digitalWrite(ystepperPin, LOW);
  digitalWrite(zstepperPin, LOW);
  digitalWrite(estepperPin, LOW); 
  digitalWrite(astepperPin, LOW);
  delayMicroseconds(delaySpeed);
 }
}

void loop() {
   recvOneChar();
   setMotorSpeed();
   
   Serial.println(motorSpeed);     // new for this version
 
   step(true, 10, motorSpeed);
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
         motorSpeed -= 5; 
        }        
        if(receivedChar == '>') {
         motorSpeed += 5; 
        }
        motorSpeed = constrain(motorSpeed, motorSpeedMIN, motorSpeedMAX);     
        
        newData = false;
    }
}
