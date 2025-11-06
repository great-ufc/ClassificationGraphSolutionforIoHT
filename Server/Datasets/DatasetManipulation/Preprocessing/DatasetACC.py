from __future__ import absolute_import, division, print_function, unicode_literals
from six.moves import urllib
from scipy import stats ##statistic functions
from . import DatasetSensorType
import math
import statistics as st
import numpy as np
import pandas as pd
import scipy

class DatasetACC(DatasetSensorType.DatasetSensorType):
    
    def feature_extraction_acc (self, arr):
        arr_acc_rms = np.array([[0.0, "", ""]])
        #Gera vertor de valores unificados para os dados de ACC
        infoName = arr[0,4]
        for line in arr:
            if(line[3] == "ACC"):
                arr_acc_rms = np.vstack([arr_acc_rms,[self.calc_rms(float(line[0]),float(line[1]),float(line[2])),line[3],line[4]]])
        arr_acc_rms = np.delete(arr_acc_rms, (0), axis=0) #deleta primeira linha vazia

        #Vector base for feature extractions
        vector_value_acc = [float(i) for i in [x[0] for x in arr_acc_rms]] #retorna primeira coluna da matriz de ACC

        result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), 0, stats.iqr(vector_value_acc),
                infoName]
               
        return result
    
    def choicelinesForTest(self, numberOfLines, numberChoices):
        import random
        lines = []
        for i in range(numberChoices):
            lines.append(random.randint(1,numberOfLines))        
        return lines
    
    #Final States for ACC     
    def convertlabelInt(self, arr):
      lvalue = np.array(-1)
  
      for value in arr:
        if(value[0] == "ANDA" or value[0] == "ANDAR" or value[0] == "Walk" or value[0] == "walk"):
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
        if(value[0] == "Brush_teeth" or value[0] == "brush_teeth"):
              lvalue = np.append(lvalue,17)
        if(value[0] == "Climb_stairs" or value[0] == "climb_stairs"):
          lvalue = np.append(lvalue,18)
        if(value[0] == "Comb_hair" or value[0] == "comb_hair"):
          lvalue = np.append(lvalue,19)
        if(value[0] == "Descend_stairs" or value[0] == "descend_stairs"):
          lvalue = np.append(lvalue,20)
        if(value[0] == "Drink_glass" or value[0] == "drink_glass"):
          lvalue = np.append(lvalue,21)
        if(value[0] == "Eat_meat" or value[0] == "eat_meat"):
          lvalue = np.append(lvalue,22)
        if(value[0] == "Eat_soup" or value[0] == "eat_soup"):
          lvalue = np.append(lvalue,23)
        if(value[0] == "Getup_bed" or value[0] == "getup_bed"):
          lvalue = np.append(lvalue,24)
        if(value[0] == "Liedown_bed" or value[0] == "liedown_bed"):
          lvalue = np.append(lvalue,25)
        if(value[0] == "Pour_water" or value[0] == "pour_water"):
          lvalue = np.append(lvalue,26)
        if(value[0] == "Sitdown_chair" or value[0] == "sitdown_chair"):
          lvalue = np.append(lvalue,27)
        if(value[0] == "Standup_chair" or value[0] == "standup_chair"):
          lvalue = np.append(lvalue,28)
        if(value[0] == "Use_telephone" or value[0] == "use_telephone"):
          lvalue = np.append(lvalue,29)
      lvalue = np.delete(lvalue, (0), axis=0)
      return lvalue

    #Final States
    def returnFinalStates():
        class_names = ['Walk', 'Hitting on a table', 'Hitting a wall', 'Running', 'Laying', 'Bumping the Wall', 'Writing', 'Clapping Standing', 'Clap Sitting', 'Jump', 'Fall Forward With Support', 'Fall Forward Without Support', 'Fall to the Sides', 'Sitting', 'Sitting With Support', 'Sitting Without Support', 'Grope', 'Brush_teeth', 'Climb_stairs', 'Comb_hair', 'Descend_stairs', 'Drink_glass', 'Eat_meat', 'Eat_soup', 'Getup_bed', 'Liedown_bed', 'Pour_water','Sitdown_chair', 'Standup_chair', 'Use_telephone']
        return class_names

    def executePreprocessing(self):
        #Result Datasets        
        MyNewDataSetTest = None
        labelTest = None
        MyNewDataSetTrain = None
        labelTrain = None
        
        #Dataset Header
        MyNewDataSet = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", ("IQR ACC"),"Movement"]])
        
        #Get data from dataset, extract features and put in dataset
        for dataset in self.datasetList:
            #Dataset1 e Dataset2
            for arr in dataset.feature_extract_dataset():
                MyNewDataSet = np.vstack([MyNewDataSet, self.feature_extraction_acc(arr)])
        
        #Dataset        
        MyNewDataSetTrain = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
        labelTrain = np.array(["Movement"])
        MyNewDataSetTest = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
        labelTest = np.array(["Movement"])

        numberTests = len(MyNewDataSet)*10//100
        linesForTest = self.choicelinesForTest(len(MyNewDataSet), numberTests)
        count = 0

        for line in MyNewDataSet:
            if(count > 0):
                if(count in linesForTest):
                  labelTest = np.vstack([labelTest, line[9]])
                  line = np.delete(line, 9, 0)
                  MyNewDataSetTest = np.vstack([MyNewDataSetTest, line])
                else:
                  labelTrain = np.vstack([labelTrain, line[9]])
                  line = np.delete(line, 9, 0)
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
        
