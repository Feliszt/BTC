// DATA
const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;
int counterData = 0;
int commandStep = 0;
int commandSpeed = 0;

// LED DEBUG
int ledpin = 2;

void setup() {
  // init led
  digitalWrite(ledpin, OUTPUT);
  
 Serial.begin(115200);
 Serial.println("Serial port is ready.");
}

void loop() {
  // switch on led
  digitalWrite(ledpin, HIGH);  
  
 recvWithEndMarker();
 showNewData();
}

void recvWithEndMarker() {
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

void showNewData() {
 if (newData == true) {
   counterData += 1;
   commandStep = atoi(strtok(receivedChars, "-"));
   commandSpeed = atoi(strtok(NULL, "-"));
        
   Serial.println(String(counterData) + " " + String(commandStep) + " " + String(commandSpeed));
   newData = false;
 }
}
