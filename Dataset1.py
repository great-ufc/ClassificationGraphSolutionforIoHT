from Dataset import Dataset
from os.path import join
import glob
import os
import platform
import numpy as np

class Dataset1 (Dataset):
    name = "Dataset1"
    
	#feature extracion for Dataset1  
    def feature_extract_dataset(self):
        pathDataset = self.path#"Datasets/Dataset1"
        
        #SO Configuration
        so = platform.system()
        file_list = [] ##Lista de arquivos no meu Dataset
        for file in glob.glob(pathDataset+"/*"):
            if so == "Windows":
                file_list.append(file.split("\\")[1])
            if so == "Linux":
                file_list.append(file.split("/")[2])
        
        arr_list = []
        ##Adiciona os streams no dataset. Uma linha para cada arquivo 
        for file in file_list: ##ler arquivos na pasta
          arr = np.array([[0.0, 0.0, 0.0, "", ""]])
          movement = str(file).split(".")[0][0:len(str(file)[0])-3]
          movement = movement[6:len(movement)]
          fname = os.path.join(self.path, file)
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
          arr_list.append(arr)
        return arr_list