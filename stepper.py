from machine import Pin
import time

DEFAULT_SPEED = 10000
GT2_20_cycle_40mm_STEPS=200*16

def plat_time():
	return  time.ticks_ms()  

def  xsleep_us(vus):
    #pass
    time.sleep_us(vus)

dbg_flg=0 #set 1 for debug info
                   
class Stepper():
    def __init__(self, dir_pin, step_pin, enable_pin ,  speed=DEFAULT_SPEED,name="",dir_invert=0):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.dir_invert=dir_invert
        self.direction = 1
        if self.dir_invert :
            self.dir_pin.value(0) 
        else :
            self.dir_pin.value(1)  
        self.step_pin.value(0) 
        if enable_pin > 0:
            self.enable_pin = Pin(enable_pin, Pin.OUT)
            self.enable_pin.value(1)  
            self.enable_flg=0;       
        else:
            self.enable_flg=-1 
        self.pulserate = 100
        self.count = 0
        self.speed = speed
        self.delay = int(1000000/speed)  
        self.limits_max=GT2_20_cycle_40mm_STEPS*20
        self.limits_min=-GT2_20_cycle_40mm_STEPS*20
        self.name=name
        print("%s delaly %d us" %(name,self.delay))
        
    def enable(self):
        if self.enable_flg != -1:
            self.enable_pin.value(0)  
            self.enable_flg=1 
            print("%s enable" % self.name)
        else:
            print("%s stop ignored" % self.name)
    
    def dir(self,direction=1):
        if direction != self.direction :
            if 1 == direction:
                self.direction=1  
                if self.dir_invert :
                    self.dir_pin.value(0) 
                else :
                    self.dir_pin.value(1)              
            else :
                self.direction=-1  
                if self.dir_invert :         
                    self.dir_pin.value(1)
                else :
                    self.dir_pin.value(0)
                
            print("%s dir:  %d" %(self.name,self.direction))
    
    def step(self, count):
        """Rotate count steps. direction = -1 means backwards"""
        if 0 == count:
            return 
        if 0 == self.enable_flg:
            print("%s disable,need enable" % self.name)
        
        if dbg_flg:
            print("%s step cnt:%d" % (self.name,count))
        if count < 0:
           # print("negtive count input %d" % count)
            count=-(count)
            direction=-1
        else :
            direction=1
        
        self.dir(direction)
            
        for x in range(count):
            if(direction == 1 and self.position() < self.limits_min ):
                print("%s MIN limit %d %d" %(self.name,self.position(),self.limits_min))
                return False
            if(direction == -1 and self.position() > self.limits_max ):
                print("%s MAX limit %d %d" %(self.name,self.position(),self.limits_max ))
                return False
            self.step_pin.on()
            xsleep_us(self.delay)
            self.step_pin.off()
            xsleep_us(self.delay)
            self.count += direction
        if dbg_flg:
            print("%s postion %d" % (self.name,self.position()))
        return True        
           
    def stop(self):
        if self.enable_flg != -1:
            self.enable_pin.value(1)   
            self.enable_flg=0
            print("%s stop" % self.name)
        else:
            print("%s stop ignored" % self.name)            
        
    def setSpeed(self,speed):
        self.delay = 1000/speed
        
    def position(self):
        return self.count
    
if __name__ == '__main__':    
    sx = Stepper(14, 12, 13, speed=10000,name="x")
    sx.step(5)
    sx.enable()
    sx.step(5)
    sx.step(-15)
    sx.step(20)
    sx.stop()
    sy = Stepper( 4, 5, 13, speed=10000,name="y")
    sy.enable()
    sy.step(5)
    start = plat_time()
    sy.step(GT2_20_cycle_40mm_STEPS)
    sy.step(-GT2_20_cycle_40mm_STEPS)
    end = plat_time()
    print("start",start)
    print("end",end)
    print("cost:" , end-start)  
