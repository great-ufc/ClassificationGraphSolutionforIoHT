from DBConnection import DBConnection
from DBInitialize import DBInitialize
from Dao import DAO
from addVerticeEdgeLists import addSensorList, addFeatureList, addMLModelList, addFinalStateList, addMLAlgorithmList
from addVerticeEdgeLists import addSensorFeatureList, addFeatureMLModel, addMLModelFinalState
from Entities import Sensor, Feature, MLModel, FinalState, MLAlgorithm
from XMLCreate import xml_create
from ModelANNTensorflow import trainModelAllSensors, trainModelWithOnlyACC
from graphFunctions import addToGraph, getGraphValues, optimizeGraph
import DatabasePreprocessing1 as dbp1

import os
import platform

so = platform.system()
db = DBInitialize()
dao = DAO(db.connection_db)

print("=========Initialize Graph Generate Data===========")

algorithName = ["Artificial Neural Network"]
modelName = ["ANNModel.tflite"]
sensorList = [["acc", "accelerometer"], ["gyr","gyroscope"]]
featureList = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr","gyr_mean", "gyr_max", "gyr_min", "gyr_std", "gyr_kurtosis", "gyr_skewness", "gyr_entropy", "gyr_mad", "gyr_iqr"]
modelName2 = ["ANNModel2.tflite"]
sensorList2 = [["acc", "accelerometer"]]
featureList2 = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr"]
finalStateList = ['Andar', 'BATER_NA_MESA', 'BATER_PAREDE', 'CORRENDO', 'DEITAR','ESBARRAR_PAREDE', 'ESCREVER', 'PALMAS_EMP', 'PALMAS_SEN', 'PULO','QUEDA_APOIO_FRENTE', 'QUEDA_LATERAL', 'QUEDA_SAPOIO_FRENTE', 'SENTAR', 'SENTAR_APOIO', 'SENTAR_SAPOIO', 'TATEAR']
preprocessingData = dbp1.executePreproccessing()
modelGenerated = trainModelAllSensors(0.8, 1, 10, preprocessingData)
modelGenerated2 = trainModelWithOnlyACC(0.8, 1, 10, preprocessingData)


print("=========Generate Graph===========")

#sensors = []
#features = []
#mlmodels = []
#finalstates = []

#Add grafo
valuesList = getGraphValues(sensorList, featureList, algorithName, modelName, finalStateList, modelGenerated)[1]
probability = valuesList[1]
valuesList = valuesList[0]
valuesList2 = getGraphValues(sensorList2, featureList2, algorithName, modelName2, finalStateList, modelGenerated2)[1]
probability2 = valuesList2[1]
valuesList2 = valuesList2[0]

if so == "Windows":
    os.system('cls') or None
if so == "Linux":
    os.system('clear') or None

print("\n=================\n")

addToGraph(dao, valuesList, probability)
addToGraph(dao, valuesList2, probability2)

print("\n=================\n")


#for i in range(2,50):
#    dao.delete("SensorFeature",i)
edges = dao.includeEdgeList()
edgeSensorFeatures = edges[0]
edgeFeatureModels = edges[1] 
edgeModelFinalStates = edges[2]


print('======edgeSensorFeatures========')
for e in edgeSensorFeatures:
    print(e.Sensor.sensorName + ' - ' + e.Feature.featureName) 
#print(edgeSensorFeatures)

print('======edgeFeatureModels========')
for e in edgeFeatureModels:
    print(e.Feature.featureName + ' - ' + e.MLModel.titleModel + e.MLModel.modelExtension)

print('======edgeModelFinalStates========')
for e in edgeModelFinalStates:
    print(e.MLModel.titleModel + e.MLModel.modelExtension + ' - ' + e.FinalState.description)

xml_create(edgeSensorFeatures, edgeFeatureModels, edgeModelFinalStates)

#addElements
'''
addSensorList(dao,sensors)
addFeatureList(dao,features)
addMLModelList(dao,mlmodels)
addFinalStateList(dao,finalstates)
addMLAlgorithmList(dao,mlalgorithms)
'''

#teste
'''
acc = Sensor()
acc.Sensor_id = 1
acc.typeSensor = "acc"
acc.sensorName = "accelerometer"
gyr = Sensor()
gyr.Sensor_id = 2
gyr.typeSensor = "gyr"
gyr.sensorName = "gyroscope"
gps = Sensor()
gps.Sensor_id = 3
gps.typeSensor = "gps"
gps.sensorName = "gps"
sensors.append(acc)
sensors.append(gyr)
sensors.append(gps)

acc_mean = Feature()
acc_mean.Feature_id = 1
acc_mean.featureName = "acc_mean"
features.append(acc_mean)
gyr_mean = Feature()
gyr_mean.Feature_id = 2
gyr_mean.featureName = "gyr_mean"
features.append(gyr_mean)
acc_max = Feature()
acc_max.Feature_id = 3
acc_max.featureName = "acc_max"
features.append(acc_max)

annmodel = MLModel()
annmodel.MLModel_id = 1
annmodel.MLAlgorihtm_id = 1
annmodel.titleModel = "ANNModel"
annmodel.modelExtension = ".tflite"
annmodel.numInFeature = 18
annmodel.numOutFeature = 17
annmodel2 = MLModel()
annmodel2.MLModel_id = 2
annmodel2.MLAlgorihtm_id = 1
annmodel2.titleModel = "ANNModel2"
annmodel2.modelExtension = ".tflite"
annmodel2.numInFeature = 18
annmodel2.numOutFeature = 17
mlmodels.append(annmodel)
mlmodels.append(annmodel2)

normalWalking = FinalState()
normalWalking.FinalState_id = 1
normalWalking.description = "Normal Walking"
normalWalking.hasAnyHealthConditionAssociated = 0
normalWalking.healthConditionsAssociated = ""
jump = FinalState()
jump.FinalState_id = 2
jump.description = "Jump"
jump.hasAnyHealthConditionAssociated = 0
jump.healthConditionsAssociated = ""
fall = FinalState()
fall.FinalState_id = 3
fall.description = "Fall"
fall.hasAnyHealthConditionAssociated = 0
fall.healthConditionsAssociated = ""
finalstates.append(normalWalking)
finalstates.append(jump)
finalstates.append(fall)

mlalgorithms = []
ann = MLAlgorithm()
ann.MLAlgorithm_id = 1
ann.mlAlgorithmName = "Artificial Neural Network"
regressaoLinear = MLAlgorithm()
regressaoLinear.MLAlgorithm_id = 2
regressaoLinear.mlAlgorithmName = "Regressão Linear"
mlalgorithms.append(ann)
mlalgorithms.append(regressaoLinear)

print("==============teste sensors==================")
#addMLModelFinalState(dao, [[1,2],[1,3]])
#addElements
print(addSensorList(dao,sensors))
print(addFeatureList(dao,features))
print(addMLModelList(dao,mlmodels))
print(addFinalStateList(dao,finalstates))
'''

