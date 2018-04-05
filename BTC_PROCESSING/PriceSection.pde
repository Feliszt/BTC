class PriceSection extends Section { 
  String BTCPriceEUR = "";
  String BTCLastPriceEUR = "";
  String BTCVariation = "";
  PFont priceFont;
  
  PriceSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
      super( _title,_borderW, _borderH,  _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
      
      priceFont = fonts.get("sanFranSemiBold");
  }
  
  void show() {
     super.show();
   
     textFont(titleFont);
     textSize(55);
     fill(txtCol);
     text(BTCPriceEUR + " €", startContentX, startContentY + textAscent());
     
     textSize(18);
     text("Hier ", 750, startContentY + textAscent());
     String str = BTCLastPriceEUR + " €";
     float strW = textWidth(str);
     text(str, startContentX + contentW - strW, startContentY + textAscent());
     text("Variation ", 750, startContentY + contentH - 20);
     str = BTCVariation + " %";
     strW = textWidth(str);
     text(str, sectionX + sectionW - strW - borderW, startContentY + contentH - 20);
  } 
  
  void setPrice(String newPrice, String lastPrice, String newVariation) {
   BTCPriceEUR = newPrice;
   BTCLastPriceEUR = lastPrice;
   BTCVariation = newVariation;
  }
}