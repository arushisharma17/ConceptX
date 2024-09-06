# TransformersConceptNet
Code and Data Associated with **Can LLMs facilitate interpretation of pre-trained language models?** 

# Data 
The data is present in the database folder. The folder has context sentences as sentences.json, 12 layer folders with each have annotations.json and clusters.txt

# Data Description 

We use agglomerative hierarchical clustering over contextualized Java representations and then annotate these concepts using GPT annotations. As of now, all layers have the layer 12 clusters and annotations. (Check to do)

# Load data into display 

Clone the repo-

```
git clone https://github.com/arushisharma17/CodeConceptNet.git
cd annotation/TransformersConceptNet_Visualization
```

Create and activate virtual environment: 
```
python -m venv .envs/tcn
source .envs/tcn/bin/activate
```
Install requirements: 
```
pip install -r requirements.txt
```
Start the webapp using the following command:

```bash
python -u app.py -d <path-to-database-folder>
```

and visit http://localhost:8080 in your browser. The port and hostname can be passed as additional arguments to `app.py`.

# To Do - 
Update all layers with their respective files. Update sentences.json.
Update with different categories of labels
Connect to updated annotation tool. 

