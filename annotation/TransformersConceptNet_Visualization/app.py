from flask import Flask, redirect, render_template, request, url_for
from collections import Counter
import argparse 
from pathlib import Path
from utils import read_cluster_data, read_annotations, read_sentences, load_all_cluster_data
app = Flask(__name__) 


@app.route("/")
def index(): 
   return redirect(url_for("get_cluster", cluster_id=0, layer_id=0)) 

@app.route('/cluster/<layer_id>/<cluster_id>', methods = ['GET'])
def get_cluster(cluster_id, layer_id):

    cluster_id=int(cluster_id)
    temp = "c" + str(cluster_id)
    clusters_path = Path(DATA_PATH) / f"layer{layer_id}" / "clusters-500.txt"
    annotations_path = Path(DATA_PATH) / f"layer{layer_id}" / "annotations.json"
    cluster_to_words = read_cluster_data(clusters_path)
    if temp not in list(cluster_to_words.keys()): 
        return f"<p> Invalid cluster ID {temp} </p>"
    words = cluster_to_words[temp] 
    label = read_annotations(annotations_path)[temp]
    
    word_frequencies = list(Counter(words).items()) 

    return render_template("display.html", word_frequencies=word_frequencies, label=label, cluster_id=cluster_id, layer_id=layer_id, model=MODEL)

@app.route("/sentences", methods=['POST']) 
def get_sentences(): 
    cluster_id = request.json["cluster_id"]
    word = request.json["word"] 
    layer_id = request.json["layer_id"]

    word = word.strip() 
    temp = "c" + str(cluster_id)

    clusters_path = Path(DATA_PATH) / f"layer{layer_id}" / "clusters-500.txt"

    clusters = load_all_cluster_data(clusters_path=clusters_path)

    if temp not in list(clusters.keys()): 
        return f"<p> Invalid cluster ID {temp} </p>"
    
    local_sentences = [[SENTENCES[sentence_idx], token_idx] for token, sentence_idx, token_idx in clusters[f"c{cluster_id}"] if token == word]

    return {"success": True, "sentences": local_sentences}
    



if __name__=="__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument("-dp", "--data_path", help="path to where the data was downloaded")
    parser.add_argument("-p", "--port", default="8080", help="port used to run the app")
    parser.add_argument("-hs", "--host", default="0.0.0.0", help="host used to run the app")
    args=parser.parse_args()

    DATA_PATH=args.data_path
    PORT=args.port
    HOST=args.host

    sentences_path = Path(DATA_PATH) / "sentences.json"
    SENTENCES = read_sentences(sentences_path)
    MODEL = DATA_PATH.split("/")[-1]


    app.run(host=HOST, debug=True, port= PORT)


