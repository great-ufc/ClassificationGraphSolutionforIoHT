import os

'''trainModelsFunctions'''

def trainModelWithOnlyACC(threshold, numMin, numMax,preprocessingData):
    import tensorflow.compat.v2.feature_column as fc
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import optimizers
    from os.path import join
    from pathlib import Path
    
    """**ANN Modeling**"""
    labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest = preprocessingData
    
    ##cria e compila o modelo da rede neural

    model = keras.Sequential([
        keras.layers.Dense(9),  # input layer (1)
        keras.layers.Dense(120, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(120, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(30, activation='softmax') # output layer (3)
    ])
    
    ##Treina o modelo
    cont = 0
    valueAccuracy = 0
    resultModel = None
    while cont < numMin or (valueAccuracy < threshold and cont < numMax):
        model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        model.fit(MyNewDataSetTrain, labelTrain, epochs=300)  # we pass the data, labels and epochs and watch the magic!

        ##Avalia o modelo
        test_loss, test_acc = model.evaluate(MyNewDataSetTest,  labelTest, verbose=1)
        if valueAccuracy < test_acc:
            valueAccuracy = test_acc
            resultModel = model
        cont+=1
    
    ##Avalia o modelo
    #test_loss, test_acc = model.evaluate(MyNewDataSetTest,  labelTest, verbose=1)

    print('Test accuracy:', test_acc)

    """**Export Model**"""

    tms_model = resultModel.save('saved_model/my_model_')

    """**Load Model**"""

    #path = os.path.join('saved_model/my_model_')
    #loaded = tf.keras.models.load_model(path)


    #print('Test accuracy:', test_acc)


    """**Generate Model Trained File**"""
          
    ##pip install -q tflite_support
    ##**Transfort to Tensorflow lite model**

    _TFLITE_MODEL_PATH = "saved_model/"+"ANNModel2.tflite"

    converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model_')
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()


    with open(_TFLITE_MODEL_PATH, 'wb') as f:
      f.write(tflite_model)

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath('saved_model')
    tflite_model_file = dataset_dir.joinpath("ANNModel2.tflite"+'32')
    tflite_model_file.write_bytes(tflite_model)

    converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model_')
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath('saved_model')
    tflite_model_file = dataset_dir.joinpath("ANNModel2.tflite"+'16')
    tflite_model_file.write_bytes(tflite_model)
    
    return [resultModel,valueAccuracy]
    

def trainModelWithACCGYR(threshold, numMin, numMax,preprocessingData):
    import tensorflow.compat.v2.feature_column as fc
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import optimizers
    from os.path import join
    from pathlib import Path

    """**ANN Modeling**"""

    labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest = preprocessingData

    ##cria e compila o modelo da rede neural

    model = keras.Sequential([
        keras.layers.Dense(18),  # input layer (1)
        keras.layers.Dense(120, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(120, activation='relu'),  # hidden layer (2)
        keras.layers.Dense(17, activation='softmax') # output layer (3)
    ])

    ##Treina o modelo
    cont = 0
    valueAccuracy = 0
    resultModel = None
    while cont < numMin or (valueAccuracy < threshold and cont < numMax):
        model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        model.fit(MyNewDataSetTrain, labelTrain, epochs=300)  # we pass the data, labels and epochs and watch the magic!

        ##Avalia o modelo
        test_loss, test_acc = model.evaluate(MyNewDataSetTest,  labelTest, verbose=1)
        if valueAccuracy < test_acc:
            valueAccuracy = test_acc
            resultModel = model
        cont+=1

    print('Test accuracy:', valueAccuracy)

    """**Export Model**"""

    tms_model = resultModel.save('saved_model/my_model')

    """**Generate Model Trained File**"""
          
    ##pip install -q tflite_support
    ##**Transfort to Tensorflow lite model**

    _TFLITE_MODEL_PATH = "saved_model/"+"ANNModel.tflite"

    converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model')
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()


    with open(_TFLITE_MODEL_PATH, 'wb') as f:
      f.write(tflite_model)

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath('saved_model')
    tflite_model_file = dataset_dir.joinpath("ANNModel.tflite"+'32')
    tflite_model_file.write_bytes(tflite_model)

    converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model')
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath('saved_model')
    tflite_model_file = dataset_dir.joinpath("ANNModel.tflite"+'16')
    tflite_model_file.write_bytes(tflite_model)
    
    return [resultModel,valueAccuracy]



'''Predict'''
    
def predict(model, classes, correct_label):
  import numpy as np
  
  class_names = ['Andar', 'BATER_NA_MESA', 'BATER_PAREDE', 'CORRENDO', 'DEITAR', 'ESBARRAR_PAREDE', 'ESCREVER', 'PALMAS_EMP', 'PALMAS_SEN', 'PULO','QUEDA_APOIO_FRENTE', 'QUEDA_LATERAL', 'QUEDA_SAPOIO_FRENTE', 'SENTAR', 'SENTAR_APOIO', 'SENTAR_SAPOIO', 'TATEAR' ]
  
  prediction = model.predict(np.array([classes]))
  predicted_class = class_names[np.argmax(prediction)]
  print(class_names[correct_label])
  print(predicted_class)

def get_number():
  while True:
    num = input("Pick a number: ")
    if num.isdigit():
      num = int(num)
      if 0 <= num <= 1000:
        return int(num)
    else:
      print("Try again...")

if __name__ == '__main__':
    from Dataset1 import Dataset1
    from Dataset2 import Dataset2
    from DatasetACC import DatasetACC
    from DatasetACC_GYR import DatasetACC_GYR
    print("====Preprocessing====")
    dt1 = Dataset1("Datasets/Dataset1")
    dt2 = Dataset2("Datasets/D2_ADL_Dataset/HMP_Dataset/All_data")
    dtACC = DatasetACC([dt1,dt2])
    dtACCGYR = DatasetACC_GYR([dt1])
    ppDataACC = dtACC.executePreprocessing()
    ppDataACCGYR = dtACCGYR.executePreprocessing()
    print("====Training====")
    modelGenerated2 = trainModelWithOnlyACC(0.7, 1, 10, ppDataACC)
    modelGenerated = trainModelWithACCGYR(0.7, 1, 10, ppDataACCGYR)
    

    print("=========Initialize Graph Generate Data===========")
    algorithName = ["Artificial Neural Network"]
    modelName = ["ANNModel.tflite"]
    sensorList = [["acc", "accelerometer"], ["gyr","gyroscope"]]
    featureList = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr","gyr_mean", "gyr_max", "gyr_min", "gyr_std", "gyr_kurtosis", "gyr_skewness", "gyr_entropy", "gyr_mad", "gyr_iqr"]
    modelName2 = ["ANNModel2.tflite"]
    sensorList2 = [["acc", "accelerometer"]]
    featureList2 = ["acc_mean", "acc_max", "acc_min", "acc_std", "acc_kurtosis", "acc_skewness", "acc_entropy", "acc_mad", "acc_iqr"]
    finalStateList = ['Andar', 'BATER_NA_MESA', 'BATER_PAREDE', 'CORRENDO', 'DEITAR','ESBARRAR_PAREDE', 'ESCREVER', 'PALMAS_EMP', 'PALMAS_SEN', 'PULO','QUEDA_APOIO_FRENTE', 'QUEDA_LATERAL', 'QUEDA_SAPOIO_FRENTE', 'SENTAR', 'SENTAR_APOIO', 'SENTAR_SAPOIO', 'TATEAR']


    print("=========Predict===========")
    labelTrain = ppDataACC[0]
    labelTest = ppDataACC[1]
    MyNewDataSetTrain = ppDataACC[2]
    MyNewDataSetTest = ppDataACC[3]
    
    while True:
        num = get_number()
        if num > 37:
            break 
        classes = MyNewDataSetTest[num]
        label = labelTest[num]
        predict(modelGenerated2[0], classes, label)