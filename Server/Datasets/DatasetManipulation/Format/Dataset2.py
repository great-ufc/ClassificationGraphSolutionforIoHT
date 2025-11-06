from . import Dataset
from os.path import join
import glob
import os
import platform
import numpy as np

class Dataset2 (Dataset.Dataset):
    name = "Dataset2"
    
    #adjust sensor noise for Dataset 2    
    def calc_noiseD2(self, data):
        return -14.709 + (data/63)*(2*14.709)
	
	#feature extracion for Dataset2  
    def feature_extract_dataset(self):
        pathDataset = self.path#"Datasets/D2_ADL_Dataset/HMP_Dataset/All_data"
        
        #SO Configuration
        so = platform.system()
        file_list = [] ##Lista de arquivos no meu Dataset
        for file in glob.glob(pathDataset+"/*"):
            if so == "Windows":
                file_list.append(file.split("\\")[len(file.split("\\"))-1])
            if so == "Linux":
                file_list.append(file.split("/")[len(file.split("/"))-1])
         
        arr_list = []
        ##Adiciona os streams no dataset. Uma linha para cada arquivo 
        for file in file_list: ##ler arquivos na pasta
          arr = np.array([[0.0, 0.0, 0.0, "", ""]])
          movement = str(file).split(".")[0][0:len(str(file_list[0])[0])-3].split("-")[7]
          fname = os.path.join(self.path, file)
          with open(fname, 'r') as f:
            lines = f.readlines()
            for line in lines: ##ler linhas do arquivo
              #print(len(line.split(':')))
              if(len(line.split(':')) < 2):
                sensor = "ACC"
                row = [self.calc_noiseD2(float(line.split(' ')[0])),self.calc_noiseD2(float(line.split(' ')[1])), self.calc_noiseD2(float(line.split(' ')[2])), sensor, movement]
                arr = np.vstack([arr,row])
          arr = np.delete(arr, (0), axis=0) #deleta primeira linha vazia
          arr_list.append(arr)
        return arr_list