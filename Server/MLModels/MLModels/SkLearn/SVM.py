import joblib
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


class ModelTrainer:
    def __init__(self):
        """Initialize the multi-model trainer"""
        self.acc_model = None
        self.acc_gyr_model = None
        self.acc_class_names = []
        self.acc_gyr_class_names = []

        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)

    def train_models(self, dataset_paths):
        """
        Train both ACC and ACC+GYR models
        :param dataset_paths: list of paths to training datasets
        """
        # Train ACC-only model
        self._train_acc_model(dataset_paths)

        # Train ACC+GYR model (only uses Dataset1)
        self._train_acc_gyr_model([p for p in dataset_paths if 'Dataset1' in p])

    def _train_acc_model(self, dataset_paths):
        """Train model using only accelerometer data"""
        from DatasetACC import DatasetACC
        from Dataset1 import Dataset1
        from Dataset2 import Dataset2

        datasets = []
        for path in dataset_paths:
            if 'Dataset1' in path:
                datasets.append(Dataset1(path))
            elif 'Dataset2' in path:
                datasets.append(Dataset2(path))

        feature_extractor = DatasetACC(datasets)
        labelTrain, _, X_train, _ = feature_extractor.executePreprocessing()
        self.acc_class_names = DatasetACC.returnFinalStates()

        self.acc_model = make_pipeline(
            StandardScaler(),
            SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
        )
        self.acc_model.fit(X_train, labelTrain)
        print("ACC-only model training completed")

    def _train_acc_gyr_model(self, dataset_paths):
        """Train model using both accelerometer and gyroscope data"""
        if not dataset_paths:
            print("Skipping ACC+GYR model - no Dataset1 paths provided")
            return

        from DatasetACC_GYR import DatasetACC_GYR
        from Dataset1 import Dataset1

        datasets = [Dataset1(path) for path in dataset_paths]
        feature_extractor = DatasetACC_GYR(datasets)
        labelTrain, _, X_train, _ = feature_extractor.executePreprocessing()
        self.acc_gyr_class_names = DatasetACC_GYR.returnFinalStates()

        self.acc_gyr_model = make_pipeline(
            StandardScaler(),
            SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
        )
        self.acc_gyr_model.fit(X_train, labelTrain)
        print("ACC+GYR model training completed")

    def save_models(self):
        """
        Save both trained models to the 'models' directory
        """
        if not os.path.exists('models'):
            os.makedirs('models')

        if self.acc_model:
            acc_path = os.path.join('models', 'acc_model.joblib')
            joblib.dump({
                'model': self.acc_model,
                'class_names': self.acc_class_names,
                'sensor_type': 'acc'
            }, acc_path)
            print(f"ACC model saved to {os.path.abspath(acc_path)}")

        if self.acc_gyr_model:
            acc_gyr_path = os.path.join('models', 'acc_gyr_model.joblib')
            joblib.dump({
                'model': self.acc_gyr_model,
                'class_names': self.acc_gyr_class_names,
                'sensor_type': 'acc_gyr'
            }, acc_gyr_path)
            print(f"ACC+GYR model saved to {os.path.abspath(acc_gyr_path)}")


# Example usage for training:
if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_models([
        "Datasets/Dataset1",  # Contains both ACC and GYR
        "Datasets/D2_ADL_Dataset/HMP_Dataset/All_data"  # Contains only ACC
    ])
    trainer.save_models()