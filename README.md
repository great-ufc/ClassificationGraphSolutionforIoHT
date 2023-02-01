# Classification Graph Solution for IoHT
Solution to create a Classification Graph using Cloud  for Internet of Health Applications from Evilasio Junior Research

# Setup

Download this full repository

To add new Datasets:
 - Add the new Dataset in the Datasets directory
 - Create code for preprocessing following the pattern of DatabasePreprocessing*.py files
 - Modify the updateGraph() ServerProcessAPI.py method to use preprocessing data from the added dataset

# Initilizing steps

Run the following command to run the flask Web API on server port 3000:
 - flask run --host=0.0.0.0 --port=3000 &

Modify the ServerProcessAPI.py file to read the correct endpoint of your web API (e.g., api_url_base = '<_API address_>:3000')

Run "python MainServer.py" to run the server constant process or "python ServerProcessAPI.py" to test the web API

# Endpoints da api

Informs the API that the graph must be updated:
- <_API address_>:3000/UpdateGraphRequest/2

Download the last updated complete graph:
- <_API address_>:3000/GraphRequest

Download the last generated optimized graph:
- <_API address_>:3000/OptimizeGraphRequest/download.xml

Request for optimization and download of the graph optimized by the application:
- <_API address_>:3000/OptimizeGraphRequest/<_All types of sensors used by the application separated by an underscore_>
or
- <_API address_>:3000/OptimizeGraphRequest/<_All types of sensors used by the application separated by an underscore_>/<_Threshold probability_>

Request to download the trained models:
- <_API address_>:3000/OptimizeGraphRequest/saved_model/<_Model Name_>

Note: We suggest downloading the complete graph first to identify which models are trained and the types of sensors it uses. The complete Graph can also guide decision-making in the requirements elicitation and application design phases.
