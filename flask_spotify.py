from flask import Flask, jsonify, request, render_template
import pickle
import viz
import json
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from model import neighbor, result_id_dict, clean_data_split, encoded_full, getPred, df, mood_mult, mood_check
#from tensorflow.keras.models import load_model

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
#  return render_template("main.html")
    req = request.json.get("favorite_songs")
    json_format = json.dumps(req)
    df = pd.read_json(json_format)
    mood_req = request.json.get("mood")
    print(req)
    print(mood_req)
    if mood_check(mood_req[0]):
      if mood_req != None:
          mood_req_format = json.dumps(mood_req)
          mood_df = pd.read_json(mood_req_format)
          mood_df = mood_df.fillna(0)
          df = mood_mult(df, mood_df)
#    data = pd.read_json(req, orient='split')
    print(df)
    suggested_songs = getPred(df, neighbor, result_id_dict,
                              clean_data_split, encoded_full)
    print(suggested_songs)
    return jsonify(suggested_songs)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
