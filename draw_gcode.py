import time
import re
from corexy import *
from stepper import *

Z_work=0
Z_park=2.5

class gcode_parse():
    #support G X Y Z
    syntax_tb=[
    '([GXYZ]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)',
    '([GXYZ]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)',
    '([GXYZ]\d+\.?\d*)[ ]*([XYZF]\d+\.?\d*)',
    '([GMXYZ]\d+\.?\d*)',    
   ]
    def __init__(self):
        self.x=0;
        self.y=0;
        self.z=0;  
        self.g=0 
        self.m=0   
        self.crules=[]
        print("gcode parse init, z to %d for init" % self.z)
        for rule in self.syntax_tb:            
            self.crules.append(re.compile(rule))
        
    def parse_one_gcode(self,line):
        xyz_update=0
        line = line.strip()
        #for rule in self.syntax_tb:
        for rule in self.crules:
            res=rule.search(line)
            #print(res)
            if res != None:  
                    #for word in res.groups():# 8266 no support groups()
                    for i in range(1,5):
                        try:
                            word=res.group(i)
                            #print(word)
                            if word != None:                                                     
                                digt=float(word[1:])
                                #print(digt) 
                                key=word[0]
                                if 'X' == key:
                                    self.x=digt
                                    xyz_update=1
                                elif 'Y' == key:
                                    self.y=digt
                                    xyz_update=1
                                elif 'Z' == key:
                                    self.z=digt
                                    xyz_update=1
                                elif 'G'== key:
                                    self.g=digt    
                                elif 'M'== key:
                                    self.m=digt                                                                     
                        #except Exception as e:
                        except IndexError as e:
                            #print(e)
                            #print("xyz %d %d %d" %(self.x,self.y,self.z))
                            return   xyz_update,self.x,self.y,self.z
        print("error parse:%s" % line)
        return   xyz_update,self.x,self.y,self.z

def cxy_run_xyz(cxy,sz,x,y,z):    
    
    if(z<=Z_work):
        ex,ey=cxy.draw_to(x,y)  
    else :         
        ex,ey=cxy.move_to(x,y) 
        
    set_z(sz,z)
    return ex,ey,z  
     
def cxy_run_one_gcode(cxy,sz,gp,line):
    update,x,y,z= gp.parse_one_gcode(line)
    if update:
        return cxy_run_xyz(cxy,sz,x,y,z)  
    else :
        return x,y,z  

def cxy_run_gcode_file(cxy,sz,gp,file_name):
    file = open(file_name, 'r')
    try:
        while True:
            text_line = file.readline()
            if text_line:
                print("line>",text_line)              
                lx,ly,lz=cxy_run_one_gcode(cxy,sz,gp,text_line)               
                print("xyz:",lx,ly,lz)
            else:
                print("no lines")
                break
    finally:
        file.close()

def test_print_speed(cxy,sz,gp):
    start = time.time()
    cxy_run_one_gcode(cxy,sz,gp,"G00 F2400.0 X0.0 Y100.0")
    print(time.time()-start)   
    cxy_run_one_gcode(cxy,sz,gp,"G00 F2400.0 X100.0 Y100.0")
    print(time.time()-start)  
    cxy_run_one_gcode(cxy,sz,gp,"G00 F2400.0 X200.0 Y200.0")
    print(time.time()-start)       

def parse_gcode_file(gp,file_name):
    file = open(file_name, 'r')
    try:
        while True:
            text_line = file.readline()
            if text_line:
                print(">",text_line)
                lx,ly,lz= gp.parse_one_gcode(text_line)
                print("xyz:",lx,ly,lz)
            else:
                print("no lines")
                break
    finally:
        file.close()


def test_gcode_parse():
    gp=gcode_parse()
    gp.parse_one_gcode("X17.37Y12.55")  
    gp.parse_one_gcode("X17.37 Y12.55")    
    gp.parse_one_gcode("X17.37   Y12.55")
    gp.parse_one_gcode("X17   Y12")    
    gp.parse_one_gcode("X17.5   Y12")    
    gp.parse_one_gcode("X17   Y12.5")    
    gp.parse_one_gcode("X30")  
    gp.parse_one_gcode("Y10")  
    gp.parse_one_gcode("G00 F2400.0 X0.0 Y0.0")
    gp.parse_one_gcode("G00 F300.0 Z15.000; pen down !!Zwork")
    gp.parse_one_gcode("G00 F300.0 Z17.500; pen up !!Zup")        

def draw_gcode_file(cxy,sz,gp,fn):    
    start = plat_time()
    cxy_run_gcode_file(cxy,sz,gp,fn)
    print(plat_time()-start)  
    plat_plot_show() 
    print("done")

#test speed upy 100mm/8s ; x86 py 100mm/3s
if __name__ == '__main__':
    sx = Stepper( 14, 12, -1, speed=5000,name="x")
    sy = Stepper( 4, 5, -1, speed=5000,name="y")
    sz = Stepper( 13, 16, -1, speed=5000,name="z",dir_invert=1)
    sz.enable()
    cxy=corexy(sx,sy)
    gp=gcode_parse()
    #test_gcode_parse()    
    #test_print_speed()  
    draw_gcode_file(cxy,sz,gp,"rmc_modern_young.svg.gcode")
    cxy_run_xyz(cxy,sz,0,0,0)
