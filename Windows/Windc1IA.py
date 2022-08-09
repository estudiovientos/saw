"""
El software WindClIA genera clasificaciones automatizadas de los distintos estados de vientos 
en una serie de datos históricos procedente de las EMAS, reduciendo así el tiempo de limpieza,
ordenamiento de información de archivos provenientes de EMAS. Al poder estudiar grandes cantidades 
de datos, estas clasificaciones permiten, por ejemplo, estudiar de forma rápida el potencial eólico
de diferentes zonas. El software WindC1IA genera como salida gráfica de estados de viento y archivos 
que agilizan el análisis realizado por los expertos del área.


Autores: Magali Arellano Vazquez, Carlos Minutti Martinez y Fernando Aarón Huerta Sánchez.
"""



import os
import xlrd
import datetime
import xlsxwriter
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
import pandas as pd
import matplotlib.ticker as ticker
import zipfile
import shutil
import sys


"""
Función clearDataProcess: Elimina las carpetas y archivos 
generados al iniciar con el procedimiento del programa.
"""
def clearDataProcess():
    
    #Eliminar archivos de las carpetas
    newFormat1 = glob.glob('./Resultados/processFiles/newFormat1/*.xls')
    for py_file in newFormat1:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    newFormat2 = glob.glob('./Resultados/processFiles/newFormat2/*.xls')
    for py_file in newFormat2:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    clusters = glob.glob('./Resultados/processFiles/clusters/*.xls')
    for py_file in clusters:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    graphs = glob.glob('./Resultados/processFiles/graphs/*.png')
    for py_file in graphs:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    idxTrue = glob.glob('./Resultados/processFiles/idxTrue/*.xls')
    for py_file in idxTrue:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    idxTrue_clusters = glob.glob('./Resultados/processFiles/idxTrue_clusters/*.xls')
    for py_file in idxTrue_clusters:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    mainxls = glob.glob('./Resultados/processFiles/mainxls/*.xls')
    for py_file in mainxls:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    stdProd = glob.glob('./Resultados/processFiles/stdProd/*.xls')
    for py_file in stdProd:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    acInputCSV = glob.glob('./Resultados/processFiles/acInput/*.csv')
    for py_file in acInputCSV:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    acInputXLS = glob.glob('./Resultados/processFiles/acInput/*.xls')
    for py_file in acInputXLS:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")

    ## Eliminar solo archivos de cache de la carpeta
    # acInputXLS = glob.glob('./__pycache__/*.pyc')
    # for py_file in acInputXLS:
    #     try:
    #         os.remove(py_file)
    #     except OSError as e:
    #         print(f"Error:{ e.strerror}")

    #Elimina carpeta vacia
    try:
        os.rmdir("./Resultados/processFiles/newFormat1")
    except:
        pass

    try:
        os.rmdir("./Resultados/processFiles/newFormat2")
    except:
        pass

    try:
         os.rmdir("./Resultados/processFiles/mainxls")
    except:
        pass

    try:
         os.rmdir("./Resultados/processFiles/clusters")
    except:
        pass 

    try:
         os.rmdir("./Resultados/processFiles/idxTrue")
    except:
        pass

    try:
         os.rmdir("./Resultados/processFiles/idxTrue_clusters")
    except:
        pass

    try:
         os.rmdir("./Resultados/processFiles/stdProd")
    except:
        pass

    try:
         os.rmdir("./Resultados/processFiles/acInput")
    except:
        pass 

    
    try:
         os.rmdir("./Resultados/processFiles")
    except:
        pass

    # # Elimina carpeta con archivos
    # rmtree("./__pycache__")


"""
Función clearResults: Elimina los resultados de la carpeta 
Archivos una vez iniciado el proceso nuevamente.
"""
def clearResults():
    resultsXLS = glob.glob('./Resultados/*.xls')
    for py_file in resultsXLS:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")


    resultsPNG = glob.glob('./Resultados/*.png')
    for py_file in resultsPNG:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")


    resultsZIP = glob.glob('./Resultados/*.zip')
    for py_file in resultsZIP:
        try:
            os.remove(py_file)
        except OSError as e:
            print(f"Error:{ e.strerror}")


"""
Función mainFiles: Crea las carpetas principales para la ejecución 
del programa.
"""
def mainFiles():
    try:
        os.mkdir('./Resultados')
        os.mkdir('./Archivos')
    except:
        pass


"""
Función createFiles: Crea las carpetas de los 
procedimientos al iniciar el análisis.
"""
def createFiles():
    os.mkdir('./Resultados/processFiles')
    os.mkdir('./Resultados/processFiles/newFormat1')
    os.mkdir('./Resultados/processFiles/newFormat2')
    os.mkdir('./Resultados/processFiles/mainxls')
    os.mkdir('./Resultados/processFiles/clusters')
    os.mkdir('./Resultados/processFiles/idxTrue')
    os.mkdir('./Resultados/processFiles/idxTrue_clusters')
    os.mkdir('./Resultados/processFiles/stdProd')
    os.mkdir('./Resultados/processFiles/acInput')


