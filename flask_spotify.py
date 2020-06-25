from flask import Flask, jsonify, request, render_template
import pickle
import viz
import json
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from model import neighbor, result_id_dict, clean_data_split, encoded_full
#from tensorflow.keras.models import load_model

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
#  return render_template("main.html")
    req = request.json.get("audio_features")
    json_format = json.dumps(req)
    df=pd.read_json(json_format)
#    data = pd.read_json(req, orient='split')
#    df = pd.DataFrame(data)
    print(df)
    return jsonify(req)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)