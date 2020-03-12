# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:06:06 2017

elimina cadenas que sean menores a 3 hrs de ocurrencias de los vientos de sw

@author: mag
"""

import numpy as np
import math

def formato():
    data = np.genfromtxt('./Resultados/Rumorosa/2014/edo_k.csv',delimiter=',')
    lst1 = data[:,1]  
    lst1=[value for value in lst1 if not math.isnan(value)]
    return lst1

if __name__ == '__main__':
    
    g=open("./Resultados/Rumorosa/2014/edo_kf.csv","w")
    #aux=np.array(lst1,dtype='double')
    aux=[]
    swap=[]
    indice=[]
    k=0
    original=formato()
    #obtener indices de los ceros en el arreglo original
    for i in range(len(original)):        
        if original[i]==0:
            #print original[i]
            indice.append(i)
    #copiar el arreglo original a un auxiliar
    #print indice
    for i in range(len(original)):
        aux.append(original[i])
    #obtner distancias
    for i in range(len(indice)-1):
        dis=indice[i+1]-indice[i]
        #print dis
        lon=18+1
        if dis!=1:
            if dis<lon:
                for j in range(dis):
                    aux[indice[i]+j]=0

    #print len(aux), aux
    for i in range(len(aux)):
        g.write(str(aux[i])+"\n")  
    
    g.close()
                        
