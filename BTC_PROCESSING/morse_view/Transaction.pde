class Transaction {
   String time;
   float valueBTC;
   float transHeight;
   float posX, posY;
   
   Transaction(String _time, float _valueBTC, float _transHeight, float _posX, float _posY) {
    time = _time;
    valueBTC = _valueBTC;
    
    transHeight = _transHeight;
    posX = _posX;
    posY = _posY;
   }
   
   void show() {       
       fill(255);
       noStroke();
      rect(posX, posY, valueBTC, transHeight, 100);
   }  
}