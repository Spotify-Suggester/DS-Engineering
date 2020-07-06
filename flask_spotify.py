from flask import Flask, jsonify, request, render_template
import json
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from model import neighbor, id_dict, clean_scaler, yr_model, yr_scaler, result_id_dict, clean_function, encoder_updated, getPred, mood_mult, mood_check

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
    #Takes POST from webpage, checks for mood data, multiplies mood rows
    req = request.json.get("favorite_songs")
    json_format = json.dumps(req)
    df = pd.read_json(json_format)
    mood_req = request.json.get("mood")
    if mood_check(mood_req[0]) == True:
        mood_req_format = json.dumps(mood_req)
        mood_df = pd.read_json(mood_req_format)
        df = mood_mult(df, mood_df)
    print(df)

    #Returns suggested songs
    suggested_songs = getPred(
        df, neighbor_model=neighbor, result_id_dict=id_dict, 
        cleanFunction=clean_function, clean_scaler=clean_scaler, 
        encoder=encoder_updated, model_yr=yr_model, yr_scaler=yr_scaler)
    print(suggested_songs)
    return jsonify(suggested_songs)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
