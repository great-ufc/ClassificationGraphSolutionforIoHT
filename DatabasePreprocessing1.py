from __future__ import absolute_import, division, print_function, unicode_literals

import math
import statistics as st
import numpy as np
import pandas as pd
import scipy
from six.moves import urllib
from scipy import stats ##statistic functions
import platform
"""###Import Dataset"""

import glob
import os
from os import listdir
from os.path import isfile, join

MyNewDataSetTest = None
labelTest = None
MyNewDataSetTrain = None
labelTrain = None
MyNewDataSetTest2 = None
labelTest2 = None
MyNewDataSetTrain2 = None
labelTrain2 = None
class_names = None
MyNewDataSetTest_ = None
MyNewDataSetTrain_ = None

def convertlabelInt(arr):
  lvalue = np.array(-1)
  
  for value in arr:
    if(value[0] == "ANDA" or value[0] == "ANDAR"):
      lvalue = np.append(lvalue,0)
    if(value[0] == "BATER_NA_MES" or value[0] == "BATER_NA_MESA"):
      lvalue = np.append(lvalue,1)
    if(value[0] == "BATER_PARED" or value[0] == "BATER_PAREDE"):
      lvalue = np.append(lvalue,2)
    if(value[0] == "CORREND" or value[0] == "CORRENDO"):
      lvalue = np.append(lvalue,3)
    if(value[0] == "DEITA" or value[0] == "DEITAR"):
      lvalue = np.append(lvalue,4)
    if(value[0] == "ESBARRAR_PARED" or value[0] == "ESBARRAR_PAREDE"):
      lvalue = np.append(lvalue,5)
    if(value[0] == "ESCREVE" or value[0] == "ESCREVER"):
      lvalue = np.append(lvalue,6)
    if(value[0] == "PALMAS_EMP" or value[0] == "PALMAS_EMPE"):
      lvalue = np.append(lvalue,7)
    if(value[0] == "PALMAS_SE" or value[0] == "PALMAS_SEN"):
      lvalue = np.append(lvalue,8)
    if(value[0] == "PUL" or value[0] == "PULO"):
      lvalue = np.append(lvalue,9)
    if(value[0] == "QUEDA_APOIO_FRENT" or value[0] == "QUEDA_APOIO_FRENTE"):
      lvalue = np.append(lvalue,10)
    if(value[0] == "QUEDA_LATERAL" or value[0] == "QUEDA_LATERAL_" or value[0] == "QUEDA_LATERAL_B"):
      lvalue = np.append(lvalue,11)
    if(value[0] == "QUEDA_SAPOIO_FRENT" or value[0] == "QUEDA_SAPOIO_FRENTE"):
      lvalue = np.append(lvalue,12)
    if(value[0] == "SENTA" or value[0] == "SENTAR"):
      lvalue = np.append(lvalue,13)
    if(value[0] == "SENTAR_APOIO"):
      lvalue = np.append(lvalue,14)
    if(value[0] == "SENTAR_SAPOIO"):
      lvalue = np.append(lvalue,15)
    if(value[0] == "TATEA" or value[0] == "TATEAR"):
      lvalue = np.append(lvalue,16)
  lvalue = np.delete(lvalue, (0), axis=0)
  return lvalue

