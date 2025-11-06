#Entities from server Classifications Graph generation system

from abc import ABC, abstractmethod

# list to String for classes Features and FinalStates
def _getIdtlString(list_):
        return str(list_).strip('[]')

#sensor
class Sensor:
    def __init__(self):
        self.Sensor_id = 0
        self.typeSensor = ""
        self.sensorName = ""


#feature
class Feature:
    def __init__(self):
        self.Feature_id = 0
        self.featureName = ""
 
#edgeSensorFeature
class EdgeSensorFeature:
    def __init__(self):
        self.Sensor = Sensor()
        self.Feature = Feature()
        self.context = []
 
#MLAlgorithm
class MLAlgorithm:
    def __init__(self):
        self.MLAlgorithm_id = 0
        self.mlAlgorithmName = ""
    
    @abstractmethod
    def run(self, numInputFeatures, numOutputStates, dataSetTrain, labelsTrain, dataSetEvaluation,  labelsEvaluation, anotherParams= {}):
        pass
    
#MLModel    
class MLModel():
    def __init__(self):
        self.MLModel_id = 0
        self.MLAlgorihtm_id = 0
        self.titleModel = ""
        self.modelExtension = ""
        self.numInFeature = 0
        self.numOutFeature = 0

class EdgeFeatureModel():
    def __init__(self):
        self.Feature = Feature()
        self.MLModel = MLModel()
        self.context = [] #0: inFeatures (# features de entrada), 1: outStates (# estados finais)I
    
# FinalState
class FinalState:
    def __init__(self):
        self.FinalState_id = 0
        self.description = ""
        self.hasAnyHealthConditionAssociated = False
        self.healthConditionsAssociated = ""
         
class EdgeModelFinalState:
    def __init__(self):
        self.MLModel = MLModel()
        self.FinalState = FinalState()
        self.probability = 0.0