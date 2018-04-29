// OSC //
import oscP5.* ;                   
import netP5.*;
OscP5 oscP5;
int localhostadress = 8000;

// TRANSACTIONS //
ArrayList<Transaction> transactions = new ArrayList<Transaction>();
int maxStep = 150;
int transHeight = 15;
int transWidthMin = 15;
int transWidthMax = 50;

int padX = 20;
int padY = 20;
float posX = padX;
float posY = padY;

void setup() {
    // OSC parameters
  oscP5 = new OscP5(this, localhostadress) ;   // connect to OSC channel

  // window
  size(800, 100);
  //fullScreen();
}

void draw() {
  background(25);
  
  for(int i = 0; i < transactions.size(); i++) {
   transactions.get(i).show(); 
  }
}

// function that receives OSC messages
void oscEvent(OscMessage theOscMessage) {
  // debug
  //println(theOscMessage);

  // message when transactions happen
  if (theOscMessage.checkAddrPattern("/trans")==true)
  {
    //print(theOscMessage + "\n");
    // get value of transaction
    float numStep = theOscMessage.get(1).intValue();
    float transWidth = map(numStep, 1, maxStep, transWidthMin, transWidthMax);
    
    
    if(posX + transWidth > width - padX) {
     posX = padX;
     posY += transHeight + padY;
     if(posY > height -padY) {
      posY = padY;
      for (int i = transactions.size() - 1; i >= 0; i--) {
          transactions.remove(i);
      }
     }
    }
        
    Transaction newTrans = new Transaction(theOscMessage.get(0).stringValue(), transWidth, transHeight, posX, posY);
    
    posX += transWidth + padX;
    
    //print(num  Step + "\t" + transWidth + "\n");
    print(posX + "\n");
    
    transactions.add(newTrans);
  }
}