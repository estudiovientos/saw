# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:18:37 2016

@author: magali
"""
import sys
import math
import datetime, xlrd

f=open('foo02.csv', 'w')
#g=open('foo_01.csv', 'w')
for line in sys.stdin:
    a=line.split("\n")
    book = xlrd.open_workbook(a[0])
    sh = book.sheet_by_index(0)

    for rx in range(sh.nrows):
        a1 = sh.cell_value(rx, colx=1)
	print a1
        fecha = datetime.datetime(*xlrd.xldate_as_tuple(a1, book.datemode))
	print fecha
        try:
            velV= sh.cell_value(rx, colx=4)
            dirV= sh.cell_value(rx, colx=2)
            hum_rel= sh.cell_value(rx, colx=7)
            pre_atm= sh.cell_value(rx, colx=8)
            #print fecha, velV, dirV, hum_rel
#            x=(float(velV)/3.6)*math.cos(math.radians(float(dirV)))
 #           y=(float(velV)/3.6)*math.sin(math.radians(float(dirV)))   
            #rotar 
            y=(float(velV)/3.6)*math.cos(math.radians(float(dirV)))
            x=(float(velV)/3.6)*math.sin(math.radians(float(dirV)))   

            print fecha, x, y, hum_rel, pre_atm
            f.write(str(fecha)+","+str(x) +","+ str(y) +","+ str(hum_rel)+ ","+ str(pre_atm)+"\n")
        except:
            f.write(str(fecha)+",NaN,NaN,NaN,NaN\n")

            
        
f.close()
