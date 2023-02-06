from Dao import DAO

def addSensorList(dao, sensors):
    currentSensors = dao.findAllRecords("Sensor")
    currentsensorNames = []
    sensorIds = []
    for currentSensor in currentSensors:
        currentsensorNames.append(currentSensor[2])
    for sensor in sensors:
        if not (sensor.sensorName in currentsensorNames):
            dao.add("Sensor", sensor)
        sensorIds.append(dao.findRecord("Sensor", sensor)[0][0])
    return sensorIds

    
def addFeatureList(dao, features):
    currentFeatures = dao.findAllRecords("Feature")
    currentfeatureNames = []
    featureIds = []
    for currentFeature in currentFeatures:
        currentfeatureNames.append(currentFeature[1])
    for feature in features:
        if not (feature.featureName in currentfeatureNames):
            dao.add("Feature", feature)
        featureIds.append(dao.findRecord("Feature", feature)[0][0])
    return featureIds
    
def addSensorFeatureList(dao,SensorFeatures, verify = False):
    currentSensorFeatures = dao.findAllRecords("SensorFeature")
    if verify:
        for SensorFeature in SensorFeatures:
            flag = True
            for currentSF in currentSensorFeatures:
                if SensorFeature[0] == currentSF[1] and SensorFeature[1] == currentSF[2]:
                    flag = False
            if flag:
               dao.addNE("SensorFeature", {'Sensor_id':SensorFeature[0],'Feature_id':SensorFeature[1]}) 
    else:
        for SensorFeature in SensorFeatures:
            dao.addNE("SensorFeature", {'Sensor_id':SensorFeature[0],'Feature_id':SensorFeature[1]})

def addMLModelList(dao, MLModels):
    currentMLModels = dao.findAllRecords("MLModel")
    currentMLModelNames = []
    currentMLModelIDs = []
    mlModelIds = []
    for currentMLModel in currentMLModels:
        currentMLModelNames.append(currentMLModel[2])
    for mLModel in MLModels:
        if not (mLModel.titleModel in currentMLModelNames):
            dao.add("MLModel", mLModel)
        else:
            for currentMLModel in currentMLModels:
                if (mLModel.titleModel == currentMLModel[2]):
                    dao.update("MLModel", mLModel, currentMLModel[0])
                    break
        mlModelIds.append(dao.findRecord("MLModel", mLModel)[0][0])
    return mlModelIds

def addFeatureMLModel(dao, FeatureMLModels, verify = False):
    currentFeatureMLModels = dao.findAllRecords("FeatureMLModel")
    if verify:
        for FeatureMLModel in FeatureMLModels:
            flag = True
            for currentFM in currentFeatureMLModels:
                if FeatureMLModel[0] == currentFM[1] and FeatureMLModel[1] == currentFM[2]:
                    flag = False
            if flag:
               dao.addNE("FeatureMLModel", {'Feature_id': FeatureMLModel[0], 'MLModel_id': FeatureMLModel[1]}) 
    else:
        for FeatureMLModel in FeatureMLModels:
            dao.addNE("FeatureMLModel", {'Feature_id': FeatureMLModel[0], 'MLModel_id': FeatureMLModel[1]})

def addFinalStateList(dao, FinalStates):
    currentFinalStates = dao.findAllRecords("FinalState")
    currentFinalStateNames = []
    finalStateIds = []
    for currentFinalState in currentFinalStates:
        currentFinalStateNames.append(currentFinalState[1])
    for finalState in FinalStates:
        if not (finalState.description in currentFinalStateNames):
            dao.add("FinalState", finalState)
        finalStateIds.append(dao.findRecord("FinalState",finalState)[0][0])
    return finalStateIds

def addMLModelFinalState(dao, MLModelFinalStates, verify = False):
    currentMLModelFinalStates = dao.findAllRecords("MLModelFinalState")
    if verify:
        for MLModelFinalState in MLModelFinalStates:
            flag = True
            for currentMF in currentMLModelFinalStates:
                if MLModelFinalState[0] == currentMF[1] and MLModelFinalState[1] == currentMF[2]:
                    flag = False
            if flag:
                dao.addNE("MLModelFinalState", {'MLModel_id': MLModelFinalState[0], 'FinalState_id': MLModelFinalState[1], 'probability': MLModelFinalState[2] })
    else:
        for MLModelFinalState in MLModelFinalStates:
            dao.addNE("MLModelFinalState", {'MLModel_id': MLModelFinalState[0], 'FinalState_id': MLModelFinalState[1]})

def addMLAlgorithmList(dao, MLAlgorithms):
    currentMLAlgorithms = dao.findAllRecords("MLAlgorithm")
    currentMLAlgorithmNames = []
    mlAlgorithmIds = []
    for currentMLAlgorithm in currentMLAlgorithms:
        currentMLAlgorithmNames.append(currentMLAlgorithm[1])
    for mLAlgorithm in MLAlgorithms:
        if not (mLAlgorithm.mlAlgorithmName in currentMLAlgorithmNames):
            dao.add("MLAlgorithm", mLAlgorithm)
        mlAlgorithmIds.append(dao.findRecord("MlAlgorithm", mLAlgorithm)[0][0])
    return mlAlgorithmIds