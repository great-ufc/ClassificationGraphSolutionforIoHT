class DatasetSensorType:
    def __init__(self, datasetList):
        self.datasetList = datasetList

    def executePreprocessing():
        return None
        
    ##Util functions for Dataset Preprocessing
    #return rms
    def calc_rms(self, x,y,z):
       import math
       return math.sqrt(x*x+y*y+z*z)