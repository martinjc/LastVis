class Slice {
  private float diameter;
  private float[] edges;
  private float[] midPoint;
  private Slice left;
  private Slice right;
  private String name;
  private String json;
  private int playcount;
  
  private ArrayList<Slice> slices;
  
  Slice(String json, String name, int playcount, float angleSum, float sliceAngle, float diameter){
    this.json = json;
    this.name = name;
    this.playcount = playcount;
    
    float[] edges = {angleSum, (angleSum+sliceAngle)};
    this.edges = edges;
    this.diameter = diameter;
    float[] midPoint = {width/2.0, height/2.0};
    this.midPoint = midPoint;
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
  
  void render(){
    fill(random(255), random(255),random(255)); //set colour
    arc(midPoint[0], midPoint[1], diameter, diameter, edges[0], edges[1]); //render slice
  }
  
  public void addSubSlice(Slice slice){
    if(slices == null){
      slices = new ArrayList<Slice>();
    }
    slices.add(slice);
  }
}
