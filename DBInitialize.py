from DatabaseQueryFunctions import create_table
from DatabaseQueryFunctions import drop_table
from DatabaseQueryFunctions import add_Column
from DatabaseQueryFunctions import update_Column
from DatabaseQueryFunctions import drop_Column
from DBScheme import DBScheme
from DBConnection import DBConnection
from Entities import Sensor, Feature, MLModel, FinalState, MLAlgorithm
from Dao import DAO

class DBInitialize:
    def __init__(self):
        dbconn = DBConnection()
        dbconn.connnectToDB()
        self.connection_db = dbconn.connection_db
        self.initDb()
    
    def initDb(self):
        self.create_tables(self.connection_db)
        self.insertSensorEntries()
        self.insertFeatureEntries()
        self.insertMLModelsEntries()
        self.insertFinalStateEntries()
        self.insertMLAlgorithmEntries()
        #self.insertSensorFeatureEntries()
        #self.insertFeatureMLModelEntries()
        #self.insertMLModelFinalStateEntries()
	
    def create_tables(self, connection_db):
        entities = [Sensor, Feature, MLModel, FinalState, MLAlgorithm]
        dbScheme = DBScheme(self.connection_db)
        try:
            #Entity tables
            for entity in entities:
                dbScheme.createTableByEntity(entity)
            #Other tables
            colunms = []
            colunms.append(['Sensor_id', 'int', True])
            colunms.append(['Feature_id', 'int', True])
            create_table (self.connection_db, "SensorFeature", colunms)
            colunms = []
            colunms.append(['Feature_id', 'int', True])
            colunms.append(['MLModel_id', 'int', True])
            create_table (self.connection_db, "FeatureMLModel", colunms)
            colunms = []
            colunms.append(['Feature_id', 'int', True])
            colunms.append(['FinalState_id', 'int', True])
            colunms.append(['value', 'float', False])
            create_table (self.connection_db, "FeatureValueFinalState", colunms)
            colunms = []
            colunms.append(['MLModel_id', 'int', True])
            colunms.append(['FinalState_id', 'int', True])
            colunms.append(['probability', 'float', False])
            create_table (self.connection_db, "MLModelFinalState", colunms)
        except Error as err:
            print(f"Error: '{err}'")
    
    #Sensor    
    def insertSensorEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("Sensor")) == 0:
            sensors = []
            acc = Sensor()
            acc.Sensor_id = 1
            acc.typeSensor = "acc"
            acc.sensorName = "accelerometer"
            sensors.append(acc)
            for s in sensors:
                dao.add("Sensor", s)
    
    #Feature, MLModel, FinalState, MLAlgorithm
    def insertFeatureEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("Feature")) == 0:
            features = []
            acc_mean = Feature()
            acc_mean.Feature_id = 1
            acc_mean.featureName = "acc_mean"
            features.append(acc_mean)
            for f in features:
                dao.add("Feature", f)
    
    #MLModel
    def insertMLModelsEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("MLModel")) == 0:
            mlmodels = []
            annmodel = MLModel()
            annmodel.MLModel_id = 1
            annmodel.MLAlgorihtm_id = 1
            annmodel.titleModel = "ANNModel"
            annmodel.modelExtension = ".tflite"
            annmodel.numInFeature = 18
            annmodel.numOutFeature = 17
            mlmodels.append(annmodel)
            for mlm in mlmodels:
                dao.add("MLModel", mlm)
    
    #FinalState
    def insertFinalStateEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("FinalState")) == 0:
            finalstates = []
            normalWalking = FinalState()
            normalWalking.FinalState_id = 1
            normalWalking.description = "Normal Walking"
            normalWalking.hasAnyHealthConditionAssociated = 0
            normalWalking.healthConditionsAssociated = ""
            finalstates.append(normalWalking)
            for fs in finalstates:
                dao.add("FinalState", fs)
    
    #MLAlgorithm
    def insertMLAlgorithmEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("MLAlgorithm")) == 0:
            mlalgorithms = []
            ann = MLAlgorithm()
            ann.MLAlgorithm_id = 1
            ann.mlAlgorithmName = "Artificial Neural Network"
            mlalgorithms.append(ann)
            for ma in mlalgorithms:
                dao.add("MLAlgorithm", ma)
    '''
    #SensorFeature    
    def insertSensorFeatureEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("SensorFeature")) == 0:
            dao.addNE("SensorFeature", {'Sensor_id':1,'Feature_id':1})
    
    #FeatureMLModel
    def insertFeatureMLModelEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("FeatureMLModel")) == 0:
            dao.addNE("FeatureMLModel", {'Feature_id': 1, 'MLModel_id': 1})

    #MLModelFinalState
    def insertMLModelFinalStateEntries(self):
        dao = DAO(self.connection_db)
        if len(dao.findAllRecords("MLModelFinalState")) == 0:
            dao.addNE("MLModelFinalState", {'MLModel_id': 1, 'FinalState_id': 1})
    '''