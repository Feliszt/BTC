class PriceSection extends Section { 
  String BTCPriceEUR = "";
  String BTCLastPriceEUR = "";
  String BTCVariation = "";
  PFont priceFont;
  int btcSz, statSz;
  String stat1 = "Hier";
  String stat2 = "Variation";
  
  PriceSection(String _title, float _borderW, float _borderH, float _sectionX, float _sectionY, float _sectionW, float _sectionH, HashMap _palette, HashMap _fonts) {
      super( _title,_borderW, _borderH,  _sectionX, _sectionY, _sectionW, _sectionH, _palette, _fonts);
      
      priceFont = fonts.get("sanFranSemiBold");
      
      btcSz = (int) (contentH * 0.58);
      statSz = (int) (contentH * 0.15);
  }
  
  void show() {
     super.show();
   
     // display price
     textFont(titleFont);
     textSize(btcSz);
     fill(txtCol);
     text(BTCPriceEUR + " €", startContentX, startContentY + textAscent());
     
     // display stat1
     textSize(statSz);
     String str = BTCLastPriceEUR + " €";
     float strW = textWidth(str);
     float posStat1X = startContentX + contentW - strW;
     text(str, posStat1X, startContentY + textAscent());
     posStat1X -= contentW * 0.18;
     text(stat1, posStat1X, startContentY + textAscent());
     
     // display stat2
     str = BTCVariation + " %";
     strW = textWidth(str);
     float posStat2X = startContentX + contentW - strW;
     text(str, posStat2X, startContentY + contentH - textAscent() / 2);
     text(stat2, posStat1X, startContentY + contentH - textAscent() / 2);
  } 
  
  void setPrice(String newPrice, String lastPrice, String newVariation) {
   BTCPriceEUR = newPrice;
   BTCLastPriceEUR = lastPrice;
   BTCVariation = newVariation;
  }
}