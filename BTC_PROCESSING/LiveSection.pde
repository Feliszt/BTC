class LiveSection extends Section {  
  String transTime, transValueBTC, transValueEUR;
  ArrayList<Transaction> trans = new ArrayList<Transaction>();
  
  PFont monoSpaceBold, monoSpace;
  int contentCol, timeCol, bgCol;
  
  LiveSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
      super( _title,_borderW, _borderH,  _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
      
      monoSpaceBold = fonts.get("monoSpaceBold");
      monoSpace = fonts.get("monoSpace");
      contentCol = palette.get("content");
      timeCol = palette.get("header");
      bgCol = palette.get("background");
  }
  
  void show() {
     super.show();
     
     // display legend
     float posY = borderH + startContentY - 17;
     float posX = sectionX + borderW;
     textFont(titleFont);
     textSize(10);
     text("Heure", posX, posY);
     posX += 500;      
     text("Valeur (BTC)", posX, posY);
     posX += 380;      
     text("Valeur (EUR)", posX, posY);
     
     // display transaction
    
    textFont(monoSpaceBold);
    posY += textAscent() + 20;
    for(int i = trans.size() - 1; i >= 0 ; i--) {
     trans.get(i).show(sectionX + borderW, posY, contentCol, timeCol, bgCol, monoSpaceBold, monoSpace);
     posY += textAscent() + 20;
    }
   
  }
  
  void addTrans(Transaction newTrans) {
    trans.add(newTrans);
    if(trans.size() > 13){
      trans.remove(0); 
    }
  }  
}

class Transaction {
   String time;
   String valueBTC;
   String valueEUR;
   
   Transaction(String _time, String _valueBTC, String _valueEUR) {
    time = _time;
    valueBTC = _valueBTC;
    valueEUR = _valueEUR;
   }
   
   void show(float posX, float posY, int contentCol, int timeCol, int bgCol, PFont valueFont, PFont timeFont) {
      // init stuff
      float x = posX;      
      
      // draw time
      textFont(timeFont);
      fill(timeCol);
      text(time, x, posY);
      x += 430;
      
      // draw BTC value of transaction
      textFont(valueFont);
      //fill(contentCol);
      text(valueBTC, x, posY);
      x += 410;
      
      // draw EUR value of transaction
      fill(contentCol);
      text(valueEUR, x, posY);
      
      // draw line
      stroke(bgCol);
      line(posX, posY - textAscent() - 5, posX + x + 80, posY - textAscent() - 5);
      noStroke();
   }  
}