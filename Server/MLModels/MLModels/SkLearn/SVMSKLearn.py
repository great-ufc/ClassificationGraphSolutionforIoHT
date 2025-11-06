import joblib
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from Utilitarios import Constants

pathProjectSaveModels = Constants.pathProjectSaveModels


class ModelTrainer:
    def __init__(self):
        """Initialize the multi-model trainer"""
        self.acc_model = None
        self.acc_gyr_model = None
        self.acc_class_names = []
        self.acc_gyr_class_names = []

        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)

    def train_modelACC(self, threshold, testMin, testMax, preprocessingData, finalStates):
        """
        Train both ACC and ACC+GYR models
        :param dataset_paths: list of paths to training datasets
        """
        # Train ACC-only model
        result = self._train_acc_model(threshold, testMin, testMax, preprocessingData, finalStates)
        self.save_modelsACC()
        return result

    def train_modelACCGYR(self, threshold, testMin, testMax, preprocessingData, finalStates):
        """
        Train both ACC and ACC+GYR models
        :param dataset_paths: list of paths to training datasets
        """

        # Train ACC+GYR model (only uses Dataset1)
        result = self._train_acc_gyr_model(threshold, testMin, testMax, preprocessingData, finalStates)
        self.save_modelsACCGYR()
        return result


    def _train_acc_model(self, threshold, testMin, testMax, preprocessingData, finalStates):
        """Train model using only accelerometer data"""
        labelTrain, labelTest, X_train, DataSetTest = preprocessingData
        self.acc_class_names = finalStates

        cont = 0
        valueAccuracy = 0
        resultModel = None
        while cont < testMin or (valueAccuracy < threshold and cont < testMax):
            self.acc_model = make_pipeline(
                StandardScaler(),
                SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
            )
            self.acc_model.fit(X_train, labelTrain)

            result = []
            for mndst in  DataSetTest:
                result.append(self.acc_model.predict([mndst]))

            qtd = 0
            for i in range(len(labelTest)):
                if result[i] == labelTest[i]:
                    qtd += 1
                
            if valueAccuracy < qtd/len(labelTest):
                valueAccuracy = qtd/len(labelTest)
                resultModel = self.acc_model
            cont+=1
        print("ACC-only model training completed")
        print(round(valueAccuracy,2))
        return [resultModel,valueAccuracy]

    def _train_acc_gyr_model(self, threshold, testMin, testMax, preprocessingData, finalStates):
        """Train model using both accelerometer and gyroscope data"""

        labelTrain, labelTest, X_train, DataSetTest = preprocessingData
        self.acc_gyr_class_names = finalStates

        cont = 0
        valueAccuracy = 0
        resultModel = None
        while cont < testMin or (valueAccuracy < threshold and cont < testMax):
            self.acc_gyr_model = make_pipeline(
                StandardScaler(),
                SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
            )
            self.acc_gyr_model.fit(X_train, labelTrain)

            result = []
            for mndst in  DataSetTest:
                result.append(self.acc_gyr_model.predict([mndst]))

            qtd = 0
            for i in range(len(labelTest)):
                if result[i] == labelTest[i]:
                    qtd += 1
                
            if valueAccuracy < qtd/len(labelTest):
                valueAccuracy = qtd/len(labelTest)
                resultModel = self.acc_gyr_model
            cont+=1    
            
        print("ACC+GYR model training completed")
        print(round(valueAccuracy,2))
        return [resultModel,valueAccuracy]

    def save_modelsACC(self):
        """
        Save both trained models to the 'models' directory
        """

        if self.acc_model:
            acc_path = pathProjectSaveModels + '\\SVM' + '\\acc_model.joblib'
            joblib.dump({
                'model': self.acc_model,
                'class_names': self.acc_class_names,
                'sensor_type': 'acc'
            }, acc_path)
            print(f"ACC model saved to {acc_path}")

        
    def save_modelsACCGYR(self):
        """
        Save both trained models to the 'models' directory
        """

        if self.acc_gyr_model:
            acc_gyr_path = pathProjectSaveModels + '\\SVM' + '\\acc_gyr_model.joblib'
            joblib.dump({
                'model': self.acc_gyr_model,
                'class_names': self.acc_gyr_class_names,
                'sensor_type': 'acc_gyr'
            }, acc_gyr_path)
            print(f"ACC+GYR model saved to {acc_gyr_path}")
