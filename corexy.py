from math import *
from stepper import *

STEP_PER_MM=0.0125
MM_PER_STEP=80

STEP_TMC2225_32_PER_MM=0.00125
MM_TMC2225_32_PER_STEP=800

#2GT 2mm per gear, 20 gear , 20*2=40mm a cycle
#1.8 per step, so 200 steps a cycle. then 0.2mm/step
trace_flg=0
def plat_plot_show():
     pass
	 
def plat_plot(x,y,para):
     pass

def axis_accm_step(acc,delta):
        acc+=delta
        step=0
        if 0==int(acc):   
            pass # less one step 
        else :          
            step=int(acc)
            acc-=int(acc)
        return acc,step

def set_z(sz,ez):
        acc_z=0
        zc=sz.position()
        z=float(zc)*STEP_TMC2225_32_PER_MM               
        dz = ez - z; 
        if 1:             
            print(">c:%d z:%f->%f dz:%f" % (zc,z,ez,dz)) 
        if abs(dz) < STEP_TMC2225_32_PER_MM:
            return ez
        c = floor(abs(8*dz) );
        if c >0 :
            del_z= (dz) /c          
            del_z= del_z*MM_TMC2225_32_PER_STEP   
            for  i in range(0,c) :
                acc_z,step=axis_accm_step(acc_z,del_z)
                sz.step(step)
        zc=sz.position()
        z=float(zc)*STEP_TMC2225_32_PER_MM
        if 1:             
            print(">>c:%d z:%f" % (zc,z))      
        return ez


class corexy():
    def __init__(self, sx, sy):
        self.sx=sx
        self.sy=sy
        self.x=0
        self.y=0 # the x,y postion is exist naturely
        self.acc_a=0;
        self.acc_b=0
        self.sx.enable()
        self.sy.enable()
        print("corexy init")

    def actually_positon(self):
        a=self.sx.position()
        b=self.sy.position()
        x=float((a+b)/2)*STEP_PER_MM
        y=float((a-b)/2)*STEP_PER_MM
        return a,b,x,y
    
    def draw_actually_positon(self,plot_flg):
        a,b,x,y=self.actually_positon()
        if trace_flg:
            print("a:%d b:%d x:%f ,y:%f" % (a,b,x,y))
        if plot_flg:
            plat_plot(x,y,'b.')
        else :
            plat_plot(x,y,'y.')
    def direction(self,delta):
        if delta> 0:
            return 1
        else :
            return -1
    
    def accm_step(self,acc,delta):
        acc+=delta
        step=0
        if 0==int(acc):   
            pass # less one step 
        else :          
            step=int(acc)
            acc-=int(acc)
        return acc,step
    
    def set_xy(self,ex,ey,plot_flg):
        if 1: 
            a,b,x,y=self.actually_positon()
            print(">a:%d b:%d x:%f ,y:%f" % (a,b,x,y))
        x=self.x
        y=self.y
        dx = ex - x;
        dy = ey - y;   
 
        c = floor(8 * sqrt(dx * dx + dy * dy));
        if c >0 :
            del_a= (dx+dy) /c
            del_b= (dx-dy) /c
            del_a= del_a*MM_PER_STEP
            del_b= del_b*MM_PER_STEP
            for  i in range(0,c) :
                #self.set_xy(x + (i * dx / c), y + (i * dy / c));
                self.acc_a,step=self.accm_step(self.acc_a,del_a)
                self.sx.step(step)
                self.draw_actually_positon(plot_flg)                
                #
                self.acc_b,step=self.accm_step(self.acc_b,del_b)
                self.sy.step(step)
                self.draw_actually_positon(plot_flg) 
         
        self.x=ex
        self.y=ey       
        if 1: 
            a,b,x,y=self.actually_positon()
            print(">>a:%d b:%d x:%f y:%f ex:%f ey:%f" % (a,b,x,y ,abs(ex-x),abs(ey-y)))
        return ex,ey
    
    def move_to(self,x,y):
        return self.set_xy(x,y,0)
    
    def draw_to(self,x,y):
        return self.set_xy(x,y,1)
    
    def get_xy(self):
        a,b,x,y=self.actually_positon()
        return x,y
    

def draw_rect(cxy,x,y,w,h):  
    cxy.move_to(x,y)
    cxy.draw_to(x,y+h)
    cxy.draw_to(x+w,y+h)
    cxy.draw_to(x+w,y)
    cxy.draw_to(x,y)   

    
def  draw_cycle(cxy,x,y,r):
    cxy.move_to(x+r,y)
    for i in range(0,2*314,2):
      print(i) 
      a=float(i)/100   
      cxy.draw_to(x+r*cos(a),y+r*sin(a))
   
        

if __name__ == '__main__':
    sx = Stepper( 14, 12, 13, speed=10000,name="x")
    sy = Stepper( 4, 5, 16, speed=10000,name="y")
    cxy=corexy(sx,sy)
    draw_rect(cxy,10,10,10,10)
    draw_cycle(cxy,20,20,20)
    plat_plot_show() 