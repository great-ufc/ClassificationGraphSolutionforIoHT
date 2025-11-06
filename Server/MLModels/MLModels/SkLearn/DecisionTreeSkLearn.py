import pandas as pd
import numpy as np 
import scipy
from six.moves import urllib
from scipy import stats ##statistic functions
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import subprocess
import os
import platform
from Utilitarios import Constants
pathProjectSaveModels = Constants.pathProjectSaveModels

def trainDecisionTreeModelAccGyr(threshold, testMin, testMax, preprocessingData):
    
    print("===ACC Decision Tree===")
    labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest = preprocessingData
    
    from sklearn import tree
    X, y = MyNewDataSetTrain, labelTrain
    
    cont = 0
    valueAccuracy = 0
    resultModel = None
    while cont < testMin or (valueAccuracy < threshold and cont < testMax) :
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
        tree.plot_tree(clf)

        result = []
        for mndst in  MyNewDataSetTest:
          result.append(clf.predict([mndst]))

        qtd = 0
        for i in range(len(labelTest)):
          if result[i] == labelTest[i]:
            qtd += 1
        
        if valueAccuracy < qtd/len(labelTest):
            valueAccuracy = qtd/len(labelTest)
            resultModel = clf
        cont+=1
   
    print(round(valueAccuracy,2))
    
    print("==== Deision Tree Model Save ====")
    # Specify an initial type for the model ( similar to input shape for the model )
    initial_type = [ 
        ( 'input_study_hours' , FloatTensorType( [None,1] ) ) 
    ]

    # Write the ONNX model to disk
    converted_model = convert_sklearn(resultModel , initial_types=initial_type )
    with open( "sklearn_model_dt.onnx", "wb" ) as f:
        f.write( converted_model.SerializeToString() )

    
    cmd = ['python', '-m', 'onnxruntime.tools.convert_onnx_models_to_ort', 'sklearn_model_dt.onnx']
    shell_cmd = subprocess.run((cmd), capture_output=True, text=True)
    command_output=(shell_cmd.stdout)
    
    so = platform.system()
    if so == "Windows":
        os.system('copy sklearn_model_dt.onnx '+pathProjectSaveModels+'\\DecisionTree')
        os.system('del sklearn_model_dt.onnx')
        os.system('copy sklearn_model_dt.ort '+pathProjectSaveModels+'\\DecisionTree')
        os.system('del sklearn_model_dt.ort')
    if so == "Linux":
        os.system('mv sklearn_model_dt.onnx '+pathProjectSaveModels+'\\DecisionTree')
        
    print(valueAccuracy)
    return [resultModel,valueAccuracy]

def trainDecisionTreeModelAcc(threshold, testMin, testMax, preprocessingData):
    
    print("===ACC Decision Tree===")
    labelTrain, labelTest, MyNewDataSetTrain, MyNewDataSetTest = preprocessingData
    
    from sklearn import tree
    X, y = MyNewDataSetTrain, labelTrain
    
    cont = 0
    valueAccuracy = 0
    resultModel = None
    while cont < testMin or (valueAccuracy < threshold and cont < testMax) :
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, y)
        tree.plot_tree(clf)

        result = []
        for mndst in  MyNewDataSetTest:
          result.append(clf.predict([mndst]))

        qtd = 0
        for i in range(len(labelTest)):
          if result[i] == labelTest[i]:
            qtd += 1
        
        if valueAccuracy < qtd/len(labelTest):
            valueAccuracy = qtd/len(labelTest)
            resultModel = clf
        cont+=1
   
    print(round(valueAccuracy,2))
    
    print("==== Deision Tree Model Save ====")
    # Specify an initial type for the model ( similar to input shape for the model )
    initial_type = [ 
        ( 'input_study_hours' , FloatTensorType( [None,1] ) ) 
    ]

    # Write the ONNX model to disk
    converted_model = convert_sklearn(resultModel , initial_types=initial_type )
    with open( "sklearn_model_dt2.onnx", "wb" ) as f:
        f.write( converted_model.SerializeToString() )

    
    cmd = ['python', '-m', 'onnxruntime.tools.convert_onnx_models_to_ort', 'sklearn_model_dt2.onnx']
    shell_cmd = subprocess.run((cmd), capture_output=True, text=True)
    command_output=(shell_cmd.stdout)
    
    so = platform.system()
    if so == "Windows":
        os.system('copy sklearn_model_dt2.onnx '+pathProjectSaveModels+'\\DecisionTree')
        os.system('del sklearn_model_dt2.onnx')
        os.system('copy sklearn_model_dt2.ort '+pathProjectSaveModels+'\\DecisionTree')
        os.system('del sklearn_model_dt2.ort')
    if so == "Linux":
        os.system('mv sklearn_model_dt2.onnx '+pathProjectSaveModels+'\\DecisionTree')
        
    print(valueAccuracy)
    return [resultModel,valueAccuracy]