"""
Función info: Recolecta información del sistema operativo y de los datos.
"""
def info(numClusters):
    stationFiles = os.listdir('.\\Archivos')
    firstFile = stationFiles[0]

    path = f".\\Archivos\\{firstFile}"
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)

    firstValue = worksheet.cell_value(1, 0)
    lastValue = worksheet.cell_value(1, worksheet.ncols-1)

    if isinstance(firstValue, str):
        nameEstacion = firstValue
        dateValue = firstValue = worksheet.cell_value(1, 1)

        converted_date = xlrd.xldate_as_tuple(
            dateValue, workbook.datemode)
        print_date = datetime.datetime(
            *converted_date).strftime("%d/%m/%Y %H:%M")
        
        return nameEstacion, print_date[6:11], numClusters

    elif isinstance(lastValue, str):
        nameEstacion = lastValue
        dateValue = firstValue = worksheet.cell_value(1, 0)

        converted_date = xlrd.xldate_as_tuple(
            dateValue, workbook.datemode)
        print_date = datetime.datetime(
            *converted_date).strftime("%d/%m/%Y %H:%M")

        return nameEstacion, print_date[6:10], numClusters


"""
Función formats: Permite la limpieza de los datos de entrada, quitando el encabezado, el nombre de la estación
independientemente si esta al inicio o al final y arregla el formato de la fecha, los archivos generados se 
guardan en la carpeta de newFormat1.
"""
def formats():
    # Entrar a la carpeta de todos los archivos
    stationFiles = os.listdir('.\\Archivos')
    numDatos = len(stationFiles)

    for i in range(0, numDatos):
        # Abrir un archivo
        old_path = f".\\Archivos\\{stationFiles[i]}"
        old_workbook = xlrd.open_workbook(old_path)
        old_worksheet = old_workbook.sheet_by_index(0)

        # Crea el nuevo archivo modificado
        new_path = f".\\Resultados\\processFiles\\newFormat1\\Nuevo_{stationFiles[i]}"
        new_workbook = xlsxwriter.Workbook(new_path)
        new_worksheet = new_workbook.add_worksheet()

        for row in range(old_worksheet.nrows):
            for col in range(old_worksheet.ncols):
                if(row != 0):
                    # CUANDO EL NOMBRE DE LA ESTACIÓN ESTA AL FINAL
                    dato = old_worksheet.cell_value(1, 0)
                    if isinstance(dato, float) == True:
                        # Empezar desde el segundo elemento y no la fecha
                        columnas = old_worksheet.ncols
                        if(col != 0 and col != columnas-1):
                            new_worksheet.write(
                                row-1, col, old_worksheet.cell_value(row, col))
                        if (col == 0):
                            # Formato de fecha
                            raw_value = old_worksheet.cell_value(row, col)
                            converted_date = xlrd.xldate_as_tuple(
                                raw_value, old_workbook.datemode)
                            to_print_date = datetime.datetime(
                                *converted_date).strftime("%d/%m/%Y %H:%M")
                            new_worksheet.write(row-1, col, to_print_date)
                        # CUANDO EL NOMBRE DE LA ESTACIÓN ESTA AL INICIO
                    elif isinstance(dato, str) == True:
                        # Empezar desde el segundo elemento y no la fecha
                        if(col != 0 and col != 1):
                            new_worksheet.write(
                                row-1, col-1, old_worksheet.cell_value(row, col))
                            # Cambiar el formato de la fecha
                        if (col == 1):
                            # Formato de fecha
                            raw_value = old_worksheet.cell_value(row, col)
                            converted_date = xlrd.xldate_as_tuple(
                                raw_value, old_workbook.datemode)
                            to_print_date = datetime.datetime(
                                *converted_date).strftime("%d/%m/%Y %H:%M")
                            new_worksheet.write(row-1, col-1, to_print_date)

        new_workbook.close()


