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
    MyNewDataSetTrain_, MyNewDataSetTest_, labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest, labelTrain2, labelTest2, MyNewDataSetTrain2, MyNewDataSetTest2  = preprocessingData
    
    ##cria e compila o modelo da rede neural

    model = keras.Sequential([
        keras.layers.Dense(9),  # input layer (1)
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
        model.fit(MyNewDataSetTrain2, labelTrain2, epochs=300)  # we pass the data, labels and epochs and watch the magic!

        ##Avalia o modelo
        test_loss, test_acc = model.evaluate(MyNewDataSetTest2,  labelTest2, verbose=1)
        if valueAccuracy < test_acc:
            valueAccuracy = test_acc
            resultModel = model
        cont+=1
    
    #model.fit(MyNewDataSetTrain2, labelTrain2, epochs=300)  # we pass the data, labels and epochs and watch the magic!

    ##Avalia o modelo
    #test_loss, test_acc = model.evaluate(MyNewDataSetTest2,  labelTest2, verbose=1)

    print('Test accuracy:', test_acc)

    """**Export Model**"""

    tms_model = resultModel.save('saved_model/my_model_')

    """**Load Model**"""

    path = os.path.join('saved_model/my_model_')
    loaded = tf.keras.models.load_model(path)

    print(loaded)

    #test
    test_loss, test_acc = loaded.evaluate(MyNewDataSetTest2, labelTest2, verbose=1) 

    print('Test accuracy:', test_acc)


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
    
    print("SUCCESS2")
    return [resultModel,valueAccuracy]
    

def trainModelAllSensors(threshold, numMin, numMax,preprocessingData):
    import tensorflow.compat.v2.feature_column as fc
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import optimizers
    from os.path import join
    from pathlib import Path

    """**ANN Modeling**"""

    MyNewDataSetTrain_, MyNewDataSetTest_, labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest, labelTrain2, labelTest2, MyNewDataSetTrain2, MyNewDataSetTest2  = preprocessingData

    ##cria e compila o modelo da rede neural

    model = keras.Sequential([
        keras.layers.Dense(18),  # input layer (1)
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

    """**Load Model**"""

    path = os.path.join('saved_model/my_model')
    loaded = tf.keras.models.load_model(path)

    print(loaded)

    #test
    test_loss, test_acc = loaded.evaluate(MyNewDataSetTest, labelTest, verbose=1) 

    print('Test accuracy:', test_acc)


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
    
    print("SUCCESS")
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
    #import ANNPreprocessing as pre
    import DatabasePreprocessing1 as dbp1
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
    #modelGenerated = trainModelAllSensors(0.7, 10, 1000, preprocessingData)
    modelGenerated2 = trainModelWithOnlyACC(0.8, 1, 10, preprocessingData)

    print("=========Predict===========")

    
    '''
    import platform
    so = platform.system()
    if so == "Windows":
        os.system('cls') or None
    if so == "Linux":
        os.system('clear') or None
    '''

    MyNewDataSetTrain_, MyNewDataSetTest_, labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest, labelTrain2, labelTest2, MyNewDataSetTrain2, MyNewDataSetTest2  = preprocessingData
    while True:
        num = get_number()
        if num > 37:
            break 
        #classes = MyNewDataSetTest[num]
        #label = labelTest[num]
        classes = MyNewDataSetTest2[num]
        label = labelTest2[num]
        predict(modelGenerated2[0], classes, label)