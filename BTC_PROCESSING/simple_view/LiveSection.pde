class LiveSection extends Section {  
  String transTime, transValueBTC, transValueEUR;
  ArrayList<Transaction> trans = new ArrayList<Transaction>();
  
  PFont monoSpaceBold, monoSpace;
  int contentCol, timeCol, bgCol;
  
  String firstColumn = "Heure";
  String secondColumn = "Valeur (BTC)";
  float secondColumnW;
  String thirdColumn = "Valeur (EUR)";
  float thirdColumnW;
  
  LiveSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
      super( _title,_borderW, _borderH,  _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
      
      monoSpaceBold = fonts.get("monoSpaceBold");
      monoSpace = fonts.get("monoSpace");
      //contentCol = palette.get("content");
      contentCol = palette.get("text");
      timeCol = palette.get("text");
      bgCol = palette.get("background");
      
      // set column widths
      textFont(titleFont);
      textSize(regTxtSz);
      secondColumnW = textWidth(secondColumn) / 2;
      thirdColumnW = textWidth(thirdColumn);
      
  }
  
  void show() {
     super.show();
     
     // display legend
     textFont(titleFont);
     textSize(regTxtSz);
     float posY = startContentY + textAscent();
     float posX = startContentX;
     text(firstColumn, posX, posY);
     posX = startContentX + contentW / 2 - secondColumnW;      
     text(secondColumn, posX, posY);
     
    stroke(contentCol);
    line(startContentX, posY + 0.5 * textAscent(), contentW, posY  + 0.5 * textAscent());
    noStroke();
     /*
     posX = startContentX + contentW  - thirdColumnW;      
     text(thirdColumn, posX, posY);
     */
     
     // display transaction    
    posY += 1.5 * textAscent();
    for(int i = trans.size() - 1; i >= 0 ; i--) {
     if(posY < startContentY + contentH) {  
       trans.get(i).show(startContentX, posY, startContentX + contentW / 2 + secondColumnW, posX + thirdColumnW, contentCol, timeCol, bgCol, monoSpace, monoSpace);
       posY += 1.5 * textAscent();
     }     
    }
   
  }
  
  void addTrans(Transaction newTrans) {
    trans.add(newTrans);
    if(trans.size() > 100){
      trans.remove(0); 
    }
  }  
}

class Transaction {
   String time;
   String valueBTC;
   String valueEUR;
   int numberSz;
   
   Transaction(String _time, String _valueBTC) {
    time = _time;
    valueBTC = _valueBTC;
    
    numberSz = (int) map(height, 0, 1080, 8, 32);
   }
   
   void show(float posX, float posY, float posX2, float posX3, int contentCol, int timeCol, int bgCol, PFont valueFont, PFont timeFont) {     
      // draw time
      textFont(timeFont);
      textSize(numberSz);  
      fill(timeCol);
      text(time, posX, posY);
      
      // draw BTC value of transaction
      textFont(valueFont);
      textSize(numberSz);
      text(valueBTC, posX2 - textWidth(valueBTC), posY); 
      
      /*
      // draw EUR value of transaction
      fill(contentCol);
      text(valueEUR, posX3 - textWidth(valueEUR), posY);
      */
      
      // draw line
      /*
      stroke(bgCol);
      line(posX, posY - textAscent() - 5, posX3, posY - textAscent() - 5);
      noStroke();
      */
   }  
}