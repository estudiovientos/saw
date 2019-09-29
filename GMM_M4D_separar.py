# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 11:45:01 2016

Este programa genera un archivo con los datos clasificados por estados 
(clusters_13_03st.txt)y una gráfica de los datos

@author: magali
rum_10=6
rum_11=6
rum_12=9
rum_13=3
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
import math

def formato():
    
    data = np.genfromtxt('./Archivos/rum_14_rot.csv',delimiter=',')    #Nombre del archivo a procesar
    lst1 = data[:,0]
    lst2 = data[:,1]
    lst3 = data[:,2]
    lst4 = data[:,3]
    lst1=[value for value in lst1 if not math.isnan(value)]
    lst2=[value for value in lst2 if not math.isnan(value)]
    lst3=[value for value in lst3 if not math.isnan(value)]
    lst4=[value for value in lst4 if not math.isnan(value)]
    print len(lst1), len(lst2),len(lst3), len(lst4)
  
    return lst1, lst2, lst3 , lst4


def sample():
    lst1,lst2,lst3, lst4 = formato()
    x=np.array(lst1,dtype='double')
    y=np.array(lst2,dtype='double')
    z=np.array(lst3,dtype='double')
    w=np.array(lst4,dtype='double')
    xmin=x.min()
    xmax=x.max()
    ymin=y.min()
    ymax=y.max()
    zmin=z.min()
    zmax=z.max()
    wmin=w.min()
    wmax=w.max()
   
    x1=x/(xmax-xmin)
    y1=y/(ymax-ymin)
    z1=z/(zmax-zmin)
    w1=w/(wmax-wmin)
    sz=len(lst1)  
    print sz

    samples = np.array([(x1[i],y1[i],z1[i],w1[i]) for i in range(len(x))])
    #samples = np.array([(x[i],y[i],z[i],w[i]) for i in range(len(x))])
    return samples    
    




def fit_samples(samples,num,nombre):
    #f0=open('./Resultados/Polar/clusters_04st.txt', 'w')    
    f0=open('./Resultados/Rumorosa/2014/clusters_4d_6G.txt', 'w')
    gmix = mixture.GMM(n_components=num, covariance_type='full', n_iter=800, random_state=60)
    #55
    gmix.fit(samples)
    
    dx = 0.01
    x = np.arange(np.min(samples[:,0]), np.max(samples[:,0]), dx)
    y = np.arange(np.min(samples[:,1]), np.max(samples[:,1]), dx)
    fl=samples[:,2]
#    print samples
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
#    ax.set_xlim([-17,17])
#    ax.set_ylim([-17,17])
    ax.set_xlim([-.8,.8])
    ax.set_ylim([-.8,.8])
    #ax.grid(True)
#    ax.set_xlabel('Velocidad (m/s)')    
#    ax.set_ylabel('Velocidad (m/s)')    
#    ax.set_title('Viento en La Rumorosa 2011')      
    ax.set_title('Wind in Rumorosa 2014')      
    ax.set_xlabel('Speed (m/s)')    
    ax.set_ylabel('Speed (m/s)')                 
    grp = gmix.predict(samples)
    tam=len(samples)
    print tam,"tam"
    cad=[]
    for i in range(tam):
        cad.append(0)
#
    idx =(grp==5)
    ax.scatter(samples[idx,0], samples[idx,1], c='b', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=6
          
    idx =(grp==4)    
    ax.scatter(samples[idx,0], samples[idx,1], c='m', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=5       

    idx =(grp==3)    
    ax.scatter(samples[idx,0], samples[idx,1], c='r', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=4       
    
    idx =(grp==2)
    ax.scatter(samples[idx,0], samples[idx,1], c='c', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=3       

    idx =(grp==1)
    #lila '#7b68ee'
    ax.scatter(samples[idx,0], samples[idx,1], c='g', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=2     
#1e90ff
            
    idx =(grp==0)
    ax.scatter(samples[idx,0], samples[idx,1], c='#7b68ee', alpha=0.1)
    for i in range(len(idx)):
        if str(idx[i])=='True':
           cad[i]=1
    for i in range(len(cad)):
        f0.write(str(cad[i])+","+str(fl[i])+"\n");

    f0.close()
  
    #plt.contour(X, Y, Z, 20, alpha=0.3)
    plt.savefig(nombre,dpi = 300, format="png")
    plt.show()
    plt.clf()
    #plt.close()
 
if __name__ == '__main__':
    s = sample()
    componentes=6
    #for i in range(4, componentes):
   # name= "./Resultados/Rumorosa/2011/rum2_4d_6G6"+str(componentes)+".png"
    name= "./Resultados/Rumorosa/2014/rum2014_g6_states"+".png"

    fit_samples(s, componentes, name)