from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np
import os


class MovementClassifier:
    def __init__(self, sensor_type='acc_gyr'):
        self.sensor_type = sensor_type
        self.model = None
        self.class_names = []

    def train(self, dataset_paths):
        if self.sensor_type == 'acc':
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
            self.class_names = DatasetACC.returnFinalStates()

        elif self.sensor_type == 'acc_gyr':
            from DatasetACC_GYR import DatasetACC_GYR
            from Dataset1 import Dataset1

            datasets = [Dataset1(path) for path in dataset_paths if 'Dataset1' in path]
            feature_extractor = DatasetACC_GYR(datasets)
            labelTrain, _, X_train, _ = feature_extractor.executePreprocessing()
            self.class_names = DatasetACC_GYR.returnFinalStates()

        self.model = make_pipeline(
            StandardScaler(),
            SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
        )
        self.model.fit(X_train, labelTrain)

    def _extract_features_from_file(self, file_path):
        from Dataset1 import Dataset1

        class TempDataset(Dataset1):
            def feature_extract_dataset(self):
                arr = np.array([[0.0, 0.0, 0.0, "", "Unknown"]])
                with open(self.path, 'r') as f:
                    for line in f:
                        if ',' in line:  # Skip timestamp lines
                            parts = line.strip().split(',')
                            if len(parts) >= 5:
                                try:
                                    sensor_id = int(parts[4])
                                    sensor_type = "ACC" if sensor_id == 1 else "GYR"
                                    x = float(parts[1])
                                    y = float(parts[2])
                                    z = float(parts[3])
                                    arr = np.vstack([arr, [x, y, z, sensor_type, "Unknown"]])
                                except (ValueError, IndexError):
                                    continue
                arr = np.delete(arr, (0), axis=0)
                return [arr] if len(arr) > 0 else []

        temp_dataset = TempDataset(file_path)

        if self.sensor_type == 'acc':
            from DatasetACC import DatasetACC
            feature_extractor = DatasetACC([temp_dataset])
            arr_list = temp_dataset.feature_extract_dataset()
            if not arr_list:
                raise ValueError("No valid data found in test file")
            return feature_extractor.feature_extraction_acc(arr_list[0])
        else:
            from DatasetACC_GYR import DatasetACC_GYR
            feature_extractor = DatasetACC_GYR([temp_dataset])
            arr_list = temp_dataset.feature_extract_dataset()
            if not arr_list:
                raise ValueError("No valid data found in test file")
            return feature_extractor.feature_extraction_acc_gyr(arr_list[0])

    def predict_movement(self, test_file_path):
        if not os.path.exists(test_file_path):
            raise FileNotFoundError(f"File not found: {test_file_path}")


        features = self._extract_features_from_file(test_file_path)


        if self.sensor_type == 'acc':
            X_test = np.array([features[:-1]])
        else:
            X_test = np.array([features[:-1]])

        # Predict
        pred = self.model.predict(X_test)
        proba = self.model.predict_proba(X_test)

        return self.class_names[pred[0]], np.max(proba)



if __name__ == "__main__":
    try:

        classifier = MovementClassifier(sensor_type='acc_gyr')


        dataset_paths = [
            "Datasets/Dataset1",  # Contains both ACC and GYR
            # "Datasets/D2_ADL_Dataset/HMP_Dataset/All_data"  # Only ACC, skip for acc_gyr mode
        ]
        classifier.train(dataset_paths)


        test_file = "teste1.txt"
        movement, confidence = classifier.predict_movement(test_file)
        print(f"Predicted movement: {movement} (confidence: {confidence:.2%})")

    except Exception as e:
        print(f"Error: {e}")