'''
if so == "Windows":
    os.system('cls') or None
if so == "Linux":
    os.system('clear') or None

print("\n=================\n")

#addElements
addSensorList(dao,sensors)
addFeatureList(dao,features)
addMLModelList(dao,mlmodels)
addFinalStateList(dao,finalstates)
addMLAlgorithmList(dao,mlalgorithms)

print("\n=================\n")

addSensorFeatureList(dao,[[1,3],[2,2]], True)
addFeatureMLModel(dao,[[2,1],[3,1],[1,2],[2,2],[3,2]], True)
#addMLModelFinalState(dao, [[1,2],[1,3]])
addMLModelFinalState(dao, [[1,2],[1,3],[2,1],[2,2],[2,3]], True)
'''
#dao.delete("Feature", 3)
#for i in range(0,16):
#    dao.delete("Feature", i)

#for i in range(0,100):
#    dao.delete("MLModel", i)

#for i in range(3,20):
#    dao.delete("SensorFeature", i)
#dao.delete("FeatureMLModel", 2)

#for i in range(2,20):
#    dao.delete("MLAlgorithm", i)

#for i in range(20,100):
#    dao.delete("MLModelFinalState", i)
#os.system('cls') or None


'''
print("\n=================\n")

sensorsl = dao.findAllRecords("Sensor")
featuresl = dao.findAllRecords("Feature")
mlModelsl = dao.findAllRecords("MLModel")
finalStatel = dao.findAllRecords("FinalState")
mlAlgorithml = dao.findAllRecords("MLAlgorithm")
edges = dao.includeEdgeList()

print("\n=================\n")
#os.system('cls') or None
print(sensorsl)
print(featuresl)
print(mlModelsl)
print(finalStatel)
print(mlAlgorithml)


print("\n=================\n")
edges = dao.includeEdgeList()
edgeSensorFeatures = edges[0] 
edgeFeatureModels = edges[1] 
edgeModelFinalStates = edges[2]
idtest = 0
print(edgeSensorFeatures[idtest].Sensor.sensorName + " - " + edgeSensorFeatures[idtest].Feature.featureName)
idtest = 0
print(edgeFeatureModels[idtest].Feature.featureName +" - " +edgeFeatureModels[idtest].MLModel.titleModel)
idtest = 1
print(edgeModelFinalStates[idtest].MLModel.titleModel +" - "+edgeModelFinalStates[idtest].FinalState.description)

print("\n=================\n")

for e in edgeSensorFeatures:
    print(e.Feature.featureName)
    
for e in edgeFeatureModels:
    print(e.MLModel.titleModel+e.MLModel.modelExtension)

xml_create(edgeSensorFeatures, edgeFeatureModels, edgeModelFinalStates)
'''


print('================================')
print('==========Otimizado=============')
print('================================')

#sensors = ['acc','gyr']
sensors = ['acc']
graphOptimized = optimizeGraph(dao,sensors, 0.50)
edgeSensorFeaturesO = graphOptimized[0]
edgeFeatureModelsO = graphOptimized[1] 
edgeModelFinalStatesO = graphOptimized[2]

print('======edgeSensorFeaturesO========')
for e in edgeSensorFeaturesO:
    print(e.Sensor.sensorName + ' - ' + e.Feature.featureName) 
#print(edgeSensorFeatures)

print('======edgeFeatureModelsO========')
for e in edgeFeatureModelsO:
    print(e.Feature.featureName + ' - ' + e.MLModel.titleModel + e.MLModel.modelExtension)
    print(str(e.MLModel.numInFeature) + ' - ' + str(e.MLModel.numOutFeature))

print('======edgeModelFinalStatesO========')
for e in edgeModelFinalStatesO:
    print(e.MLModel.titleModel + e.MLModel.modelExtension + ' - ' + e.FinalState.description)
    print(str(e.MLModel.numInFeature) + ' - ' + str(e.MLModel.numOutFeature) + ' - ' + str(e.probability))

xml_create(edgeSensorFeaturesO, edgeFeatureModelsO, edgeModelFinalStatesO, "KnowledgeBaseOptimized")