"""
Función months: Arregla el oden de ejecucion de los archivos por mes y 
separa cada dato por su mes correspondiente, los archivos generados se guardan 
en la carpeta de newFormat2.
"""
def months():
    #Entrar a la carpeta de todos los archivos
    archivos = os.listdir('.\\Resultados\\processFiles\\newFormat1')
    numDatos = len(archivos)

    for i in range(0,numDatos):

        A=[{'mes':'ene','total':0},{'mes':'feb','total':0},{'mes':'mar','total':0},{'mes':'abr','total':0},{'mes':'may','total':0},{'mes':'jun','total':0},{'mes':'jul','total':0},{'mes':'ago','total':0},{'mes':'sep','total':0},{'mes':'oct','total':0},{'mes':'nov','total':0},{'mes':'dic','total':0}]

        # Abrir un archivo
        old_path = f".\\Resultados\\processFiles\\newFormat1\\{archivos[i]}"
        old_workbook = xlrd.open_workbook(old_path)
        old_worksheet = old_workbook.sheet_by_index(0)

        for row in range (old_worksheet.nrows):
            to_print_date = old_worksheet.cell_value(row,0)

            # Ver de cada archivo la cantidas de dias de los meses registrados
            if(to_print_date.find('/01/')!=-1):
                A[0]['total']+=1
            elif(to_print_date.find('/02/')!=-1):
                A[1]['total']+=1
            elif(to_print_date.find('/03/')!=-1):
                A[2]['total']+=1
            elif(to_print_date.find('/04/')!=-1):
                A[3]['total']+=1
            elif(to_print_date.find('/05/')!=-1):
                A[4]['total']+=1
            elif(to_print_date.find('/06/')!=-1):
                A[5]['total']+=1
            elif(to_print_date.find('/07/')!=-1):
                A[6]['total']+=1
            elif(to_print_date.find('/08/')!=-1):
                A[7]['total']+=1
            elif(to_print_date.find('/09/')!=-1):
                A[8]['total']+=1
            elif(to_print_date.find('/10/')!=-1):
                A[9]['total']+=1
            elif(to_print_date.find('/11/')!=-1):
                A[10]['total']+=1
            elif(to_print_date.find('/12/')!=-1):
                A[11]['total']+=1
                
        #Sacar el mayor numero de registros del mes de cada archivo
        A.sort(key=lambda x:x['total'], reverse=True)

        #De la mayor cantidad de registros del mes en cada archivo, especificar el tipo de mes que pertenece el archivo
        if A[0]['mes'] == 'ene':
            nombreArchivo="01_Enero.xls"
        elif A[0]['mes'] == 'feb':
            nombreArchivo="02_Febrero.xls"
        elif A[0]['mes'] == 'mar':
            nombreArchivo="03_Marzo.xls"
        elif A[0]['mes'] == 'abr':
            nombreArchivo="04_Abril.xls"
        elif A[0]['mes'] == 'may':
            nombreArchivo="05_Mayo.xls"
        elif A[0]['mes'] == 'jun':
            nombreArchivo="06_Junio.xls"
        elif A[0]['mes'] == 'jul':
            nombreArchivo="07_Julio.xls"
        elif A[0]['mes'] == 'ago':
            nombreArchivo="08_Agosto.xls"
        elif A[0]['mes'] == 'sep':
            nombreArchivo="09_Septiembre.xls"
        elif A[0]['mes'] == 'oct':
            nombreArchivo="10_Octubre.xls"
        elif A[0]['mes'] == 'nov':
            nombreArchivo="11_Noviembre.xls"
        elif A[0]['mes'] == 'dic':
            nombreArchivo="12_Diciembre.xls"
                
        #Crea el nuevo archivo modificado
        new_path=f".\\Resultados\\processFiles\\newFormat2\\{nombreArchivo}"
        new_workbook = xlsxwriter.Workbook(new_path)
        new_worksheet = new_workbook.add_worksheet()

        #Determinar la fecha del mes de cada archivo 
        if nombreArchivo == "01_Enero.xls":
            mes = '/01/'
        elif nombreArchivo == "02_Febrero.xls":
            mes = '/02/'
        elif nombreArchivo == "03_Marzo.xls":
            mes = '/03/'
        elif nombreArchivo == "04_Abril.xls":
            mes = '/04/'
        elif nombreArchivo == "05_Mayo.xls":
            mes = '/05/'
        elif nombreArchivo == "06_Junio.xls":
            mes = '/06/'
        elif nombreArchivo == "07_Julio.xls":
            mes = '/07/'
        elif nombreArchivo == "08_Agosto.xls":
            mes = '/08/'
        elif nombreArchivo == "09_Septiembre.xls":
            mes = '/09/'
        elif nombreArchivo == "10_Octubre.xls":
            mes = '/10/'
        elif nombreArchivo == "11_Noviembre.xls":
            mes = '/11/'
        elif nombreArchivo == "12_Diciembre.xls":
            mes = '/12/'

        bandera = False 
        for row in range(old_worksheet.nrows):
            if old_worksheet.cell_value(row,0).find(mes)!=-1:
                if bandera == False:
                    cerorow = row
                    newrow =cerorow*0
                    bandera=True
                else:
                    newrow+=1
                for col in range(old_worksheet.ncols):
                    new_worksheet.write(newrow,col,old_worksheet.cell_value(row,col))


        new_workbook.close()

        
    #Por si faltan archivos de un mes especifico, se llenaran los faltantes
    A_elementos=["01_Enero.xls","02_Febrero.xls","03_Marzo.xls","04_Abril.xls","05_Mayo.xls","06_Junio.xls","07_Julio.xls","08_Agosto.xls","09_Septiembre.xls","10_Octubre.xls","11_Noviembre.xls","12_Diciembre.xls"]
    C_elementos=[]

    NoFaltantes = []

    B_elementos = os.listdir('.\\Resultados\\processFiles\\newFormat2')

    # Si faltan archivos
    if(len(B_elementos)!=12):
        
        #Copiar lista de archivos definidos
        for i in range(len(A_elementos)):
            C_elementos.append(A_elementos[i])

        #Encontrar los elementos no faltantes
        for i in range(len(A_elementos)):
            for j in range(len(B_elementos)):
                elemento = A_elementos.index(B_elementos[j])
                if(isinstance(elemento,int)):
                    try:
                        elemento2 = NoFaltantes.index(B_elementos[j])    
                    except:
                        NoFaltantes.append(B_elementos[j])
            
        #Encontrar los elementos que faltan 
        for i in range(len(C_elementos)):
            for j in range(len(NoFaltantes)):
                try:
                    elemento=C_elementos.index(NoFaltantes[j])
                except:
                    break

                if(isinstance(elemento,int)):
                    C_elementos.pop(elemento)

    #llenar los archivos faltantes
    archivos = os.listdir('.\\Resultados\\processFiles\\newFormat1')
    numDatos = len(archivos)

    for i in range(len(C_elementos)):
        new_path=f".\\Resultados\\processFiles\\newFormat2\\{C_elementos[i]}"
        new_workbook = xlsxwriter.Workbook(new_path)
        new_worksheet = new_workbook.add_worksheet()

        for j in range(0, numDatos):
            old_path = f".\\Resultados\\processFiles\\newFormat1\\{archivos[j]}"
            old_workbook = xlrd.open_workbook(old_path)
            old_worksheet = old_workbook.sheet_by_index(0)

            if C_elementos[i] == "01_Enero.xls":
                mes = '/01/'
            elif C_elementos[i] == "02_Febrero.xls":
                mes = '/02/'
            elif C_elementos[i] == "03_Marzo.xls":
                mes = '/03/'
            elif C_elementos[i] == "04_Abril.xls":
                mes = '/04/'
            elif C_elementos[i] == "05_Mayo.xls":
                mes = '/05/'
            elif C_elementos[i] == "06_Junio.xls":
                mes = '/06/'
            elif C_elementos[i] == "07_Julio.xls":
                mes = '/07/'
            elif C_elementos[i] == "08_Agosto.xls":
                mes = '/08/'
            elif C_elementos[i] == "09_Septiembre.xls":
                mes = '/09/'
            elif C_elementos[i] == "10_Octubre.xls":
                mes = '/10/'
            elif C_elementos[i] == "11_Noviembre.xls":
                mes = '/11/'
            elif C_elementos[i] == "12_Diciembre.xls":
                mes = '/12/'

            bandera = False 
            for row in range(old_worksheet.nrows):
                if old_worksheet.cell_value(row,0).find(mes)!=-1:
                    if bandera == False:
                        cerorow = row
                        newrow =cerorow*0
                        bandera=True
                    else:
                        newrow+=1
                    for col in range(old_worksheet.ncols):
                        new_worksheet.write(newrow,col,old_worksheet.cell_value(row,col))
                        
        new_workbook.close()


