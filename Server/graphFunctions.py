from DAO.Dao import DAO
from Database.DBConnection import DBConnection
from DBInitialize import DBInitialize
from DAO.addVerticeEdgeLists import addSensorList, addFeatureList, addMLModelList, addFinalStateList, addMLAlgorithmList
from DAO.addVerticeEdgeLists import addSensorFeatureList, addFeatureMLModel, addMLModelFinalState
from DAO.Entities import Sensor, Feature, MLModel, FinalState, MLAlgorithm

#Create Graph from DataSet and ML Model trained
def addToGraph(dao, valuesList, probability):        
    #Sensors
    sensorEdgeLst = []
    sensorsValues = valuesList[0]
    for sv in sensorsValues:
        sen = Sensor()
        sen.Sensor_id = 0
        sen.typeSensor = sv[0]
        sen.sensorName = sv[1]
        sensorEdgeLst.append(sen)
    sensorEdgeLst = addSensorList(dao,sensorEdgeLst)
    
    #Features
    featureEdgeLst = []
    featuresValues = valuesList[1]
    for fv in featuresValues:
        fea = Feature()
        fea.Feature_id = 0
        fea.featureName = fv
        featureEdgeLst.append(fea)
    featureEdgeLst = addFeatureList(dao,featureEdgeLst)

    #sensorFeature
    sensorFeatureEdgeLst = []
    for s in sensorEdgeLst:
        sense = dao.findRecordById("Sensor",s)
        for f in featureEdgeLst:
            feat = dao.findRecordById("Feature",f)
            if sense[1] == feat[1].split("_")[0]:
                sensorFeatureEdgeLst.append([s,f])
    addSensorFeatureList(dao,sensorFeatureEdgeLst, True)
    
    #MLAlgorithm
    mlAlgorithmValues = valuesList[2]
    mlalgorithms = []
    for mav in mlAlgorithmValues:
        mlalgorithms = []
        ann = MLAlgorithm()
        ann.MLAlgorithm_id = 0
        ann.mlAlgorithmName = mav
        mlalgorithms.append(ann)
    mlalgorithms = addMLAlgorithmList(dao,mlalgorithms)
    
    #FinalState
    finalStateValues = valuesList[4]
    finalStateLst = []
    for fsv in finalStateValues:
        finalS = FinalState()
        finalS.FinalState_id = 0
        finalS.description = fsv
        finalS.hasAnyHealthConditionAssociated = 0
        finalS.healthConditionsAssociated = ""
        finalStateLst.append(finalS)
    finalStateLst = addFinalStateList(dao,finalStateLst)
    
    #MLModel
    mlmodelValues = valuesList[3]
    mlmodelsEdgeLst = []
    for mmv in mlmodelValues:
        model1 = MLModel()
        model1.MLModel_id = 0
        model1.MLAlgorihtm_id = mlalgorithms[0]
        model1.titleModel = mmv.split(".")[0]
        model1.modelExtension = "."+mmv.split(".")[1]
        model1.numInFeature = len(featureEdgeLst)
        model1.numOutFeature = len(finalStateLst)
        mlmodelsEdgeLst.append(model1)
    mlmodelsEdgeLst = addMLModelList(dao,mlmodelsEdgeLst)
    
    #FeatureModel
    featureModelEdgeLst = []
    for f in featureEdgeLst:
        for m in mlmodelsEdgeLst:
            featureModelEdgeLst.append([f,m])
    addFeatureMLModel(dao,featureModelEdgeLst, True)
    
    #MLModelFinalState
    mlmodelFinalStateEdgeLst = []
    for m in mlmodelsEdgeLst:
        for fs in finalStateLst:
            mlmodelFinalStateEdgeLst.append([m,fs, probability])
    addMLModelFinalState(dao,mlmodelFinalStateEdgeLst, True)

def getGraphValues(sensorList, featureList, algorithName, modelName, finalStateList, modelGenerated):
    graphValues = []
    graphValues.append(sensorList)
    graphValues.append(featureList)
    graphValues.append(algorithName)
    graphValues.append(modelName)
    graphValues.append(finalStateList)
    return [modelGenerated[0], [graphValues,modelGenerated[1]]]

