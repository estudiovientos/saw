# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:35:56 2016

@author: mag

Abre un archivo de 2 columnas, la primera son los vientos de santana, 
la segunda estados calculados por gmm.
genera como salida 2 archivos:
prob_13_03st_vs.txt en este se encuentran las coincidencias de ambas columnas leidas
edos_13_03_sep.txt un archivo con los estados separados por columnas
"""

import numpy as np
data=np.genfromtxt('./Resultados/Rumorosa/2012/estados4d_kraf_2012.csv', delimiter=',')
f0=open('./Resultados/Rumorosa/2011/prob_12_06_st_vs.txt', 'w')
#f1=open('./Resultados/Rumorosa/mix/prob_mix_06st_fm.txt', 'w')
f2=open('./Resultados/Rumorosa/2011/edos_12_06_sep.txt', 'w')
f3=open('./Resultados/Rumorosa/2011/p_coin_12_06_sep.txt', 'w')
vs=data[:,0]
st=data[:,2]

sz=len(vs)
st1=np.zeros(sz)
st2=np.zeros(sz)
st3=np.zeros(sz)
st4=np.zeros(sz)
st5=np.zeros(sz)
st6=np.zeros(sz)
#st7=np.zeros(sz)

for i in range(len(vs)):
    if vs[i]==1 and st[i]==1:
        st1[i]=1 #arreglo de coincidencias de 1's
        f0.write('1'+"\t")
    else:
        f0.write('0'+"\t")
    
    if vs[i]==1 and st[i]==2:
        st2[i]=1
        f0.write('1'+"\t")
    else:
        f0.write('0'+"\t")
    
    if vs[i]==1 and st[i]==3:
        st3[i]=1
        f0.write('1'+"\t")
    else:
        f0.write('0'+"\t")
        
    if vs[i]==1 and st[i]==4:
        st4[i]=1
        f0.write('1'+"\t")
    else:
        f0.write('0'+"\t")

    if vs[i]==1 and st[i]==5:
        st5[i]=1
        f0.write('1'+"\t")
    else:
        f0.write('0'+"\t")


    if vs[i]==1 and st[i]==6:
        st6[i]=1
        f0.write('1'+"\n")
    else:
        f0.write('0'+"\n")

       
#              
f0.close()
#        

for i in range(len(st)):
    if st[i]==1:
        
        f2.write('1'+'\t')
    else:
        f2.write('0'+'\t')
        
    if st[i]==2:
        f2.write('1'+'\t')
        
    else:
        f2.write('0'+'\t')
    if st[i]==3:
        f2.write('1'+'\t')
        
    else:
        f2.write('0'+'\t')
        
    if st[i]==4:
        f2.write('1'+'\t')
        
    else:
        f2.write('0'+'\t')
    if st[i]==5:
        f2.write('1'+'\t')
        
    else:
        f2.write('0'+'\t')
        
    if st[i]==6:
        f2.write('1'+'\n')
        
    else:
        f2.write('0'+'\n')


f2.close() 
data1=np.genfromtxt('./Resultados/Rumorosa/2012/edos_12_06_sep.txt', delimiter='\t')   
d1=data1[:,0]
d2=data1[:,1]
d3=data1[:,2]
d4=data1[:,3]
d5=data1[:,4]
d6=data1[:,5]

c1=0
c2=0
c3=0
c4=0
c5=0
c6=0

#coincidencias totales por estado
for i in range(len(vs)):
    if (vs[i]==1 and d1[i]==1)or(vs[i]==0 and d1[i]==0):
        c1+=1   
    
    if (vs[i]==1 and d2[i]==2)or(vs[i]==0 and d2[i]==0):
        c2+=1
    
    if (vs[i]==1 and d3[i]==3)or(vs[i]==0 and d3[i]==0):
        c3+=1
        
    if (vs[i]==1 and d4[i]==4)or(vs[i]==0 and d4[i]==0):
        c4+=1
        
    if (vs[i]==1 and d5[i]==5)or(vs[i]==0 and d5[i]==0):
        c5+=1

    if (vs[i]==1 and d6[i]==6)or(vs[i]==0 and d6[i]==0):
        c6+=1  

   
      
vs_nz=float(len(vs))#numero total de registros
v_nz=np.count_nonzero(vs) #todos los unos en la medición experimental
print "longitud",vs_nz, "unos",v_nz

u1=float(np.count_nonzero(st1))#numero de 1's que coincidieron
print c1,u1
if c1==0: c1=1
print "Estado 1 , total", float(c1/vs_nz)*100  #porcentaje del total de coincidencias
print "porcentaje de 1s", float(u1/v_nz)*100,"\n"
f3.write("Estado 1 , total" + str(float(c1/vs_nz)*100) +"\n")  #porcentaje del total de coincidencias
f3.write("porcentaje de 1s"+ str(float(u1/v_nz)*100)+"\n")


u2=float(np.count_nonzero(st2))
print c2,u2
if c2==0: c2=1
print "Estado 2 , total ", float(c2/vs_nz)*100 
print "porcentaje de 1s ", float(u2/v_nz)*100 ,"\n"
f3.write("Estado 2 , total " + str( float(c2/vs_nz)*100)+"\n")
f3.write("porcentaje de 1s " + str(float(u2/v_nz)*100) +"\n")

print c3
u3=float(np.count_nonzero(st3))
if c3==0: c3=1
print "Estado 3 , total ", float(c3/vs_nz)*100 
print "porcentaje de 1s ", float(u3/v_nz)*100 ,"\n"
f3.write( "Estado 3 , total "+ str(float(c3/vs_nz)*100)+"\n" )
f3.write("porcentaje de 1s "+ str(float(u3/v_nz)*100) +"\n")

print c4
u4=float(np.count_nonzero(st4))
if c4==0: c4=1
print "Estado 4 , total ", float(c4/vs_nz)*100
print "porcentaje de 1s ", float(u4/v_nz)*100,"\n"
f3.write("Estado 4 , total "+ str(float(c4/vs_nz)*100)+"\n")
f3.write( "porcentaje de 1s "+str(float(u4/v_nz)*100)+"\n")

print c5
u5=float(np.count_nonzero(st5))
if c3==0: c5=1
print "Estado 5 , total", float(c5/vs_nz)*100 
print "porcentaje de 1s", float(u5/v_nz)*100,"\n"
f3.write( "Estado 5 , total " +str(float(c5/vs_nz)*100)+ "\n")
f3.write( "porcentaje de 1s "+str(float(u5/v_nz)*100)+"\n")


print c6
u6=float(np.count_nonzero(st6))
if c6==0: c6=1
print "Estado 6 , total ", float(c6/vs_nz)*100 
print "porcentaje de 1s ", float(u6/v_nz)*100,"\n"
f3.write( "Estado 6 , total " + str(float(c6/vs_nz)*100)+"\n")
f3.write( "porcentaje de 1s "+str(float(u6/v_nz)*100)+"\n")


f3.close()