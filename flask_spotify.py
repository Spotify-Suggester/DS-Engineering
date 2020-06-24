from flask import Flask, jsonify, request, render_template
import pickle
import json

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
#  return render_template("main.html")
    req = request.json.get("audio_features")
    return jsonify(req)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)