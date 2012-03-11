private ArrayList<Slice> genres;
private int fontSize;
private double pi2 = 2.0*3.141592653;
boolean ready = false;
PGraphics buffer;
private int idCount;
private double zoomLevel = 1.0;


Slice addData(String jsonData){

  int totalplaycount = jsonData.chart.playcount;

  String[] children = jsonData.chart.genres;

  genres = new ArrayList<Slice>();
  
  int totalNumArtists = calcTotalNumArtists(children);

  //Construct genre slices
  double angleSum = 0;
  for(String genre: children){ //Per slice
    String name = genre.name;
    name = name.charAt(0).toUpperCase() + name.slice(1);
    int playcount = genre.playcount;
    //float sliceAngle = pi2*((double)playcount/(double)totalplaycount);
    String[] artists = genre.artists;
    //println("Total artists = " + 
    float sliceAngle = pi2*((float)artists.length/(float)totalNumArtists);
    //genres.add(new Slice(genre, name, playcount, angleSum, sliceAngle, ((float)min(width, height)*0.5 * (random(0.3)+0.7)), idCount, false));
    genres.add(new Slice(genre, name, playcount, angleSum, sliceAngle, ((float)playcount/(float)totalplaycount+0.3)*500, idCount, false));
    idCount++;
    angleSum+=sliceAngle;
  }

  for(Slice genre: genres){
    populateSliceList(genre);
  }

  ready = true;
  //render();
}

int calcTotalNumArtists(String[] genres){
  int total = 0;
  for(String genre: genres){
    String[] artists = genre.artists;
    total+=artists.length;
  }
  return total;
}

void populateSliceList(Slice slice){
    int slicePlaycount = slice.getPlaycount();
    float minAngle = slice.edges[0];
    float maxAngle = slice.edges[1];
    float diffAngle = maxAngle-minAngle;
    int angleSum = minAngle;
    String[] children = slice.getJson().artists;
    for(String subSlice: children){
      String name = subSlice.name;
      int subSlicePlaycount = subSlice.playcount;
      //float subSliceAngle = diffAngle*((float)subSlicePlaycount/(float)slicePlaycount);
      float subSliceAngle = diffAngle*((float)1.0/(float)children.length);
      //println("Angle = " + subSliceAngle + "," + children.length + "/" + slicePlaycount);
      //slice.addSubSlice(new Slice(subSlice, name, subSlicePlaycount, angleSum, subSliceAngle, slice.getDiameter(), idCount, true));
      slice.addSubSlice(new Slice(subSlice, name, subSlicePlaycount, angleSum, subSliceAngle, ((float)slicePlaycount/(float)subSlicePlaycount+35)*3.5, idCount, true));
      idCount++;
      angleSum+=subSliceAngle;
    }
}

void setup(){
  idCount = 0;
  size(600, 600);
  buffer = createGraphics(width, height);
  lights();
  smooth();
  noStroke();
  fontSize = 16;
  textFont(loadFont("Ziggurat-HTF-Black-32.vlw"), fontSize);
}

void draw(){
  
  /*camera(0, 0, 800.0, // eyeX, eyeY, eyeZ
         width/2.0, height/2.0, 0.0, // centerX, centerY, centerZ
         0.0, 1.0, 0.0); // upX, upY, upZ*/
  //scale(zoomLevel);
         
  if(ready){
    beginDraw();
    background(255);
    for (Slice slice: genres){
        slice.render();
    }

    for(Slice slice: genres){
      slice.renderText();
    }
    //println(genres.get(0).renderingLeaf);
  }
  

  
}

void mouseScrolled() {
  if (mouseScroll > 0) {
    zoomLevel+=0.2;
  } else if (mouseScroll < 0) {
    zoomLevel-=0.2;
  }
}

void mouseClicked() {
  buffer.beginDraw();
  //buffer.scale(zoomLevel);
  buffer.background(getColor(-1)); // since background is not an object, its id is -1
  buffer.noStroke();
  /*buffer.camera(0, 0, 800.0, // eyeX, eyeY, eyeZ
         width/2.0, height/2.0, 0.0, // centerX, centerY, centerZ
         0.0, 1.0, 0.0); // upX, upY, upZ*/
  for (Slice slice: genres){
    slice.bufferRender(buffer);
  }
  //image(buffer, 50, 50);
  buffer.endDraw();
  //buffer.save("BufferTest.png");
  color buffcolour = buffer.get(mouseX, mouseY);
  Slice clickedSlice = Slice.getClickedSlice(genres, getId(buffcolour));
  //println("ID: " + getId(buffcolour));
}

// id 0 gives color -2, etc.
color getColor(int id) {
  return -(id + 2);
}
 
// color -2 gives 0, etc.
int getId(color c) {
  return -(c + 2);
}
