from DatabaseQueryFunctions import insertRecord
from DatabaseQueryFunctions import updateRecord
from DatabaseQueryFunctions import deleteRecord
from DatabaseQueryFunctions import findAll
from DatabaseQueryFunctions import findById
from DatabaseQueryFunctions import findByValue
from Entities import Sensor, Feature, MLModel, FinalState, MLAlgorithm
from Entities import EdgeSensorFeature, EdgeFeatureModel, EdgeModelFinalState

class DAO:
    def __init__(self, connection_db):
        self.connection_db = connection_db
        pass
        
    def add(self, table_name, entity):
        colsName = [i for i in entity.__dict__.keys() if i[:1] != '_'][1:]
        colsValue = [i for i in entity.__dict__.values()][1:]
        dictValues = {}
        for i in range(len(colsName)):
                dictValues[colsName[i]] = colsValue[i]
        insertRecord(self.connection_db, table_name, dictValues)
    
    def addNE(self, table_name, dictValues):
        insertRecord(self.connection_db, table_name, dictValues)
    
    def update(self, table_name, entity, idVal):
        #values
        colsName = [i for i in entity.__dict__.keys() if i[:1] != '_'][1:]
        colsValue = [i for i in entity.__dict__.values()][1:]
        
        #conditions
        idName = [i for i in entity.__dict__.keys() if i[:1] != '_'][0]
        dictConditions = {str(idName):idVal}
        
        #update
        for i in range(len(colsValue)):
                dictValues = {}
                dictValues[colsName[i]] = colsValue[i]
                updateRecord(self.connection_db, table_name, dictValues, dictConditions)
    
    def delete(self,table_name, id_value):
        deleteRecord(self.connection_db, table_name, id_value)
    
    def findAllRecords(self, table_name):
        return findAll(self.connection_db,table_name)
        
    def findRecordById(self,table_name, id_value):
        return findById(self.connection_db, table_name, id_value)
        
    def findRecord(self, table, entity):
        colsName = [i for i in entity.__dict__.keys() if i[:1] != '_'][1:]
        colsValue = [i for i in entity.__dict__.values()][1:]
        dictValues = {}
        for i in range(len(colsName)):
                dictValues[colsName[i]] = colsValue[i]
        return findByValue(self.connection_db, table, dictValues)
    
    def includeEdgeList(self):
        edgeSensorFeatures = [] #EdgeSensorFeature()
        edgeFeatureModels = [] #EdgeFeatureModel()
        edgeModelFinalStates = [] #EdgeModelFinalState()
        SensorFeatures = self.findAllRecords('SensorFeature')
        FeatureMLModels = self.findAllRecords('FeatureMLModel')
        MLModelFinalStates = self.findAllRecords('MLModelFinalState')
        
        for SensorFeature in SensorFeatures:
            edgeSensorFeature = EdgeSensorFeature()
            
            sensor = Sensor()
            #print(SensorFeature[1])
            s = self.findRecordById('Sensor', SensorFeature[1])
            sensor.Sensor_id = s[0]
            sensor.typeSensor = s[1]
            sensor.sensorName = s[2]
            
            feature = Feature()
            f = self.findRecordById('Feature', SensorFeature[2])
            feature.Feature_id = f[0]
            feature.featureName = f[1]
            
            edgeSensorFeature.Sensor = sensor
            edgeSensorFeature.Feature = feature
            edgeSensorFeatures.append(edgeSensorFeature)
        
        for FeatureMLModel in FeatureMLModels:
            edgeFeatureModel = EdgeFeatureModel()
            print(FeatureMLModel)
            feature = Feature()
            f = self.findRecordById('Feature', FeatureMLModel[1])
            feature.Feature_id = f[0]
            feature.featureName = f[1]
            
            mLModel = MLModel()
            m = self.findRecordById('MLModel', FeatureMLModel[2])
            mLModel.MLModel_id = m[0]
            mLModel.MLAlgorihtm_id = m[1]
            mLModel.titleModel = m[2]
            mLModel.modelExtension = m[3]
            mLModel.numInFeature = m[4]
            mLModel.numOutFeature = m[5]
            
            edgeFeatureModel.Feature = feature
            edgeFeatureModel.MLModel = mLModel
            edgeFeatureModels.append(edgeFeatureModel)
        
        for MLModelFinalState in MLModelFinalStates:
            edgeModelFinalState = EdgeModelFinalState()
            
            mLModel = MLModel()
            m = self.findRecordById('MLModel', MLModelFinalState[1])
            mLModel.MLModel_id = m[0]
            mLModel.MLAlgorihtm_id = m[1]
            mLModel.titleModel = m[2]
            mLModel.modelExtension = m[3]
            mLModel.numInFeature = m[4]
            mLModel.numOutFeature = m[5]
            
            finalState = FinalState()
            f = self.findRecordById('FinalState', MLModelFinalState[2])
            finalState.FinalState_id = f[0]
            finalState.description = f[1]
            finalState.hasAnyHealthConditionAssociated = True if f[2] == 1 else False
            finalState.healthConditionsAssociated = f[3]
            
            probability = MLModelFinalState[3]
            
            edgeModelFinalState.MLModel = mLModel
            edgeModelFinalState.FinalState = finalState
            edgeModelFinalState.probability = probability
            edgeModelFinalStates.append(edgeModelFinalState)
        
        return [edgeSensorFeatures, edgeFeatureModels, edgeModelFinalStates]