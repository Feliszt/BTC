class GraphSection extends Section { 
  // data
  JSONObject BTCvaluesJSON;
  int szJSON;
  
  // graph
  PFont textFont;
  float minX, maxX, minY, maxY;
  int titleSz = 12;
  int labelSz = 10;
  float graphH, graphMinX, graphMinY;
  
  // curve
  int nbPoints = 100;
  float[] BTCvalues;
  float firstInd, newFirstInd;
  float[] valueX = new float[nbPoints];
  float[] valueY = new float[nbPoints];
  
  // colors
  int contentCol;
  int bgCol;
  int txtCol;
  
  // label and states
  int displayState = 0;
  String[] abs = {"0 €", "5 000 €", "10 000 €", "15 000 €"};
  String[] displayStates = {"DEPUIS LE DEBUT", "1 AN", "6 MOIS", "1 MOIS"};
  
  // animation
  int secondToChange = 30;
  int secondPrev;
  int nextChangeMillis;
  float progressBarW;

  GraphSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
      super( _title,_borderW, _borderH,  _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
      
      contentCol = palette.get("content");
      bgCol = palette.get("background");
      txtCol = palette.get("text");
      
      textFont = fonts.get("sanFranSemiBold");
      
      minX = startContentX;
      minY = startContentY;
      maxX = startContentX + contentW;
      maxY = startContentY+ contentH;
      
      float padY = map(maxY - minY, 100, 500, 10, 15);
      textSize(titleSz);
      graphH = maxY - padY - textAscent() - padY;
      textSize(labelSz);
      float maxStringSz = 0;
      for(int i = 0; i < abs.length; i++) {
        if(textWidth(abs[i]) > maxStringSz) maxStringSz = textWidth(abs[i]);
      }
      graphMinX = minX + maxStringSz;
      graphMinY = minY + textAscent() / 2;
      
      //
      loadData();
  }
  
  void show() {
     super.show();    
     
     //
    firstInd *= 0.5;
    firstInd += (1 - 0.5) * newFirstInd;
    
    // draw lines
    textFont(textFont);
    textSize(labelSz);
    fill(txtCol);
    noStroke();
    for(int i = 0; i < abs.length; i++) {
      float y = map(i, 0, abs.length - 1, graphH, graphMinY);
      text(abs[i], graphMinX - textWidth(abs[i]), y + textAscent() / 2); 
      rect(graphMinX + 10, y, 8, 3);
      for(float j = graphMinX + 30; j < maxX; j+=15) {
        ellipse(j, y + 1.5, 2, 2);
      }
    }
    
    // draw
    noFill();
    stroke(contentCol);
    strokeWeight(6);
    beginShape();
    int indInArrayPrev = 0;
    for(int i = 0; i < nbPoints; i++) {
     int indInArray = (int) map(i, 0, nbPoints - 1, firstInd, szJSON - 1);
     if(indInArray != indInArrayPrev) {
       float x = map(indInArray, firstInd, szJSON - 1, graphMinX + 18, maxX);
       float y = map(BTCvalues[indInArray] * 0.81, 0, 15000, graphH, graphMinY);
       valueX[i] *= 0.7;
       valueX[i] += (1 - 0.7) * x;
       valueY[i] *= 0.7;
       valueY[i] += (1 - 0.7) * y;
       curveVertex(valueX[i],  valueY[i]);
     }
     indInArrayPrev = indInArray;
    }
    endShape();
    
    // draw title
    textFont(textFont);
    textSize(titleSz);
    fill(txtCol);
    stroke(txtCol);
    strokeWeight(1);
    String label = displayStates[displayState];
    float labelW = textWidth(label);
    float x = (minX+maxX - labelW)*0.5;
    float y = maxY - 6;
    text(label, x, y);
    progressBarW = map(second() % secondToChange, 0, secondToChange-1, 0, labelW);
    rect(x, y + 3, progressBarW, 3);
    
    if(second() % secondToChange == 0 && secondPrev % secondToChange != 0)  {
      changeState(false);
    }
      
    secondPrev = second();   
  } 
  
  void loadData() {
    // load btc prices
   BTCvaluesJSON = loadJSONObject("/home/felix/Code/ProcessingProjects/Projects/BTC_VISU/data/JSONs/historicalData.json");
   szJSON = BTCvaluesJSON.size();
   BTCvalues = new float[szJSON];
   for(int i = 0; i < szJSON; i++) {
    BTCvalues[i] = BTCvaluesJSON.getFloat(str(i)); 
   }
  }
  
  void changeState(boolean direction) {
    if(direction) {
     displayState++;
     if(displayState > 3) displayState = 0;
     setState();
    } else {
     displayState--;
     if(displayState < 0) displayState = 3;
     setState();
    }
  }
  
  void setState() {
    if(displayState == 0) newFirstInd = 0;
    if(displayState == 1) newFirstInd = szJSON - 365;
    if(displayState == 2) newFirstInd = szJSON - 183;
    if(displayState == 3) newFirstInd = szJSON - 30;
  }
}