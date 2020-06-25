from flask import Flask, jsonify, request, render_template
import pickle
import json
import viz

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def main():
    #  return render_template("main.html")
    req = request.json.get("audio_features")
    viz.prediction(req)
    return jsonify(req)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
