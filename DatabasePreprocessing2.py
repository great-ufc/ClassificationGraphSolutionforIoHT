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

def convertlabelInt(arr):
  lvalue = np.array(-1)
  
  for value in arr:
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
    if(value[0] == "Walk" or value[0] == "walk"):
      lvalue = np.append(lvalue,0)
  lvalue = np.delete(lvalue, (0), axis=0)
  return lvalue

def extractFeatures(MyNewDataSetTest, labelTest, MyNewDataSetTrain, labelTrain, class_names, MyNewDataSetTest_, MyNewDataSetTrain_):
    
    pathDataset = "Datasets/D2_ADL_Dataset/HMP_Dataset/All_data"


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
    
    MyNewDataSet = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", ("IQR ACC"),"Movement"]])
    
    #retona rms
    def calc_rms(x,y,z):
       return math.sqrt(x*x+y*y+z*z)
       
    def calc_noise(data):
        return -14.709 + (data/63)*(2*14.709)

    def feature_extraction_acc (arr):
      arr_acc_rms = np.array([[0.0, "", ""]])
      #Gera vertor de valores unificados para os dados de ACC e Gyr
      infoName = arr[0,4]
      for line in arr:
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
       
      result = [st.mean(vector_value_acc), max(vector_value_acc), min(vector_value_acc), st.stdev(vector_value_acc), stats.kurtosis(vector_value_acc), 
                stats.skew(vector_value_acc), stats.entropy(vector_value_acc), 0, stats.iqr(vector_value_acc),
                infoName]
               
                            
      
      return result  
    
    ##Adiciona os streams no dataset. Uma linha para cada arquivo 
    for file in file_list: ##ler arquivos na pasta
      arr = np.array([[0.0, 0.0, 0.0, "", ""]])
      movement = str(file).split(".")[0][0:len(str(file_list[0])[0])-3].split("-")[7]
      fname = os.path.join(path, file)
      with open(fname, 'r') as f:
        lines = f.readlines()
        for line in lines: ##ler linhas do arquivo
          #print(len(line.split(':')))
          if(len(line.split(':')) < 2):
            sensor = "ACC"
            row = [calc_noise(float(line.split(' ')[0])),calc_noise(float(line.split(' ')[1])), calc_noise(float(line.split(' ')[2])), sensor, movement]
            arr = np.vstack([arr,row])
      arr = np.delete(arr, (0), axis=0) #deleta primeira linha vazia
      MyNewDataSet = np.vstack([MyNewDataSet, feature_extraction_acc(arr)])
      
      #print(fname)
      ##print(arr.shape)
      ##print(arr[10])
      #break
    print(MyNewDataSet)
    
    MyNewDataSetTrain = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
    labelTrain = np.array(["Movement"])
    MyNewDataSetTest = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC"]])
    labelTest = np.array(["Movement"])
    
    numberTests = len(MyNewDataSet)*10//100

    def choicelinesForTest(numberOfLines, numberChoices):
        import random
        lines = []
        for i in range(numberChoices):
            lines.append(random.randint(1,numberOfLines))        
        return lines

    linesForTest = choicelinesForTest(len(MyNewDataSet), numberTests)
    
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
    MyNewDataSetTrain = MyNewDataSetTrain.astype(np.float)
    MyNewDataSetTest = np.delete(MyNewDataSetTest, (0), axis=0)
    MyNewDataSetTest = MyNewDataSetTest.astype(np.float)
    labelTrain = np.delete(labelTrain, (0), axis=0)
    labelTest = np.delete(labelTest, (0), axis=0) #precisa melhorar balancemento

    print(MyNewDataSet.shape)
    print(MyNewDataSetTrain.shape)
    print(MyNewDataSetTest.shape)
    print(np.unique(labelTrain))

    labelTrain = convertlabelInt(labelTrain)
    labelTest = convertlabelInt(labelTest)
   
    print(labelTest)

    ##Prepara as classes 
    class_names = ['Brush_teeth', 'Climb_stairs', 'Comb_hair', 'Descend_stairs', 'Drink_glass', 'Eat_meat', 'Eat_soup', 'Getup_bed', 'Liedown_bed', 'Pour_water','Sitdown_chair', 'Standup_chair', 'Use_telephone', 'Walk']

    MyNewDataSetTrain_ = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC", "Movement"]])
    MyNewDataSetTest_ = np.array([["Mean ACC", "MAX ACC", "MIN ACC", "STD ACC", "Kurtosis ACC", "Skewness ACC", "Entropy ACC", "MAD ACC", "IQR ACC", "Movement"]])

    count = 0
    for line in MyNewDataSet:
      if(count > 0):
        if(count % 20 == 0):
          MyNewDataSetTest_ = np.vstack([MyNewDataSetTest_, line])
        else:
          MyNewDataSetTrain_ = np.vstack([MyNewDataSetTrain_, line])  
      count=count+1

    for value in MyNewDataSetTest_:
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
        if(value[0] == "Walk" or value[0] == "walk"):
          lvalue = np.append(lvalue,0)

    for value in MyNewDataSetTrain_:
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
        if(value[0] == "Walk" or value[0] == "walk"):
          lvalue = np.append(lvalue,0)

    MyNewDataSetTrain_ = np.delete(MyNewDataSetTrain_, (0), axis=0)
    MyNewDataSetTest_ = np.delete(MyNewDataSetTest_, (0), axis=0)
    return MyNewDataSetTrain_, MyNewDataSetTest_, labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest
    
#====Teste====
if __name__ == "__main__":
    MyNewDataSetTest = None
    labelTest = None
    MyNewDataSetTrain = None
    labelTrain = None
    class_names = None
    MyNewDataSetTest_ = None
    MyNewDataSetTrain_ = None
    
    extractFeatures(MyNewDataSetTest, labelTest, MyNewDataSetTrain, labelTrain, class_names, MyNewDataSetTest_, MyNewDataSetTrain_)
    #executePreproccessing()