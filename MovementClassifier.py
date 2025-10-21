import joblib
import numpy as np
import os


class MovementPredictor:
    def __init__(self, model_type='acc_gyr'):
        """
        Initialize predictor with specified model type
        :param model_type: 'acc' or 'acc_gyr'
        """
        self.model_type = model_type
        self.model = None
        self.class_names = []

        # Define model paths
        model_dir = 'models'
        if model_type == 'acc':
            model_path = os.path.join(model_dir, 'acc_model.joblib')
        else:
            model_path = os.path.join(model_dir, 'acc_gyr_model.joblib')

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {os.path.abspath(model_path)}\n"
                "Please train models first by running ModelTrainer.py"
            )

        model_data = joblib.load(model_path)
        self.model = model_data['model']
        self.class_names = model_data['class_names']
        print(f"Loaded {model_type} model from {os.path.abspath(model_path)}")

    def _process_test_file(self, file_path):
        """Process the test file and extract features"""
        from Dataset1 import Dataset1

        # Create closure to capture model_type
        model_type = self.model_type

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

                                    # Use the captured model_type from outer scope
                                    if model_type == 'acc' and sensor_type == "ACC":
                                        x = float(parts[1])
                                        y = float(parts[2])
                                        z = float(parts[3])
                                        arr = np.vstack([arr, [x, y, z, sensor_type, "Unknown"]])
                                    elif model_type == 'acc_gyr':
                                        x = float(parts[1])
                                        y = float(parts[2])
                                        z = float(parts[3])
                                        arr = np.vstack([arr, [x, y, z, sensor_type, "Unknown"]])
                                except (ValueError, IndexError):
                                    continue
                arr = np.delete(arr, (0), axis=0)
                return [arr] if len(arr) > 0 else []

        temp_dataset = TempDataset(file_path)
        arr_list = temp_dataset.feature_extract_dataset()

        if not arr_list:
            raise ValueError(f"No valid {self.model_type} data found in test file")

        if self.model_type == 'acc':
            from DatasetACC import DatasetACC
            feature_extractor = DatasetACC([])
            return feature_extractor.feature_extraction_acc(arr_list[0])
        else:
            from DatasetACC_GYR import DatasetACC_GYR
            feature_extractor = DatasetACC_GYR([])
            return feature_extractor.feature_extraction_acc_gyr(arr_list[0])

    def predict(self, test_file_path):
        """
        Predict movement from test file
        :return: tuple (movement_name, confidence)
        """
        if not os.path.exists(test_file_path):
            raise FileNotFoundError(f"Test file not found: {test_file_path}")

        # Extract features
        features = self._process_test_file(test_file_path)

        # Prepare feature vector
        X_test = np.array([features[:-1]])  # Remove movement label

        # Predict
        pred = self.model.predict(X_test)
        proba = self.model.predict_proba(X_test)

        return self.class_names[pred[0]], np.max(proba)


if __name__ == "__main__":
    # Example 1: Predict using ACC+GYR model (default)
    try:
        print("\nUsing ACC+GYR model:")
        predictor_acc_gyr = MovementPredictor(model_type='acc_gyr')
        movement, confidence = predictor_acc_gyr.predict("teste.txt")
        print(f"Movement: {movement} (confidence: {confidence:.1%})")
    except Exception as e:
        print(f"ACC+GYR prediction error: {e}")

    # Example 2: Predict using ACC-only model
    try:
        print("\nUsing ACC-only model:")
        predictor_acc = MovementPredictor(model_type='acc')
        movement, confidence = predictor_acc.predict("teste.txt")
        print(f"Movement: {movement} (confidence: {confidence:.1%})")
    except Exception as e:
        print(f"ACC prediction error: {e}")