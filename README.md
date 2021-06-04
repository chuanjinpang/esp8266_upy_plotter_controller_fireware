# esp8266_upy_plotter_controller_fireware

https://blog.csdn.net/pcj2007/article/details/117549520?spm=1001.2014.3001.5501

开源供大家参考。

网上很多用marlin固，glrb固件的方案，我觉得用micropython写个原型机固件要容易点，果然400行就可以演示了。

方案：

esp8266 + micropython + 3d打印机
![image](https://github.com/chuanjinpang/esp8266_upy_plotter_controller_fireware/blob/main/svg_gcode_sample/machine.png)


技术实现：

分了３个模块，

stepper.py　	
实现42步进驱动 A4988 或者TMC2225，驱动dir/step/en.　

step(self, count)实现方向转动step，负值是反向，正值是挂电正向转step.

由于8266实际可用GPIO脚太少，只有6个可安全任意使用，其它脚会引起一些问题，比如使用GPIO15影响下载，运行后下载就状态不对了。

corexy.py	
实现corexy的位置控制，

set_xy(self,ex,ey)驱动X,Y轴位置

set_z(sz,ez)驱动Z轴位置

注意这里Z轴是独立的，不是corexy的部件，原因是Z本身是独立的，如果是激光绘制，就没有Z轴步进的概念，只有一个控制信号。

可能将来会做一个激光雕刻的原型机。

draw_gcode.py	
实现gcode绘制

draw_gcode_file(cxy,sz,gp,"3rect.svg.gcode")绘制指定的gcode.

由一个gcode_parse来解析gcode,支持最多４个参数。

def cxy_run_gcode_file(cxy,sz,gp,file_name)　

解析器单独运行，负责解析，然后调用cxy_run_xyz（）驱动3轴运行。

def cxy_run_one_gcode(cxy,sz,gp,line):
    update,x,y,z= gp.parse_one_gcode(line)
    if update:
        return cxy_run_xyz(cxy,sz,x,y,z)  
    else :
        return x,y,z  

操作步骤：

1.用inkscape生成svg文件，也可以用其他

2.转换成gcode.zwork是0,提笔4mm.

3.上传gcode到8266 flash

4.手工调z轴到纸面zwork

5.运行程序指定gcode文件

代码放github供大家参考：https://github.com/chuanjinpang/esp8266_upy_plotter_controller_fireware

![image](https://github.com/chuanjinpang/esp8266_upy_plotter_controller_fireware/blob/main/svg_gcode_sample/hlw-draw.png)


https://www.bilibili.com/video/bv1254y137xn