"""
Función oneFile: Junta todos los archivos  de la carpeta newFormat2 en un solo archivo de xls, 
con columnas establecidas para generar el archivo foo, pasando de coordenadas polares 
a cartecianas.
"""
def oneFile():
    archivos = os.listdir('.\\Resultados\\processFiles\\newFormat2')
    numArchivos = len(archivos)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\mainxls\\foo.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    dic=[]
    #Ciclo para guardar el nombre del archivo y el número de su ultimo registro
    for i in range(numArchivos):
        # Abrir un archivo
        current_path = f".\\Resultados\\processFiles\\newFormat2\\{archivos[i]}"
        current_workbook = xlrd.open_workbook(current_path)
        current_worksheet = current_workbook.sheet_by_index(0)
        dic.append({"NombreArchivo":archivos[i],"LastRow":current_worksheet.nrows})

    sumas=[]
    sumas.append(0)
    flag=False
    #Ciclo para ir sumando los registros que deberan tener los archivos al juntarlos
    for i in range(len(dic)):
        if flag==False:
            sumas.append(dic[i]["LastRow"])
            flag=True
        else:
            sumas.append(sumas[len(sumas)-1]+dic[i]["LastRow"])
                

    #Ciclo para juntar los archivos
    for i in range(numArchivos):
        Bandera1=False
        current_path = f".\\Resultados\\processFiles\\newFormat2\\{archivos[i]}"
        current_workbook = xlrd.open_workbook(current_path)
        current_worksheet = current_workbook.sheet_by_index(0)
        newrow=sumas[i]
        
        for row in range(current_worksheet.nrows):
            if Bandera1==True:
                newrow+=1
            else:
                Bandera1=True
        
            #Fecha
            new_worksheet.write(newrow, 0, current_worksheet.cell_value(row,0))

            #Dirección del viento y velocidad
            dirV = current_worksheet.cell_value(row, 1) ##dirV
            velV  = current_worksheet.cell_value(row, 3) ##velV 
            #Si no encuentra el valor poner NaN
            if type(dirV)==str or type(velV)==str:
                new_worksheet.write(newrow, 1, "NaN")
                new_worksheet.write(newrow, 2, "NaN")
            #Si encuentra el número, cambiar las coordenadas polares a cartecianas
            else:
                y=(float(velV)/3.6)*math.cos(math.radians(float(dirV)))
                x=(float(velV)/3.6)*math.sin(math.radians(float(dirV)))   
                #Escrbir en el archivo el resultado
                new_worksheet.write(newrow, 1, x)
                new_worksheet.write(newrow, 2, y)
            #Pasar la humedad relativa
            if type(current_worksheet.cell_value(row,6))==str:
                new_worksheet.write(newrow, 3, "NaN")
            else:
                new_worksheet.write(newrow, 3, current_worksheet.cell_value(row,6))
            #Pasar la presión Barometrica
            if type(current_worksheet.cell_value(row,7))==str:
                new_worksheet.write(newrow, 4, "NaN")
            else:
                new_worksheet.write(newrow, 4, current_worksheet.cell_value(row,7))
     
    new_workbook.close()