def executePreproccessing():
    global MyNewDataSetTest, labelTest, MyNewDataSetTrain, labelTrain, MyNewDataSetTest2, labelTest2, MyNewDataSetTrain2, labelTrain2, class_names
    pathDataset = "Datasets/Dataset1"

    #from google.colab import drive
    #drive.mount('/content/drive')

    #from pydrive.auth import GoogleAuth
    #from pydrive.drive import GoogleDrive
    #from google.colab import auth
    #from oauth2client.client import GoogleCredentials

    #auth.authenticate_user()
    #gauth = GoogleAuth()
    #gauth.credentials = GoogleCredentials.get_application_default()
    #drive = GoogleDrive(gauth)

    """**Preprocessing**

    (*Prepara matrizes de stream para acc e gyr*)
    """



    so = platform.system()


    file_list = [] #drive.ListFile({'q': "'1b0td7j4thzGViqUa_zpOz3GGnPEJsihL' in parents"}).GetList() ##Lista de arquivos no meu Dataset
    for file in glob.glob(pathDataset+"/*"):
        if so == "Windows":
            file_list.append(file.split("\\")[1])
        if so == "Linux":
            file_list.append(file.split("/")[2])
        


    path = os.path.expanduser(pathDataset) ##Localização do Dataset

    ##MyDataSet Labels
    MyNewDataSet = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", ("IQR ACC"),
                    "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", ("IQR GYR"),
                    "Movement"]])
    
    MyNewDataSet2 = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", ("IQR ACC"),"Movement"]])
    
    #retona rms
    def calc_rms(x,y,z):
       return math.sqrt(x*x+y*y+z*z)

    def feature_extraction_acc_gyr (arr):
      arr_acc_rms = np.array([[0.0, "", ""]])
      arr_gyr_rms = np.array([[0.0, "", ""]])
      #Gera vertor de valores unificados para os dados de ACC e Gyr
      infoName = arr[0,4]
      for line in arr:
        if(line[3] == "ACC"):
          arr_acc_rms = np.vstack([arr_acc_rms,[calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
        if(line[3] == "GYR"):
          arr_gyr_rms = np.vstack([arr_gyr_rms,[calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
      arr_acc_rms = np.delete(arr_acc_rms, (0), axis=0) #deleta primeira linha vazia
      arr_gyr_rms = np.delete(arr_gyr_rms, (0), axis=0)

      #Vector base for feature extractions
      vector_value_acc = [float(i) for i in [x[0] for x in arr_acc_rms]] #retorna primeira coluna da matriz de ACC
      vector_value_gyr = [float(i) for i in [x[0] for x in arr_gyr_rms]] #retorna primeira coluna da matriz de GYR

      #####Maybe Improve####
      ##linear acceleration (pitch, roll, yaw)
      ##angular velocity 
      ##Auto Regression coefficient
      ##correlation
      ##FFT
      ##Mean frequency

      '''result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), stats.median_absolute_deviation(vector_value_acc), stats.iqr(vector_value_acc),
                st.mean(vector_value_gyr), max(vector_value_gyr), min(vector_value_gyr), st.stdev(vector_value_gyr), stats.kurtosis(vector_value_gyr),
                stats.skew(vector_value_gyr), stats.entropy(vector_value_gyr), stats.median_absolute_deviation(vector_value_gyr), stats.iqr(vector_value_gyr),
                infoName]
      '''          
      result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), 0, stats.iqr(vector_value_acc),
                st.mean(vector_value_gyr), max(vector_value_gyr), min(vector_value_gyr), st.stdev(vector_value_gyr), stats.kurtosis(vector_value_gyr),
                stats.skew(vector_value_gyr), stats.entropy(vector_value_gyr), 0, stats.iqr(vector_value_gyr),
                infoName]
               
                            
      
      return result  

    def feature_extraction_acc (arr):
      arr_acc_rms = np.array([[0.0, "", ""]])
      #Gera vertor de valores unificados para os dados de ACC e Gyr
      infoName = arr[0,4]
      for line in arr:
        if(line[3] == "ACC"):
          arr_acc_rms = np.vstack([arr_acc_rms,[calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
      arr_acc_rms = np.delete(arr_acc_rms, (0), axis=0) #deleta primeira linha vazia

      #Vector base for feature extractions
      vector_value_acc = [float(i) for i in [x[0] for x in arr_acc_rms]] #retorna primeira coluna da matriz de ACC

      #####Maybe Improve####
      ##linear acceleration (pitch, roll, yaw)
      ##angular velocity 
      ##Auto Regression coefficient
      ##correlation
      ##FFT
      ##Mean frequency

      '''result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), stats.median_absolute_deviation(vector_value_acc), stats.iqr(vector_value_acc),
                st.mean(vector_value_gyr), max(vector_value_gyr), min(vector_value_gyr), st.stdev(vector_value_gyr), stats.kurtosis(vector_value_gyr),
                stats.skew(vector_value_gyr), stats.entropy(vector_value_gyr), stats.median_absolute_deviation(vector_value_gyr), stats.iqr(vector_value_gyr),
                infoName]
      '''          
      result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), 0, stats.iqr(vector_value_acc),
                infoName]
               
                            
      
      return result
    
    ##Adiciona os streams no dataset. Uma linha para cada arquivo 
    for file in file_list: ##ler arquivos na pasta
      arr = np.array([[0.0, 0.0, 0.0, "", ""]])
      movement = str(file).split(".")[0][0:len(str(file)[0])-3]
      movement = movement[6:len(movement)]
      fname = os.path.join(path, file)
      with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines: ##ler linhas do arquivo
          #print(len(line.split(':')))
          if(len(line.split(':')) < 2):
            if(int(line.split(',')[4]) == 1):
              sensor = "ACC"
            if(int(line.split(',')[4]) == 4):
              sensor = "GYR"
            row = [float(line.split(',')[1]),float(line.split(',')[2]), float(line.split(',')[3]), sensor, movement]
            arr = np.vstack([arr,row])
      arr = np.delete(arr, (0), axis=0) #deleta primeira linha vazia
      MyNewDataSet = np.vstack([MyNewDataSet, feature_extraction_acc_gyr(arr)])
      MyNewDataSet2 = np.vstack([MyNewDataSet2, feature_extraction_acc(arr)])
      
      #print(fname)
      ##print(arr.shape)
      ##print(arr[10])
      #break

    #print(MyNewDataSet)
    print(MyNewDataSet2)

    MyNewDataSetTrain = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC",
                    "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR"]])
    labelTrain = np.array(["Movement"])
    MyNewDataSetTest = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC",
                    "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR"]])
    labelTest = np.array(["Movement"])
    
    MyNewDataSetTrain2 = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
    labelTrain2 = np.array(["Movement"])
    MyNewDataSetTest2 = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
    labelTest2 = np.array(["Movement"])
    
    

    numberTests = len(MyNewDataSet)*10//100
    numberTests2 = len(MyNewDataSet2)*10//100

    def choicelinesForTest(numberOfLines, numberChoices):
        import random
        lines = []
        for i in range(numberChoices):
            lines.append(random.randint(1,numberOfLines))        
        return lines

    linesForTest = choicelinesForTest(len(MyNewDataSet), numberTests)
    linesForTest2 = choicelinesForTest(len(MyNewDataSet2), numberTests2)
    
    count = 0
    for line in MyNewDataSet:
        if(count > 0):
            if(count in linesForTest):
              labelTest = np.vstack([labelTest, line[18]])
              line = np.delete(line, 18, 0)
              MyNewDataSetTest = np.vstack([MyNewDataSetTest, line])
            else:
              labelTrain = np.vstack([labelTrain, line[18]])
              line = np.delete(line, 18, 0)
              MyNewDataSetTrain = np.vstack([MyNewDataSetTrain, line])  
        count=count+1
    MyNewDataSetTrain = np.delete(MyNewDataSetTrain, (0), axis=0)
    MyNewDataSetTrain = MyNewDataSetTrain.astype(np.float)
    MyNewDataSetTest = np.delete(MyNewDataSetTest, (0), axis=0)
    MyNewDataSetTest = MyNewDataSetTest.astype(np.float)
    labelTrain = np.delete(labelTrain, (0), axis=0)
    labelTest = np.delete(labelTest, (0), axis=0) #precisa melhorar balancemento

    count = 0
    for line in MyNewDataSet2:
        if(count > 0):
            if(count in linesForTest2):
              labelTest2 = np.vstack([labelTest2, line[9]])
              line = np.delete(line, 9, 0)
              MyNewDataSetTest2 = np.vstack([MyNewDataSetTest2, line])
            else:
              labelTrain2 = np.vstack([labelTrain2, line[9]])
              line = np.delete(line, 9, 0)
              MyNewDataSetTrain2 = np.vstack([MyNewDataSetTrain2, line])  
        count=count+1
    print(MyNewDataSetTrain2)
    MyNewDataSetTrain2 = np.delete(MyNewDataSetTrain2, (0), axis=0)
    MyNewDataSetTrain2 = MyNewDataSetTrain2.astype(np.float)
    MyNewDataSetTest2 = np.delete(MyNewDataSetTest2, (0), axis=0)
    MyNewDataSetTest2 = MyNewDataSetTest2.astype(np.float)
    labelTrain2 = np.delete(labelTrain2, (0), axis=0)
    labelTest2 = np.delete(labelTest2, (0), axis=0) #precisa melhorar balancemento

    print(MyNewDataSet.shape)
    print(MyNewDataSetTrain.shape)
    print(MyNewDataSetTest.shape)
    print(np.unique(labelTrain))
    print("====DatasetACCOnly====")
    print(MyNewDataSet2.shape)
    print(MyNewDataSetTrain2.shape)
    print(MyNewDataSetTest2.shape)
    print(np.unique(labelTrain2))



    labelTrain = convertlabelInt(labelTrain)
    labelTest = convertlabelInt(labelTest)
    
    labelTrain2 = convertlabelInt(labelTrain2)
    labelTest2 = convertlabelInt(labelTest2)

    print(labelTest)
    print(labelTest2)

    ##Prepara as classes 
    class_names = ['Andar', 'BATER_NA_MESA', 'BATER_PAREDE', 'CORRENDO', 'DEITAR', 'ESBARRAR_PAREDE', 'ESCREVER', 'PALMAS_EMP', 'PALMAS_SEN', 'PULO','QUEDA_APOIO_FRENTE', 'QUEDA_LATERAL', 'QUEDA_SAPOIO_FRENTE', 'SENTAR', 'SENTAR_APOIO', 'SENTAR_SAPOIO', 'TATEAR' ]

    MyNewDataSetTrain_ = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC",
                    "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR", "Movement"]])
    MyNewDataSetTest_ = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC",
                    "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR", "Movement"]])

    count = 0
    for line in MyNewDataSet:
      if(count > 0):
        if(count % 20 == 0):
          MyNewDataSetTest_ = np.vstack([MyNewDataSetTest_, line])
        else:
          MyNewDataSetTrain_ = np.vstack([MyNewDataSetTrain_, line])  
      count=count+1

    for value in MyNewDataSetTest_:
        if(value[18] == "ANDA" or value[18] == "ANDAR"):
          value[18] = 0
        if(value[18] == "BATER_NA_MES" or value[18] == "BATER_NA_MESA"):
          value[18] = 1
        if(value[18] == "BATER_PARED" or value[18] == "BATER_PAREDE"):
          value[18] = 2
        if(value[18] == "CORREND" or value[18] == "CORRENDO"):
          value[18] = 3
        if(value[18] == "DEITA" or value[18] == "DEITAR"):
          value[18] = 4
        if(value[18] == "ESBARRAR_PARED" or value[18] == "ESBARRAR_PAREDE"):
          value[18] = 5
        if(value[18] == "ESCREVE" or value[18] == "ESCREVER"):
          value[18] = 6
        if(value[18] == "PALMAS_EMP" or value[18] == "PALMAS_EMPE"):
          value[18] = 7
        if(value[18] == "PALMAS_SE" or value[18] == "PALMAS_SEN"):
          value[18] = 8
        if(value[18] == "PUL" or value[18] == "PULO"):
          value[18] = 9
        if(value[18] == "QUEDA_APOIO_FRENT" or value[18] == "QUEDA_APOIO_FRENTE"):
          value[18] = 10
        if(value[18] == "QUEDA_LATERAL" or value[18] == "QUEDA_LATERAL_" or value[18] == "QUEDA_LATERAL_B"):
          value[18] = 11
        if(value[18] == "QUEDA_SAPOIO_FRENT" or value[18] == "QUEDA_SAPOIO_FRENTE"):
          value[18] = 12
        if(value[18] == "SENTA" or value[18] == "SENTAR"):
          value[18] = 13
        if(value[18] == "SENTAR_APOIO"):
          value[18] = 14
        if(value[18] == "SENTAR_SAPOIO"):
          value[18] = 15
        if(value[18] == "TATEA" or value[18] == "TATEAR"):
          value[18] = 16

    for value in MyNewDataSetTrain_:
        if(value[18] == "ANDA" or value[18] == "ANDAR"):
          value[18] = 0
        if(value[18] == "BATER_NA_MES" or value[18] == "BATER_NA_MESA"):
          value[18] = 1
        if(value[18] == "BATER_PARED" or value[18] == "BATER_PAREDE"):
          value[18] = 2
        if(value[18] == "CORREND" or value[18] == "CORRENDO"):
          value[18] = 3
        if(value[18] == "DEITA" or value[18] == "DEITAR"):
          value[18] = 4
        if(value[18] == "ESBARRAR_PARED" or value[18] == "ESBARRAR_PAREDE"):
          value[18] = 5
        if(value[18] == "ESCREVE" or value[18] == "ESCREVER"):
          value[18] = 6
        if(value[18] == "PALMAS_EMP" or value[18] == "PALMAS_EMPE"):
          value[18] = 7
        if(value[18] == "PALMAS_SE" or value[18] == "PALMAS_SEN"):
          value[18] = 8
        if(value[18] == "PUL" or value[18] == "PULO"):
          value[18] = 9
        if(value[18] == "QUEDA_APOIO_FRENT" or value[18] == "QUEDA_APOIO_FRENTE"):
          value[18] = 10
        if(value[18] == "QUEDA_LATERAL" or value[18] == "QUEDA_LATERAL_" or value[18] == "QUEDA_LATERAL_B"):
          value[18] = 11
        if(value[18] == "QUEDA_SAPOIO_FRENT" or value[18] == "QUEDA_SAPOIO_FRENTE"):
          value[18] = 12
        if(value[18] == "SENTA" or value[18] == "SENTAR"):
          value[18] = 13
        if(value[18] == "SENTAR_APOIO"):
          value[18] = 14
        if(value[18] == "SENTAR_SAPOIO"):
          value[18] = 15
        if(value[18] == "TATEA" or value[18] == "TATEAR"):
          value[18] = 16

    MyNewDataSetTrain_ = np.delete(MyNewDataSetTrain_, (0), axis=0)
    MyNewDataSetTest_ = np.delete(MyNewDataSetTest_, (0), axis=0)
    return MyNewDataSetTrain_, MyNewDataSetTest_, labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest, labelTrain2, labelTest2, MyNewDataSetTrain2, MyNewDataSetTest2 