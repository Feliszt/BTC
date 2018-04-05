class Section {
 float borderW, borderH, sectionX, sectionY, sectionW, sectionH;
 float startContentX, startContentY, contentW, contentH;
 String title; 
 int mainTitleSz = 14;
 HashMap<String, Integer> colors;
 int bgCol, txtCol;
 HashMap<String, PFont> fonts;
 PFont titleFont;
 
  
  Section(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
    title = _title;
    
    borderW = _borderW;
    borderH = _borderH;
    sectionX = _sectionX;
    sectionY = _sectionY;
    sectionW = _sectionW;
    sectionH = _sectionH;
    
    palette = _palette;
    bgCol = palette.get("box");
    txtCol = palette.get("text");

    fonts = _fonts;
    titleFont = fonts.get("sanFranSemiBold");    
    textFont(titleFont);
    textSize(mainTitleSz);
    
    startContentX = sectionX + borderW;
    startContentY = sectionY + borderH + textAscent() + borderH;
    contentW = sectionW - 2 * borderW;
    contentH = sectionH - (startContentY - sectionY) - borderH;
  }
  
  void show() {
     fill(bgCol);
     noStroke();
     rect(sectionX, sectionY, sectionW, sectionH);
     
     fill(txtCol);
     textFont(titleFont);
     textSize(mainTitleSz);
     text(title, sectionX + borderW, sectionY + borderH + textAscent());
     
     // debug
     noFill();
     stroke(txtCol);
     strokeWeight(1);
     //rect(startContentX, startContentY, contentW, contentH);
     noStroke();
  }
}