"""
Función NaN: Pone a toda un fila en NaN, si cualquier dato de la 
fila es NaN del archivo foo.py que se encuentra en la carpeta principal.
"""
def NaN():
    # Abrir un archivo
    old_path = f".\\Resultados\\processFiles\\mainxls\\foo.xls"
    old_workbook = xlrd.open_workbook(old_path)
    old_worksheet = old_workbook.sheet_by_index(0)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    for row in range(old_worksheet.nrows):
        for col in range(old_worksheet.ncols):
            if old_worksheet.cell_value(row,col)=="NaN":
                new_worksheet.write(row,1,"NaN")
                new_worksheet.write(row,2,"NaN")
                new_worksheet.write(row,3,"NaN")
                new_worksheet.write(row,4,"NaN")
            else:
                new_worksheet.write(row,col,old_worksheet.cell_value(row,col))
            

    new_workbook.close()


"""
Función gmm: Utiliza el algoritmo denominado gaussian mixture model
para poder mostrar las graficas que representan los estados de los vientos.
"""
def gmm(nameEstacion, year, numClusters):
    # Abrir un archivo
    main_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    main_workbook = xlrd.open_workbook(main_path)
    main_worksheet = main_workbook.sheet_by_index(0)

    dirViento=[]
    velViento=[]
    humRelativa=[]
    preBarometrica=[]
    for row in range(main_worksheet.nrows):

        if main_worksheet.cell_value(row,1)!="NaN": 
            dirViento.append(main_worksheet.cell_value(row,1))

        if main_worksheet.cell_value(row,2)!="NaN":
            velViento.append(main_worksheet.cell_value(row,2))

        if main_worksheet.cell_value(row,3)!="NaN":
            humRelativa.append(main_worksheet.cell_value(row,3))

        if main_worksheet.cell_value(row,4)!="NaN":
            preBarometrica.append(main_worksheet.cell_value(row,4))

    x=np.array(dirViento,dtype='double')
    y=np.array(velViento,dtype='double')
    z=np.array(humRelativa,dtype='double')
    w=np.array(preBarometrica,dtype='double')

    xmin=x.min()
    xmax=x.max()
    ymin=y.min()
    ymax=y.max()
    zmin=z.min()
    zmax=z.max()
    wmin=w.min()
    wmax=w.max()

    x1=(x-x.mean())/(xmax-xmin)
    y1=(y-y.mean())/(ymax-ymin)
    z1=(z-z.mean())/(zmax-zmin)
    w1=(w-w.mean())/(wmax-wmin)
    
    samples = np.array([(x1[i],y1[i],z1[i],w1[i]) for i in range(len(x))])
    name= f"./Resultados/{nameEstacion} {year}.png"

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\clusters\\clusters_rum_12.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    gmix = mixture.GaussianMixture(n_components=numClusters, covariance_type='full', max_iter=500,random_state=50)
    gmix.fit(samples)
    ax = plt.gca()
    ax.set(xlabel="m/s",
       ylabel="m/s",
       title= f"{nameEstacion} {year}");

    ax.set_xlim([-.8,.8])
    ax.set_ylim([-.8,.8])
    ax.grid(True)      
    grp = gmix.predict(samples)
    tam=len(samples)
    cad=[]
    for i in range(tam):
        cad.append(0)
        
    idx =(grp==5)
    ax.scatter(samples[idx,0], samples[idx,1], c='#e2f413', alpha=0.1) #amarillo
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=6
            
    idx =(grp==4)    
    ax.scatter(samples[idx,0], samples[idx,1], c='#1a9918', alpha=0.1)#verde
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=5       
    
    idx =(grp==3)    
    ax.scatter(samples[idx,0], samples[idx,1], c='#f4a4c1', alpha=0.1)#rosa
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=4       
       
    idx =(grp==2)
    ax.scatter(samples[idx,0], samples[idx,1], c='r', alpha=0.1)#rojo
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=3       
    

    idx =(grp==1)
    ax.scatter(samples[idx,0], samples[idx,1], c='#1e90ff', alpha=0.1)#azul
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=2     

    idx =(grp==0)
    ax.scatter(samples[idx,0], samples[idx,1], c='#3d11a3', alpha=0.1)#morado
    for i in range(len(idx)):
        if str(idx[i])=='True':
            cad[i]=1

    for i in range(len(cad)):
        new_worksheet.write(i,0,str(cad[i]));

    new_workbook.close()

    plt.savefig(name,dpi = 300, format="png")

    # plt.show()
    plt.clf()
    plt.close()


