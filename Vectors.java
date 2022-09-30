public class Main
{
	public static void main(String[] args) {
	    Vector vec=new Vector(1,0,0);
	    Vector vec2=new Vector(1,1,0);
	    
	    System.out.println("Vector 1");
	    System.out.println(vec.getInfo());
	    System.out.println("Vector 2");
	    System.out.println(vec2.getInfo());
	    System.out.println();
	    
	    System.out.print("Scalar product: ");
	    System.out.println(vec.scalarWith(vec2));
	    
	    System.out.print("Vector product: ");
	    (vec.vectorialWith(vec2)).display();
	    
	    System.out.print("Angle between: ");
	    System.out.println(vec.anglWith(vec2));
        
        System.out.println("Sum and difference:");
        (vec.sumWith(vec2)).display();
        (vec.diffWith(vec2)).display();
	}
}

class Vector{
    private double x,y,z;
    Vector(double xNew, double yNew, double zNew){
        x=xNew; y=yNew; z=zNew;
    }
    Vector(){
        x=Math.random()*20-10;
        y=Math.random()*20-10;
        z=Math.random()*20-10;
    }
    double getX()
    {
        return x;
    }
    double getY()
    {
        return y;
    }
    double getZ()
    {
        return z;
    }
    double length()
    {
        return Math.sqrt(x*x+y*y+z*z);
    }
    String toStr()
    {
        String result="("+Double.toString(x)+", "+Double.toString(y)+", "+Double.toString(z)+")";
        return result;
    }
    void display()
    {
        System.out.println(toStr());
    }
    String getInfo()
    {
        double angle=anglWith(new Vector(1,0,0));
        String result=toStr()+"\nLength: "+Double.toString(length())+"\nAngle with 0X:"+Double.toString(angle);
        return result;
    }
    
    
    double scalarWith(Vector two)
    {
        return getX()*two.getX()+getY()*two.getY()+getZ()*two.getZ();
    }
    Vector vectorialWith(Vector two)
    {
        Vector result=new Vector(getY()*two.getZ()-getZ()*two.getY(), getZ()*two.getX()-getX()*two.getZ(),
            getX()*two.getX()-getY()*two.getX());
        return result;
    }
    double anglWith(Vector two)
    {
        return((180*Math.acos(scalarWith(two)/(length()*two.length())))/Math.PI);
    }
    Vector sumWith(Vector two)
    {
        Vector result=new Vector(getX()+two.getX(), getY()+two.getY(), getZ()+two.getZ());
        return result;
    }
    Vector diffWith(Vector two)
    {
        Vector result=new Vector(getX()-two.getX(), getY()-two.getY(), getZ()-two.getZ());
        return result;
    }
}