def optimizeGraph(dao, sensors, probability = 0):
    db = DBInitialize()
    dao = DAO(db.connection_db)
    
    #for i in range(2,50):
    #    dao.delete("SensorFeature",i)
    
    graph = dao.includeEdgeList()
    edgeSensorFeatures = graph[0]
    edgeFeatureModels = graph[1] 
    edgeModelFinalStates = graph[2]
    
    #edgeSensorFeaturesOptimized
    edgeSensorFeaturesOptimized = []
    for esf in edgeSensorFeatures:
        if esf.Sensor.typeSensor not in sensors:
            continue
        edgeSensorFeaturesOptimized.append(esf)
    
    #edgeFeatureModelsOptimized
    edgeFeatureModelsOptimized = []
    noModels = []
    featuresOptimized = []
    for sf in edgeSensorFeaturesOptimized:
        featuresOptimized.append(sf.Feature.featureName)
    for efm in edgeFeatureModels:
        if efm.Feature.featureName not in featuresOptimized:
            if efm.MLModel.MLModel_id not in noModels:
                noModels.append(efm.MLModel.MLModel_id)
    for efm in edgeFeatureModels:
        if (efm.Feature.featureName in featuresOptimized) and (efm.MLModel.MLModel_id not in noModels):
            edgeFeatureModelsOptimized.append(efm)
            
    #edgeModelFinalStatesOptimized
    edgeModelFinalStatesOptimized = []
    modelsOptimized = []
    for fm in edgeFeatureModelsOptimized:
        modelsOptimized.append(fm.MLModel.MLModel_id)
    for emf in edgeModelFinalStates:
        if (emf.MLModel.MLModel_id not in modelsOptimized) or (emf.probability < probability):
            continue
        edgeModelFinalStatesOptimized.append(emf)
    
    #remove edges with probability less than informed
    modelsOptimized = []
    featuresOptimized = []
    for fm in edgeModelFinalStatesOptimized:
        if fm.MLModel.titleModel not in modelsOptimized:
            modelsOptimized.append(fm.MLModel.titleModel)
    for efm in edgeFeatureModelsOptimized:
        if efm.MLModel.titleModel in modelsOptimized:
            featuresOptimized.append(efm.Feature.featureName)
    
 
    featuresModels = []
    sensorsFeatures = []    
    for sfm in edgeSensorFeaturesOptimized:
        if sfm.Feature.featureName not in featuresOptimized:
            sensorsFeatures.append(sfm)
    for efm in edgeFeatureModelsOptimized:
        if efm.MLModel.titleModel not in modelsOptimized:
            featuresModels.append(efm)
            
    #remove edgeSensorFeatures
    for sfm in edgeSensorFeatures:
        if sfm in sensorsFeatures:
            edgeSensorFeaturesOptimized.remove(sfm)
            
    #remove edgeFeatureModels        
    for efm in edgeFeatureModels:
        if efm in featuresModels:
            edgeFeatureModelsOptimized.remove(efm)
    
    return [edgeSensorFeaturesOptimized, edgeFeatureModelsOptimized, edgeModelFinalStatesOptimized]

if __name__ == "__main__": 
    from ModelANNTensorflow import getGraphValues, getGraphValues2
    print("\n=================\n")
    valuesList = getGraphValues()[0]
    probability = valuesList[1]
    valuesList = valuesList[0]
    valuesList2 = getGraphValues2()[0]
    probability2 = valuesList2[1]
    valuesList2 = valuesList2[0]
    
    #connect DB and initialize daoFunctions
    db = DBInitialize()
    dao = DAO(db.connection_db)
    
    #add elments to graph
    addToGraph(dao, valuesList, probability)
    addToGraph(dao, valuesList2, probability2)
    
    #limpa tela
    import os
    import platform
    so = platform.system()
    if so == "Windows":
        os.system('cls') or None
    if so == "Linux":
        os.system('clear') or None
    
    print("\n=======Complete Graph==========\n")

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

    print("\n========Optimezed=========\n")
    sensors = ['acc']
    graphOptimized = optimizeGraph(dao, sensors)
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

