import os
from Utilitarios import Constants

'''trainModelsFunctions'''

def trainModelWithOnlyACC(threshold, numMin, numMax,preprocessingData):
    import tensorflow as tf
    from tensorflow import keras
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
    pathModel = Constants.pathProjectSaveModels+ "\\ANN\\"
    saved_model = pathModel +'LastANNModelACC'
    resultModel.export(saved_model)

    """**Load Model**"""

    #path = os.path.join('saved_model/my_model_')
    #loaded = tf.keras.models.load_model(path)


    #print('Test accuracy:', test_acc)


    """**Generate Model Trained File**"""
          
    ##pip install -q tflite_support
    ##**Transfort to Tensorflow lite model**

    _TFLITE_MODEL_PATH = pathModel+"LastANNModeACC.tflite"

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()


    with open(_TFLITE_MODEL_PATH, 'wb') as f:
      f.write(tflite_model)

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath(pathModel)
    tflite_model_file = dataset_dir.joinpath("LastANNModelACC.tflite"+'32')
    tflite_model_file.write_bytes(tflite_model)

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath(pathModel)
    tflite_model_file = dataset_dir.joinpath("LastANNModelACC.tflite"+'16')
    tflite_model_file.write_bytes(tflite_model)
    
    return [resultModel,valueAccuracy]
    

def trainModelWithACCGYR(threshold, numMin, numMax,preprocessingData):
    import tensorflow as tf
    from tensorflow import keras
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

    pathModel = Constants.pathProjectSaveModels+ "\\ANN\\"
    saved_model = pathModel +'LastANNModelALL'
    resultModel.export(saved_model)
    """**Generate Model Trained File**"""
          
    ##pip install -q tflite_support
    ##**Transfort to Tensorflow lite model**

    _TFLITE_MODEL_PATH = pathModel+"LastANNModelAll.tflite"

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()


    with open(_TFLITE_MODEL_PATH, 'wb') as f:
      f.write(tflite_model)

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath(pathModel)
    tflite_model_file = dataset_dir.joinpath("LastANNModelAll.tflite"+'32')
    tflite_model_file.write_bytes(tflite_model)

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    PATH_DIR = Path.cwd()
    dataset_dir = PATH_DIR.joinpath(pathModel)
    tflite_model_file = dataset_dir.joinpath("LastANNModelAll.tflite"+'16')
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
