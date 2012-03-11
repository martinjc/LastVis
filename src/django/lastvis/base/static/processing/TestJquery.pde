private ArrayList<Slice> genres;
private int fontSize;
private double pi2 = 2.0*3.141592653;

Slice addData(String jsonData){
  //printMessage(xmlString);
  //printMessage(xmlString.chart.genres[0].name);
  
  //String bob = jsonData.chart.genres[0].name;
  //println(bob);
    
  //XMLElement data = new XMLElement(xmlString);

  int totalplaycount = jsonData.chart.playcount;
  //println("jsonplaycount" + totalplaycount);
  //int totalplaycount = .getAttribute("playcount");

  String[] children = jsonData.chart.genres;
  //println("Jsontest " + children[0].playcount); 

  genres = new ArrayList<Slice>();

  //Construct genre slices
  double angleSum = 0;
  for(String genre: children){ //Per slice
    String name = genre.name;
    int playcount = genre.playcount;
    float sliceAngle = pi2*((double)playcount/(double)totalplaycount);
    genres.add(new Slice(genre, name, playcount, angleSum, sliceAngle, ((float)min(width, height) * (random(0.3)+0.7))));
    angleSum+=sliceAngle;
  }

  for(Slice genre: genres){
    populateSliceList(genre);
  }

  /*for(Slice genre: genres){
    print(genre.getName() + "," + "(" + genre.getPlaycount() + " plays)");
     for(Slice artist: genre.slices){
       println("\t"+artist.getName() + ", " + artist.getPlaycount() + " plays");
     }
  }*/

  render();
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
      float subSliceAngle = diffAngle*((double)subSlicePlaycount/(double)slicePlaycount);
      slice.addSubSlice(new Slice(subSlice, name, subSlicePlaycount, angleSum, subSliceAngle, slice.getDiameter()));
      angleSum+=subSliceAngle;
    }
}

void setup(){
  size(300, 300);
  background(255);
  smooth();
  noStroke();
  fontSize = 16;
  textFont(loadFont("Ziggurat-HTF-Black-32.vlw"), fontSize);
}

void render(){
  for (Slice slice: genres){
    //Slice slice = genres.get(4);
    //slice.render();
    for(Slice sub: slice.slices){
      sub.render();
    }
  }
  for(Slice s: genres){
    renderSliceText(s);
  }
}

void renderSliceText(Slice slice){

  float[] centre = {width/2.0, height/2.0};
  float midAngle = slice.getMidAngle();
  float[] midSlice = LinearAlg.polarToCart(slice.diameter*0.3,midAngle);

  midSlice[0] += slice.midPoint[0];
  midSlice[1] += slice.midPoint[1];
  midSlice[0] -= textWidth(slice.getName())*0.5;

  fill(0);
  text(slice.getName(), midSlice[0], midSlice[1]);
}

