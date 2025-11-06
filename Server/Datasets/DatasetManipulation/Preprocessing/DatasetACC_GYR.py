from __future__ import absolute_import, division, print_function, unicode_literals
from six.moves import urllib
from scipy import stats ##statistic functions
from . import DatasetSensorType
import math
import statistics as st
import numpy as np
import pandas as pd
import scipy

class DatasetACC_GYR(DatasetSensorType.DatasetSensorType):
    
    def feature_extraction_acc_gyr (self, arr):
        arr_acc_rms = np.array([[0.0, "", ""]])
        arr_gyr_rms = np.array([[0.0, "", ""]])
        #Gera vertor de valores unificados para os dados de ACC e GYR
        infoName = arr[0,4]
        for line in arr:
            if(line[3] == "ACC"):
              arr_acc_rms = np.vstack([arr_acc_rms,[self.calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
            if(line[3] == "GYR"):
              arr_gyr_rms = np.vstack([arr_gyr_rms,[self.calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
        arr_acc_rms = np.delete(arr_acc_rms, (0), axis=0) #deleta primeira linha vazia
        arr_gyr_rms = np.delete(arr_gyr_rms, (0), axis=0)

        #Vector base for feature extractions
        vector_value_acc = [float(i) for i in [x[0] for x in arr_acc_rms]] #retorna primeira coluna da matriz de ACC
        vector_value_gyr = [float(i) for i in [x[0] for x in arr_gyr_rms]] #retorna primeira coluna da matriz de GYR

        result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), 0, stats.iqr(vector_value_acc),
                st.mean(vector_value_gyr), max(vector_value_gyr), min(vector_value_gyr), st.stdev(vector_value_gyr), stats.kurtosis(vector_value_gyr),
                stats.skew(vector_value_gyr), stats.entropy(vector_value_gyr), 0, stats.iqr(vector_value_gyr),
                infoName]
               
        return result
    
    def choicelinesForTest(self, numberOfLines, numberChoices):
        import random
        lines = []
        for i in range(numberChoices):
            lines.append(random.randint(1,numberOfLines))        
        return lines
    
    #Final States for ACC and GYR    
    def convertlabelInt(self, arr):
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

    #Final States
    def returnFinalStates():
        class_names = ['Walk', 'Hitting on a table', 'Hitting a wall', 'Running', 'Laying', 'Bumping the Wall', 'Writing', 'Clapping Standing', 'Clap Sitting', 'Jump', 'Fall Forward With Support', 'Fall Forward Without Support', 'Fall to the Sides', 'Sitting', 'Sitting With Support', 'Sitting Without Support', 'Grope']
        return class_names

    def executePreprocessing(self):
        #Result Datasets        
        MyNewDataSetTest = None
        labelTest = None
        MyNewDataSetTrain = None
        labelTrain = None
        
        #Dataset Header
        MyNewDataSet = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", ("IQR ACC"), "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", ("IQR GYR"),
                    "Movement"]])
        
        #Get data from dataset, extract features and put in dataset
        for dataset in self.datasetList:
            #Dataset1
            
            for arr in dataset.feature_extract_dataset():
                MyNewDataSet = np.vstack([MyNewDataSet, self.feature_extraction_acc_gyr(arr)])
        
        #Dataset       
        MyNewDataSetTrain = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC", "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR"]])
        labelTrain = np.array(["Movement"])
        MyNewDataSetTest = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC", "Mean GYR", "MAX GYR", "MIN GYR", "STD GYR", "Kurtosis GYR", "Skewness GYR", "Entropy GYR", "MAD GYR", "IQR GYR"]])
        labelTest = np.array(["Movement"])

        numberTests = len(MyNewDataSet)*10//100
        linesForTest = self.choicelinesForTest(len(MyNewDataSet), numberTests)
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
        MyNewDataSetTrain = MyNewDataSetTrain.astype(np.float64)
        MyNewDataSetTest = np.delete(MyNewDataSetTest, (0), axis=0)
        MyNewDataSetTest = MyNewDataSetTest.astype(np.float64)
        labelTrain = np.delete(labelTrain, (0), axis=0)
        labelTest = np.delete(labelTest, (0), axis=0) #precisa melhorar balancemento
        #print(labelTrain)
        
        labelTrain = self.convertlabelInt(labelTrain)
        labelTest = self.convertlabelInt(labelTest)
        
        return labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest
        
    
    