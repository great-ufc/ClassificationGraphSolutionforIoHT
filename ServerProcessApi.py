import json
import requests
import platform

api_token = 'seu_api_token'

so = platform.system()
if so == "Windows":
    api_url_base = 'http://3.86.153.243:3000'#'http://localhost:5000'
if so == "Linux":
    api_url_base = 'http://3.86.153.243:3000'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

def get_info(id=None):

    api_url_model = '{0}/UpdateGraphRequest/0'.format(api_url_base)
    api_url_model_generated = '{0}/UpdateGraphRequest/1'.format(api_url_base)
    api_url_model_generate = '{0}/UpdateGraphRequest/2'.format(api_url_base)
    api_url_optmize = '{0}/OptimizeGraphRequest/acc_gyr'.format(api_url_base)
    api_url_optmize_with_percentage = '{0}/OptimizeGraphRequest/acc/70'.format(api_url_base)
    api_url = '{0}//api/v1/resources/ngos'.format(api_url_base)
    
    if id == 0:
        response = requests.get(api_url_model, headers=headers)
        print(api_url_model)
    elif id == 3:
        response = requests.get(api_url_optmize, headers=headers)
        print(api_url_optmize)
    elif id == 1:
        response = requests.get(api_url_model_generated, headers=headers)
        print(api_url_model_generated)
    elif id == 2:
        response = requests.get(api_url_model_generate, headers=headers)
        print(api_url_model_generate)
    elif id == 4:
        response = requests.get(api_url_optmize_with_percentage, headers=headers)
        print(api_url_optmize_with_percentage)
    else:
        response = requests.get(api_url_base, headers=headers)
        print(api_url_base)
    if response.status_code == 200:
        return response.content.decode('utf-8')#json.loads(response.content.decode('utf-8'))
    else:
        return response.content.decode('utf-8')

def execute(id=None):
    info = get_info(id)
    if info is not None:
        print(info)
        if info == 'execute':
            #response = requests.post(api_url, headers=headers, json=ssh_key)
            #modeltree.generateTreeModels()
            '''
            print("Aqui estão suas informações: ")
            for c in account_info['ngos']:
                print('{0}'.format(c))
            '''
        elif info == 'graph_update':
            get_info(1) #limpa requisição
            updateGraph()
        elif info == 'graph_optimized':
            print('Optimized')
    else:
        print('[!] Solicitação inválida')


def updateGraph():
    from DBConnection import DBConnection
    from DBInitialize import DBInitialize
    from Dao import DAO
    from addVerticeEdgeLists import addSensorList, addFeatureList, addMLModelList, addFinalStateList, addMLAlgorithmList
    from addVerticeEdgeLists import addSensorFeatureList, addFeatureMLModel, addMLModelFinalState
    from Entities import Sensor, Feature, MLModel, FinalState, MLAlgorithm
    from XMLCreate import xml_create
    from ModelANNTensorflow import trainModelAllSensors, trainModelWithOnlyACC
    from ModelDecisionTreeRandomForestSKLearn import trainDecisionTreeModelAllSensors, trainRandomForestModelAllSensors
    from graphFunctions import addToGraph, getGraphValues, optimizeGraph
    import DatabasePreprocessing1 as dbp1

    so = platform.system()
    db = DBInitialize()
    dao = DAO(db.connection_db)

    print("=========Initialize Graph Generate Data from DataBase 1===========")

    algorithName = ["Artificial Neural Network"]
    modelName = ["ANNModel.tflite"]
    modelName2 = ["ANNModel2.tflite"]
    
    algorithName2 = ["Decision Tree"]
    modelName3 = ["sklearn_model_dt.onnx"]
    
    algorithName3 = ["Random Forest"]
    modelName5 = ["sklearn_model_rf.onnx"]
    
    sensorList = [["acc", "accelerometer"], ["gyr","gyroscope"]]
    featureList = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr","gyr_mean", "gyr_max", "gyr_min", "gyr_std", "gyr_kurtosis", "gyr_skewness", "gyr_entropy", "gyr_mad", "gyr_iqr"]
    
    sensorList2 = [["acc", "accelerometer"]]
    featureList2 = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr"]
    
    finalStateList = ['Andar', 'BATER_NA_MESA', 'BATER_PAREDE', 'CORRENDO', 'DEITAR','ESBARRAR_PAREDE', 'ESCREVER', 'PALMAS_EMP', 'PALMAS_SEN', 'PULO','QUEDA_APOIO_FRENTE', 'QUEDA_LATERAL', 'QUEDA_SAPOIO_FRENTE', 'SENTAR', 'SENTAR_APOIO', 'SENTAR_SAPOIO', 'TATEAR']
    preprocessingData = dbp1.executePreproccessing()
    ANNModelAllSensors = trainModelAllSensors(0.75, 1, 10, preprocessingData)
    ANNModelOnlyACC = trainModelWithOnlyACC(0.75, 1, 10, preprocessingData)
    DTModelAllSensors = trainDecisionTreeModelAllSensors(0.75, 10, 1000, preprocessingData)
    #DTModelOnlyACC = trainDecisionTreeModelWithOnlyACC(0.8, 1, 10, preprocessingData)
    RFModelAllSensors = trainRandomForestModelAllSensors(0.75, 10, 1000, preprocessingData)
    #RFModelOnlyACC = trainRandomForestModelWithOnlyACC(0.8, 1, 10, preprocessingData)


    print("=========Generate Graph===========")
    
    #Add Ann Model related Values with All Sensors
    valuesList = getGraphValues(sensorList, featureList, algorithName, modelName, finalStateList, ANNModelAllSensors)[1]
    probability = valuesList[1]
    valuesList = valuesList[0]
    addToGraph(dao, valuesList, probability) 
    
    #Add Ann Model related Values with only Accelerometer
    valuesList2 = getGraphValues(sensorList2, featureList2, algorithName, modelName2, finalStateList, ANNModelOnlyACC)[1]
    probability2 = valuesList2[1]
    valuesList2 = valuesList2[0]
    addToGraph(dao, valuesList2, probability2)
    
    
    #Add Decision Tree Model related Values with All Sensors
    valuesList = getGraphValues(sensorList, featureList, algorithName2, modelName3, finalStateList, DTModelAllSensors)[1]
    probability = valuesList[1]
    valuesList = valuesList[0]
    print(valuesList[1])
    print(valuesList[0])
    addToGraph(dao, valuesList, probability) 
    
    #Add Decision Tree Model related Values with only Accelerometer
    
    #Add Random Forest Model related Values with All Sensors
    valuesList = getGraphValues(sensorList, featureList, algorithName3, modelName5, finalStateList, RFModelAllSensors)[1]
    probability = valuesList[1]
    valuesList = valuesList[0]
    addToGraph(dao, valuesList, probability) 
    
    #Add Random Forest Model related Values with only Accelerometer
    
    print("\n=================\n")

    #for i in range(2,50):
    #    dao.delete("SensorFeature",i)
    edges = dao.includeEdgeList()
    edgeSensorFeatures = edges[0]
    edgeFeatureModels = edges[1] 
    edgeModelFinalStates = edges[2]
    xml_create(edgeSensorFeatures, edgeFeatureModels, edgeModelFinalStates)

#====Teste====
#execute()
if __name__ == "__main__":
    #execute(2) #UpdateGraphRequest
    #execute(0) #UpdateGraphRequest Execute
    ##OptimizeGraphRequest
    updateGraph()
    file = open("download.xml", "w")
    file.write(get_info(3))
    file.close()
    print("optimized")
    file = open("download_.xml", "w")
    file.write(get_info(4))
    file.close()
    print("optimized2")
    
