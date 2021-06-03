G00 S1; endstops
G00 E0; no extrusion
G01 S1; endstops
G01 E0; no extrusion
G21; millimeters
G91 G0 F300.0 Z8.000; pen park !!Zsafe
G90; absolute
G28 X; home
G28 Y; home
G28 Z; home
G00 F300.0 Z8.000; pen park !!Zpark
G00 F2400.0 Y8.000; !!Ybottom
G00 F2400.0 X7.000; !!Xleft
G00 F2400.0 X27.000 Y53.000; move !!Xleft+20.000 Ybottom+45.000
G00 F300.0 Z0.000; pen down !!Zwork
G01 F2100.0 X42.000 Y53.000; draw !!Xleft+35.000 Ybottom+45.000
G01 F2100.0 X42.000 Y38.000; draw !!Xleft+35.000 Ybottom+30.000
G01 F2100.0 X27.000 Y38.000; draw !!Xleft+20.000 Ybottom+30.000
G01 F2100.0 X27.000 Y53.000; draw !!Xleft+20.000 Ybottom+45.000
G00 F300.0 Z2.500; pen up !!Zup
G00 F2400.0 X17.000 Y33.000; move !!Xleft+10.000 Ybottom+25.000
G00 F300.0 Z0.000; pen down !!Zwork
G01 F2100.0 X32.000 Y33.000; draw !!Xleft+25.000 Ybottom+25.000
G01 F2100.0 X32.000 Y18.000; draw !!Xleft+25.000 Ybottom+10.000
G01 F2100.0 X17.000 Y18.000; draw !!Xleft+10.000 Ybottom+10.000
G01 F2100.0 X17.000 Y33.000; draw !!Xleft+10.000 Ybottom+25.000
G00 F300.0 Z2.500; pen up !!Zup
G00 F2400.0 X37.000 Y33.000; move !!Xleft+30.000 Ybottom+25.000
G00 F300.0 Z0.000; pen down !!Zwork
G01 F2100.0 X37.000 Y18.000; draw !!Xleft+30.000 Ybottom+10.000
G01 F2100.0 X52.000 Y18.000; draw !!Xleft+45.000 Ybottom+10.000
G01 F2100.0 X52.000 Y33.000; draw !!Xleft+45.000 Ybottom+25.000
G01 F2100.0 X37.000 Y33.000; draw !!Xleft+30.000 Ybottom+25.000
G00 F300.0 Z8.000; pen park !!Zpark