"""
Función gmmOne: Genera una grafica por cluster.
"""
def gmmOne(nameEstacion, year, numClusters):

    colors=['#3d11a3','#1e90ff','r','#f4a4c1','#1a9918','#e2f413']
    for cluster in range(0, numClusters):
    
        # Abrir un archivo
        main_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
        main_workbook = xlrd.open_workbook(main_path)
        main_worksheet = main_workbook.sheet_by_index(0)

        dirViento=[]
        velViento=[]
        humRelativa=[]
        preBarometrica=[]
        for row in range(main_worksheet.nrows):

            if main_worksheet.cell_value(row,1)!="NaN": 
                dirViento.append(main_worksheet.cell_value(row,1))

            if main_worksheet.cell_value(row,2)!="NaN":
                velViento.append(main_worksheet.cell_value(row,2))

            if main_worksheet.cell_value(row,3)!="NaN":
                humRelativa.append(main_worksheet.cell_value(row,3))

            if main_worksheet.cell_value(row,4)!="NaN":
                preBarometrica.append(main_worksheet.cell_value(row,4))

        x=np.array(dirViento,dtype='double')
        y=np.array(velViento,dtype='double')
        z=np.array(humRelativa,dtype='double')
        w=np.array(preBarometrica,dtype='double')

        xmin=x.min()
        xmax=x.max()
        ymin=y.min()
        ymax=y.max()
        zmin=z.min()
        zmax=z.max()
        wmin=w.min()
        wmax=w.max()

        x1=(x-x.mean())/(xmax-xmin)
        y1=(y-y.mean())/(ymax-ymin)
        z1=(z-z.mean())/(zmax-zmin)
        w1=(w-w.mean())/(wmax-wmin)

        samples = np.array([(x1[i],y1[i],z1[i],w1[i]) for i in range(len(x))])
        name= f"./Resultados/Cluster {cluster+1} {nameEstacion} {year}.png"
        gmix = mixture.GaussianMixture(n_components=numClusters, covariance_type='full', max_iter=500,random_state=50)
        gmix.fit(samples)

        ax = plt.gca()

        ax.set(xlabel="m/s",
            ylabel="m/s",
            title= f"{nameEstacion} {year}");

        ax.set_xlim([-.8,.8])
        ax.set_ylim([-.8,.8])
        ax.grid(True)      
        grp = gmix.predict(samples) 

        idx =(grp==cluster)
        ax.scatter(samples[idx,0], samples[idx,1], c=colors[cluster], alpha=0.1)
       
        plt.savefig(name,dpi = 300, format="png")

        # plt.show()
        plt.clf()
        plt.close()


"""
Función ibxTrue: Coloca el indice actual de cada registro en un archivo diferente.
"""
def ibxTrue():
    # Abrir un archivo
    old_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    old_workbook = xlrd.open_workbook(old_path)
    old_worksheet = old_workbook.sheet_by_index(0)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\idxTrue\\idxTrue.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    for row in range(old_worksheet.nrows):
        new_worksheet.write(row,0,str(row+1))

    new_workbook.close()


"""
Función idxTrue_clusters: Junta el indice y el tipo de cluster en un archivo aparte.0
"""
def idxTrue_clusters():

    # Abrir un archivo de indices
    old_path1 = f".\\Resultados\\processFiles\\idxTrue\\idxTrue.xls"
    old_workbook1 = xlrd.open_workbook(old_path1)
    old_worksheet1 = old_workbook1.sheet_by_index(0)


    # Abrir un archivo de grupos
    old_path2 = f".\\Resultados\\processFiles\\clusters\\clusters_rum_12.xls"
    old_workbook2 = xlrd.open_workbook(old_path2)
    old_worksheet2 = old_workbook2.sheet_by_index(0)

    # Abrir el archivo principal
    old_path3 = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    old_workbook3 = xlrd.open_workbook(old_path3)
    old_worksheet3 = old_workbook3.sheet_by_index(0)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\idxTrue_clusters\\idxTrue_clusters.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    # Coloca el número de registro
    for row in range(old_worksheet1.nrows):
        new_worksheet.write(row,0,old_worksheet1.cell_value(row,0))

    # Sacar clusters
    cluster=list()
    for row in range(old_worksheet2.nrows):
        cluster.append(old_worksheet2.cell_value(row,0))

    # Sacar filas NaN
    rowNaN=list()
    f=0
    for row in range(old_worksheet3.nrows):
    
        pres = old_worksheet3.cell_value(row,1)            
        temp = old_worksheet3.cell_value(row,2)
        velV = old_worksheet3.cell_value(row,3)
        dirV = old_worksheet3.cell_value(row,4)
    
        if (pres and temp and velV and dirV)=="NaN":
            rowNaN.append(0)
        else:
            try:
                rowNaN.append(cluster[f])
                f+=1
            except:
                rowNaN.append(0)


    for row in range(old_worksheet3.nrows):
        new_worksheet.write(row,1,rowNaN[row])

    new_workbook.close()


