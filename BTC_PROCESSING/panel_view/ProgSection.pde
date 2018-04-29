class ProgSection extends Section { 
  // general (colors, fonts)
  int contentCol, txtCol;
  PFont txtFont;
  
  // logo display
  PImage btcLogo;
  float posImageX, posImageY;
  
  // progression
  float counter, targetCounter, targetCounterPrev;
  boolean reaching = false;
  boolean reachingBar = false;
  

  ProgSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
    super( _title, _borderW, _borderH, _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
    
    // setup general stuff
    contentCol = palette.get("content");
    txtCol = palette.get("text");
    txtFont = fonts.get("sanFranSemiBold");
    
    // load image, resize and compute position
    btcLogo = loadImage("images/bitcoinLogo3.png");
    int imgsz = (int) (0.70 * (contentH));
    btcLogo.resize(imgsz, imgsz);
    posImageX = startContentX + (contentW - btcLogo.width) / 2;
    posImageY = startContentY + (contentH - btcLogo.height) / 2;
    
    // init counter
    counter = 0;
  }

  void show() {
    super.show();

    // animate counter variable
    if (counter <= targetCounter) {
      counter += 0.007 * targetCounter;
    }
    if (reaching) {
      counter += 0.01;
      if (counter >= 1) {
        counter = 0;
        reaching = false;
        reachingBar = true;
      }
    }
    if (targetCounterPrev > targetCounter) {
      reaching = true;
    }

    // show progress
    fill(txtCol);
    textFont(txtFont);
    textSize(regTxtSz);
    String str = nf(counter * 100, 2, -1) + " %";
    float posX1 = posImageX + counter * btcLogo.width;
    float posX2 = posX1 - textWidth(str) / 2;
    float posY = startContentY + textAscent();
    textFont(txtFont);
    textSize(regTxtSz);
    text(str, posX2, posY);
    for (int i = 0; i < 2; i++) {
      ellipse(posX1, posY + 10 * (i + 1), 2, 2);
    }

    // display rectangle in negative space
    fill(contentCol);
    noStroke();
    rect(posImageX, posImageY, counter * (btcLogo.width - 2), btcLogo.height - 1);
    
    // display image
    image(btcLogo, posImageX, posImageY);

    // update stuff
    targetCounterPrev = targetCounter;
  } 

  void setCounter(float _counter) {
    targetCounter = _counter;
  }
}