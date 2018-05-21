import java.util.Map;

// OSC //
import oscP5.* ;                   
import netP5.*;
OscP5 oscP5;
int localhostadress = 8000;

// FONTS //
HashMap<String, PFont> fonts = new HashMap<String, PFont>();
PFont sanFranReg, sanFranSemiBold, sanFranBold, sanFranHeavy, monoSpaceNumbers;

// LAYOUT //
int bigTitleSz;
float borderW, borderH;
float headerH;
LiveSection liveSect;
PriceSection priceSect;
GraphSection graphSect;
ProgSection progSect;
ArrayList<Section> sections = new ArrayList<Section>();

// COLORS //
HashMap<String, Integer> palette = new HashMap<String, Integer>();

void setup() {
  // OSC parameters
  oscP5 = new OscP5(this, localhostadress) ;   // connect to OSC channel

  // window
  //size(1400, 1000);
  fullScreen();

  // canvas
  setupCanvas();
}

void draw() {
  // BACKGROUND
  background(palette.get("background"));

  // HEADER
  fill(palette.get("header"));
  //rect(0, 0, width, headerH);

  // TITLE
  fill(palette.get("header"));
  textFont(fonts.get("sanFranHeavy"));
  textSize(bigTitleSz);
  //ellipse(borderW, borderH + textAscent(), 10, 10);
  text("BTC", borderW, borderH + textAscent());
  
  //text("BTC", borderW, borderH);

  // SECTION 
  for (int i = 0; i < sections.size(); i++) {
    sections.get(i).show();
  }
}

// function that receives OSC messages
void oscEvent(OscMessage theOscMessage) {
  // debug
  //println(theOscMessage);

  // message when transactions happen
  if (theOscMessage.checkAddrPattern("/trans")==true)
  {
    // get value of transaction
    //transValueBTC = theOscMessage.get(0).floatValue();
    if (theOscMessage.arguments().length == 3) {      
      // create transaction element and add it
      Transaction newTrans = new Transaction(theOscMessage.get(0).stringValue(), "lol", theOscMessage.get(2).stringValue());
      liveSect.addTrans(newTrans);
    } else {
      print("TRANSACTION OSC MESSAGE DOES NOT HAVE 3 ARGUMENTS");
    }
  }

  // message when transactions happen
  if (theOscMessage.checkAddrPattern("/priceEUR")==true)
  {
    priceSect.setPrice(theOscMessage.get(0).stringValue(), theOscMessage.get(1).stringValue(), theOscMessage.get(2).stringValue());
  }

  // message when transactions happen
  if (theOscMessage.checkAddrPattern("/btcCounter")==true)
  {
    progSect.setCounter(theOscMessage.get(0).floatValue());
  }
}

void setupCanvas() {  
  // set fonts
  fonts.put("sanFranReg", createFont("fonts/SanFranciscoText-Regular.otf", map(height, 0, 1080, 12, 20)));
  fonts.put("sanFranHeavy", createFont("fonts/SanFranciscoText-Heavy.otf", map(height, 0, 1080, 12, 56)));
  fonts.put("sanFranSemiBold", createFont("fonts/SanFranciscoText-Semibold.otf", map(height, 0, 1080, 0, 24)));
  fonts.put("monoSpaceBold", createFont("fonts/MonospaceBold.ttf", map(height, 0, 1080, 12, 22)));
  fonts.put("monoSpace", createFont("fonts/Monospace.ttf", map(height, 0, 1080, 12, 22)));

  // set palette
  palette.put("header", #242D4A);
  palette.put("background", #DED9D4);
  palette.put("box", #F9F9F9);
  palette.put("text", #17203A);
  palette.put("content", #A13030);
  /*
  palette.put("header", #F8F0FB);
  palette.put("background", #070707);
  palette.put("box", #1A1A1A);
  palette.put("text", #F8F0FB);
  palette.put("content", #F8F0FB);
  */

  // set borders
  borderW = 0.02 * width;
  borderH = 0.03 * height;
  bigTitleSz = (int) map(height, 10, 1080, 12, 56);
  

  // set sizes and positions
  // header
  float headerSz = 0.1;
  headerH = headerSz * height;
  float rem = 1 - 3 * borderH / height - headerSz;
  float liveSecH = rem * 0.75;
  float priceSecH = rem * 0.25;
  float graphSecH = rem * 0.5;
  float progSecH = rem * 0.5;

  // live trade section
  liveSect = new LiveSection("Transactions en temps réel", 
    borderW, 
    borderH, 
    borderW, 
    headerH + borderH, 
    0.564 * width, 
    liveSecH * height, 
    palette, fonts);
  sections.add((Section) liveSect);

  // price section
  priceSect = new PriceSection("Prix du Bitcoin", 
    borderW, 
    borderH, 
    borderW, 
    headerH + borderH + liveSecH * height + borderH, 
    0.564 * width, 
    priceSecH * height, 
    palette, fonts);
  sections.add((Section) priceSect);

  // graph section
  graphSect = new GraphSection("Évolution temporelle", 
    borderW, 
    borderH, 
    borderW + 0.564 * width + borderW, 
    headerH + borderH + graphSecH * height + borderH, 
    0.376 * width, 
    graphSecH * height, 
    palette, fonts);
  sections.add((Section) graphSect);

  // progress section
  progSect = new ProgSection("Pièce libérée", 
    borderW, 
    borderH, 
    borderW + 0.564 * width + borderW, 
    headerH + borderH, 
    0.376 * width, 
    progSecH * height, 
    palette, fonts);
  sections.add((Section) progSect);
}