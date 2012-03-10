class LinearAlg{
  
  static float average(float[] a, float[] b){
   float[] avg = {([0]+b[0])*0.5, ([1]+b[1])*0.5};
   return avg;
  }
  
  static float polarToCart(float r, float theta){
   float[] cart = {r*cos(theta), r*sin(theta)};
   return cart;
  }
}
