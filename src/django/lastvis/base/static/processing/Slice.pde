class Slice {
  private float diameter;
  private float[] edges;
  private float[] midPoint;
  private Slice left;
  private Slice right;
  private String name;
  private String json;
  private int playcount;
  private int[] colour;
  private boolean leaf = false;
  private int randomGrey;
  
  static boolean renderingLeaf = false;
  
  int id;
  
  private boolean renderChildren;
  
  private ArrayList<Slice> slices;
  
  Slice(String json, String name, int playcount, float angleSum, float sliceAngle, float diameter, int id, boolean leaf){
    this.json = json;
    this.name = name;
    this.playcount = playcount;
    this.id = id;
    this.leaf = leaf;
    
    float[] edges = {angleSum, (angleSum+sliceAngle)};
    this.edges = edges;
    this.diameter = diameter;
    float[] midPoint = {width/2.0, height/2.0};
    this.midPoint = midPoint;
    
    colour = new int[3];
    colour[0] = (int)random(255);
    colour[1] = (int)random(255);
    colour[2] = (int)random(255);
    
    randomGrey = 200+random(20);
    
    renderChildren = false;
  }
  
  public String getName(){
    return this.name;
  }
  
  public float[] getEdges(){
    return this.edges;
  }
  
  public float getMidAngle(){
   return (edges[0]+edges[1])*0.5; 
  }
  
  public XMLElement getJson(){
    return json;
  }
  
  public int getPlaycount(){
    return playcount;
  }
  
  public float getDiameter(){
   return diameter; 
  }
  
  public int[] getColour(){
    return colour;
  }
  
  public void setRenderChildren(boolean b){
    renderChildren = b;
  }

  public boolean getRenderChildren(){
    return renderChildren;
  }
  
  void render(){
    if(renderChildren){
      if(slices != null){
        for(Slice slice: slices){
         slice.render();
        }
      }
    }else{
      //filter( BLUR, 1 );
      fill(colour[0], colour[1], colour[2]); //set colour
      
      float localDiameter = diameter;
      if(leaf){
        localDiameter*=1.5;
      }
      if(renderingLeaf && !leaf){
        filter(SOFT_LIGHT, 2.0);
       fill(randomGrey, randomGrey, randomGrey);
      } 
        
      arc(midPoint[0], midPoint[1], localDiameter, localDiameter, edges[0], edges[1]); //render slice
      
      float[] localCentre = {width/2.0, height/2.0};
      float midAngle = getMidAngle();
      float[] midSlice = LinearAlg.polarToCart(diameter, midAngle);
      float[] startSlice = LinearAlg.polarToCart(diameter, edges[0]);
      float[] endSlice = LinearAlg.polarToCart(diameter, edges[1]);
      
      //stroke(0);

      //line(localCentre[0], localCentre[1], midSlice[0], midSlice[1]);
      //line(localCentre[0], localCentre[1], midSlice[0], midSlice[1]);
      //noStroke();

    }
  }
  
  void bufferRender(PGraphics buffer){
    if(renderChildren){
      if(slices != null){
        for(Slice slice: slices){
         slice.bufferRender(buffer);
        }
      }
    }else{
      //print("local id = " + id);
      color idColor = getColor(id);
      //println(", local colour = " + idColor);
      buffer.fill(idColor);
      //buffer.fill(colour[0], colour[1], colour[2]); //set colour
      buffer.arc(midPoint[0], midPoint[1], diameter, diameter, edges[0], edges[1]); //render slice
    }
  }
  
  // id 0 gives color -2, etc.
  color getColor(int localId) {
    return -(localId + 2);
  }
  // color -2 gives 0, etc.
  int getId(color c) {
    return -(c + 2);
  }
  
  void renderText(){

    if(renderChildren){
      if(slices != null){
        for(Slice slice: slices){
         slice.renderText();
        }
      }
    }else{
      fill(0);
      float localDiameter = diameter;
      if(leaf){
        localDiameter*=1.5;
        fill(200, 0, 0);
      }
      
      float[] centre = {width/2.0, height/2.0};
      float midAngle = getMidAngle();
      float radius = (localDiameter*0.5+5);
      //if(radius < 0)radius = 20;
      float[] midSlice = LinearAlg.polarToCart(radius,midAngle);
      
      pushMatrix();
        translate(midSlice[0], midSlice[1]+4);
        translate(centre[0], centre[1]);
        rotate(midAngle); 
        if(midAngle > 3.141592653*0.5 && midAngle < 3.141592653*1.5){
          rotate(3.141592653);
          translate(-textWidth(name)*1.15, 0);
        }
        
        text(name, 0, 0);
      popMatrix();
    }
    
  }
  
  public void addSubSlice(Slice slice){
    if(slices == null){
      slices = new ArrayList<Slice>();
    }
    slices.add(slice);
  }
  
  public static Slice getClickedSlice(ArrayList<Slice> slices, int clickedId){
    //println("Clicked id: " + clickedId);
    for(Slice s: slices){
      if(clickedId == s.id){
        for(Slice unflag: slices){
          unflag.setRenderChildren(false);
        }
        s.renderChildren = true;
        renderingLeaf = true;
        return s;
      }
      //println("Possible ids: " + s.id);

    }
    for(Slice unflag: slices){
      unflag.setRenderChildren(false);
      renderingLeaf = false;
    }
    return null;
  }
}
