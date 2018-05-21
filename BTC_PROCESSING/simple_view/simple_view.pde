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
ArrayList<Section> sections = new ArrayList<Section>();

// COLORS //
HashMap<String, Integer> palette = new HashMap<String, Integer>();

void setup() {
    // OSC parameters
  oscP5 = new OscP5(this, localhostadress) ;   // connect to OSC channel

  // window
   //size(1000, 1000);
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
    // create transaction element and add it
    Transaction newTrans = new Transaction(theOscMessage.get(0).stringValue(), theOscMessage.get(2).stringValue());
    liveSect.addTrans(newTrans);
  }
}

void setupCanvas() {  
  // set fonts
  fonts.put("sanFranReg", createFont("fonts/SanFranciscoText-Regular.otf", map(height, 0, 1080, 12, 20)));
  fonts.put("sanFranHeavy", createFont("fonts/SanFranciscoText-Heavy.otf", map(height, 0, 1080, 12, 56)));
  fonts.put("sanFranSemiBold", createFont("fonts/SanFranciscoText-Semibold.otf", map(height, 0, 1080, 0, 24)));
  fonts.put("monoSpace", createFont("fonts/monaco.ttf", map(height, 0, 1080, 12, 22)));
  fonts.put("monoSpaceBold", createFont("fonts/NotoMono-Regular.ttf", map(height, 0, 1080, 12, 22)));

  // set palette
  palette.put("header", #010101);        
  palette.put("background", #010101);
  palette.put("box", #1A1A1A);
  palette.put("text", #F2F2F2);
  palette.put("content", #DDDDDD);

  // set borders
  borderW = 0.01 * width;
  borderH = 0.01 * height;
  bigTitleSz = (int) map(height, 10, 1080, 12, 56);  

  // set sizes and positions
  // header
  float headerSz = 0.0;
  headerH = headerSz * height;
  
  // liveSection
  float liveSecW = width - 2 * borderW;
  float liveSecH = height - 2 * borderH;  

  // live trade section
  liveSect = new LiveSection("", 
    borderW, 
    borderH, 
    borderW, 
    headerH + borderH, 
    liveSecW, 
    liveSecH,  
    palette, fonts);
  sections.add((Section) liveSect);
}