"""
Función std: Lee la columna 2 que pertenece a la clasificación del archivo idxTrue_clusters.xls, 
para después generar 6 columnas binarias dependiendo del tipo de clasificación.
"""
def std():
     # Abrir archivo
     path=f".\\Resultados\\processFiles\\idxTrue_clusters\\idxTrue_clusters.xls"
     workbook = xlrd.open_workbook(path)
     worksheet = workbook.sheet_by_index(0)

     #Crear archivo F2
     new_path = f".\\Resultados\\processFiles\\stdProd\\F2.xls"
     new_workbook = xlsxwriter.Workbook(new_path)
     new_worksheet = new_workbook.add_worksheet()

     for row in range(worksheet.nrows):
 
          if worksheet.cell_value(row,1)=='1':
               new_worksheet.write(row,0,'1')
          else:
               new_worksheet.write(row,0,'0')

          if worksheet.cell_value(row,1)=='2':
               new_worksheet.write(row,1,'1')
          else:
               new_worksheet.write(row,1,'0')

          if worksheet.cell_value(row,1)=='3':
               new_worksheet.write(row,2,'1')
          else:
               new_worksheet.write(row,2,'0')

          if worksheet.cell_value(row,1)=='4':
               new_worksheet.write(row,3,'1')  
          else: 
               new_worksheet.write(row,3,'0')

          if worksheet.cell_value(row,1)=='5':
               new_worksheet.write(row,4,'1') 
          else:
               new_worksheet.write(row,4,'0')

          if worksheet.cell_value(row,1)=='6':
               new_worksheet.write(row,5,'1')
          else:
               new_worksheet.write(row,5,'0')

     new_workbook.close()

        
"""
Función inputAc: Prepara un archivo de entrada, juntando la fecha y hora de cada registro como tambien juntar 
las 6 columnas binarias dependiendo del tipo de clasificación del programa std_prod.
"""
def inputAc(numClusters):
    # Abrir el archivo mainxls
    main_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    main_workbook = xlrd.open_workbook(main_path)
    main_worksheet = main_workbook.sheet_by_index(0)

    #Abrir el archivo std
    std_path = f".\\Resultados\\processFiles\\\\stdProd\\F2.xls"
    std_workbook = xlrd.open_workbook(std_path)
    std_worksheet = std_workbook.sheet_by_index(0)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\processFiles\\acInput\\ac_input.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()

    new_worksheet.write(0,0,"Date")
    new_worksheet.write(0,1,"Time")

    #Encabezados
    for i in range(0,numClusters):
        new_worksheet.write(0,i+2,f"Cluster{i+1}")
        
    #Fechas
    for row in range(main_worksheet.nrows):
        fecha_completa = main_worksheet.cell_value(row,0)
        new_worksheet.write(row+1,0,fecha_completa[0:10])
        new_worksheet.write(row+1,1,fecha_completa[11:16])

    #Clasificaciones
    for row in range(std_worksheet.nrows):
        for col in range(numClusters):
            new_worksheet.write(row+1,col+2,std_worksheet.cell_value(row,col))

    new_workbook.close()


"""
Función histogram: Convierte el archivo xls generado por input_ac.py a archivo csv, 
para despues generar el histograma final.
"""
def histogram(nameEstacion, year, numClusters):
       # Leer el archivo xls
       read_file = pd.read_excel ("./Resultados/processFiles/acInput/ac_input.xls")

       # Transformar a csv
       read_file.to_csv ("./Resultados/processFiles/acInput/ac_input.csv",
                                   index = None,
                                   header=True)

       #Leer el csv para generar el histograma
       data_ac=pd.read_csv('./Resultados/processFiles/acInput/ac_input.csv', encoding='latin1', parse_dates=[['Date','Time']], dayfirst=True)
       # print(data_ac)

       semanas={}

       for i in range(1, numClusters+1):
              hora= data_ac.set_index('Date_Time').groupby(pd.Grouper(freq='H'))[f'Cluster{i}'].mean()
              dia = hora.groupby(pd.Grouper(freq='D')).mean()
              semana = dia.groupby(pd.Grouper(freq='W')).mean()
              mesC1 = semana.groupby(pd.Grouper(freq='M')).mean()
              semanas[f"Cluster{i}"] = semana

       #GRAFICAS
       semana=pd.DataFrame(semanas)
       ax = plt.subplots() 
       ax=semana.plot.bar(width=0.9)
       ax.set(xlabel="",
              ylabel="Mean",
              title= f"{nameEstacion} {year}");

       ax.set_ylim([0,1])
       ticklabels = ['']*len(semanas["Cluster1"].index)
       ticklabels[::4] = [item.strftime('%b %d') for item in semanas["Cluster1"].index[::4]]
       ticklabels[::52] = [item.strftime('%b %d\n%Y') for item in semanas["Cluster1"].index[::52]]
       ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
       plt.gcf()
       plt.xticks(fontsize = 7)
       plt.yticks(fontsize = 7)
       plt.savefig(f"./Resultados/Promedio semanal de {nameEstacion} {year}.png",dpi=300,format="png") 

       # plt.show()
       plt.clf()
       plt.close()


"""
Función results: Genera el archivo zip.
"""
def results(nameEstation,year):
    # Colocar encabezados al archivo main
    # Abrir un archivo
    old_path = f".\\Resultados\\processFiles\\mainxls\\finalMain.xls"
    old_workbook = xlrd.open_workbook(old_path)
    old_worksheet = old_workbook.sheet_by_index(0)

    # Crea el nuevo archivo modificado
    new_path = f".\\Resultados\\gmm.xls"
    new_workbook = xlsxwriter.Workbook(new_path)
    new_worksheet = new_workbook.add_worksheet()


    for row in range(old_worksheet.nrows):
        for col in range(old_worksheet.ncols):
            if row==0 and col==0:
                new_worksheet.write(0,0,"Date")
                new_worksheet.write(0,1,"x")
                new_worksheet.write(0,2,"y")
                new_worksheet.write(0,3,"HumRelativa")
                new_worksheet.write(0,4,"PresBarometric")

            new_worksheet.write(row+1, col, old_worksheet.cell_value(row, col))


    new_workbook.close()

    # Realizar una copia del archivo ac_input.xls
    main = '.\\Resultados\\processFiles\\acInput\\ac_input.xls'
    destiny = '.\\Resultados\\histogram.xls'
    shutil.copyfile(main, destiny)

    # Crear el archivo zip
    fantasy_zip = zipfile.ZipFile(f'.\\Resultados\\{nameEstation} {year}.zip', 'w')
    files=os.listdir('.\\Resultados')
    for i in range(len(os.listdir('.\\Resultados'))):
        files[i]=f'.\\Resultados\\'+files[i]
        if files[i].endswith('.png') or files[i].endswith('.xls'):
            fantasy_zip.write(os.path.join(files[i]), os.path.relpath(os.path.join(files[i]), '.\\Resultados'), compress_type = zipfile.ZIP_DEFLATED)
    
    fantasy_zip.close()

"""
Función interface: Define la interfaz para el usuario.
"""
def interface():
    
    print("""
        Bienvenido:

        - Instrucciones(1)
        - Iniciar(2)
        - Salir(3)""")

    bandera=False
    if bandera==False:
        try:
            start=input(":: ")
        except:
            start=False

        bandera=True

    while bandera==True:
        if start==False:
            start=input(":: ")

        if start == '1' or '2' or '3':
            if len(os.listdir('./Archivos'))>=1 and start=='2':
                aviso={'False':'Por favor coloque los archivos con extencion xls.'}
                banderaAviso='True'
                ArchivoEntrada=os.listdir('./Archivos')
                for i in range(len(os.listdir('./Archivos'))):
                    if not ArchivoEntrada[i].endswith('xls'):
                        banderaAviso='False'

                if banderaAviso== 'False':
                    print(f"""
                {aviso[banderaAviso]}""")
                else:
                    try:
                        numClusters = int(input("""
                Coloque el numero de clusters: """))
                        if numClusters<=10 and numClusters>=1:
                            print("""
                Proceso iniciado por favor espere, no cierre esta ventana.""")
                            return numClusters
                        else:
                            print("""
                Solo se permite un rango entre 1 y 10, vuelva a seleccionar una opción del menu.""")
                    except:
                        print("""
                Solo se permiten números enteros, vuelva a seleccionar una opción del menu. """)
                        
            if len(os.listdir('./Archivos'))==0 and start=='2':
                print("""
                La carpeta de archivos está vacía, por favor coloque los archivos a analizar 
                y vuelva a seleccionar una opción del menu.""")

            if start=="1":
                print("""
                Por favor coloque los archivos que desea analizar en la carpeta "Archivos", 
                para después colocar 1 para iniciar con el proceso, al terminar el proceso 
                los resultados estarán en la carpeta "Resultados".""")

            if start=='3':
                sys.exit()

        if start != '1' or '2' or '3':
            start=False


"""
Función main: Función que contiene el orden de ejecución.
"""
def main():
    mainFiles()
    clearResults()
    clearDataProcess()
    interfaceValues=interface()
    createFiles()
    dataError=False
    try:
        data=info(interfaceValues)  # data = {NameStacion, year, numClusters}
        formats()
        months()
        oneFile()
        NaN()
        gmm(data[0],data[1],data[2])
        gmmOne(data[0],data[1],data[2])
        ibxTrue()
        idxTrue_clusters()
        std()
        inputAc(data[2])
        histogram(data[0],data[1],data[2])
        results(data[0],data[1])
    except:
        print("""
                El formato de los archivos es incorrecto, revise el formato adecuado. """)
        dataError=True

    clearDataProcess()

    if dataError==False:
        print("""
                Proceso finalizado, los resultados se encuentran en la carpeta "Resultados". """)
        salir=input("""
        - Salir(3):: """)
    
        while salir!='3':
            salir=input("""
        - Salir(3):: """)

        if salir=='3':
            sys.exit()

    if dataError==True:
        salir=input("""
        - Salir(3):: """)

        while salir!='3':
            salir=input("""
        - Salir(3):: """)
        

    # Elimina carpeta con archivos cache
    # rmtree("./__pycache__")
    #Elimina carpeta vacia
    # rmdir("./__pycache__")

# Iniciar funcion principal
if __name__ =='__main__':
    main()