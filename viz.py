
# viz.py

import flask_spotify
import math
from flask import jsonify, request
import json

'''
Script to compile data from user input playlist and compare
similarites to suggested tracks.
'''

test = {
    "recommended_songs": [
        {
            "id": "7GI1Weh21oGJYeSbrtOyR1",
            "name": "Windshield",
            "acousticness": .00587,
            "artist": "Greensky Bluegrass",
            "album": "If Sorrows Swim",
            "image_url": "https://i.scdn.co/image/ab67616d0000b273b26aa443332e4ccd14d42c0b",
            "popularity": 55,
            "duration_ms": 224853,
            "key": 0,
            "mode": 1,
            "time_signature": 4,
            "danceability": 0.48,
            "energy": 0.548,
            "instrumentalness": 0.00502,
            "liveness": 0.205,
            "loudness": -9.119,
            "speechiness": 0.0328,
            "valence": 0.322,
            "tempo": 90.109
        },
        {
            "id": "6DavaRzYekSRYl0VMHnlwo",
            "name": "Helpless (feat. Neil Young) - Concert Version",
            "artist": "The Band",
            "acousticness": .00587,
            "album": "The Last Waltz (Deluxe Version)",
            "image_url": "https://i.scdn.co/image/ab67616d0000b273415e5ff0f5a631e22af127a6",
            "popularity": 43,
            "duration_ms": 353227,
            "key": 0,
            "mode": 1,
            "time_signature": 4,
            "danceability": 0.43,
            "energy": 0.835,
            "instrumentalness": 0.0000153,
            "liveness": 0.99,
            "loudness": -7.415,
            "speechiness": 0.105,
            "valence": 0.393,
            "tempo": 114.186
        },
        {
            "id": "4QuSTcFDbHPrDFzxFxeF5s",
            "name": "Wrecking Ball",
            "artist": "Gillian Welch",
            "album": "Soul Journey",
            "image_url": "https://i.scdn.co/image/ab67616d0000b2736e13bd95bdb89f6bc030635b",
            "popularity": 38,
            "acousticness": .00587,
            "duration_ms": 296267,
            "key": 0,
            "mode": 1,
            "time_signature": 4,
            "danceability": 0.48,
            "energy": 0.417,
            "instrumentalness": 0.0000245,
            "liveness": 0.155,
            "loudness": -8.743,
            "speechiness": 0.0283,
            "valence": 0.366,
            "tempo": 145.637
        },
        {
            "id": "0shBLNwbMS8i903cWwnwln",
            "name": "Morning Dew - Live at Barton Hall, Cornell University, Ithaca, NY 5/8/77",
            "artist": "Grateful Dead",
            "album": "Cornell 5/8/77 (Live)",
            "image_url": "https://i.scdn.co/image/ab67616d0000b27375fcab3be9f5833d23e211f0",
            "popularity": 40,
            "acousticness": .00587,
            "duration_ms": 857213,
            "key": 7,
            "mode": 1,
            "time_signature": 4,
            "danceability": 0.456,
            "energy": 0.403,
            "instrumentalness": 0.15,
            "liveness": 0.591,
            "loudness": -13.965,
            "speechiness": 0.0383,
            "valence": 0.511,
            "tempo": 128.074
        },
        {
            "id": "5NRJrFPd3rfJRJUMWxV7zr",
            "name": "Surprise Valley",
            "artist": "Widespread Panic",
            "album": "Til the Medicine Takes",
            "image_url": "https://i.scdn.co/image/ab67616d0000b2730b7bf250f2d9a04ed521b891",
            "popularity": 36,
            "acousticness": .00587,
            "duration_ms": 375000,
            "key": 7,
            "mode": 1,
            "time_signature": 4,
            "danceability": 0.482,
            "energy": 0.908,
            "instrumentalness": 0.153,
            "liveness": 0.457,
            "loudness": -4.956,
            "speechiness": 0.0422,
            "valence": 0.506,
            "tempo": 103.317
        }
    ]
}

# important features
important_features = ["danceability", "energy", "mode", "speechiness",
                      "instrumentalness", "liveness",
                      "valence"]

# round function
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# function that returns averages of important features
def aggregate(df, key):
    key1 = key
    features = req
    keys = [feature[key1] for feature in features]
    average = abs(sum(keys)) / len(keys)
    return round_up(average, 4)
    # return keys


def viz_data(df):
    important_features = ["danceability", "energy", "mode", "speechiness",
                          "instrumentalness", "liveness",
                          "valence"]
    features = {}

    for i in important_features:
        features[i] = (aggregate(df, i))

    return features


def prediction(df):
    important_features = ["acousticness",  "popularity", "danceability", "duration_ms", "energy",
                          "instrumentalness", "key", "liveness", "loudness", "mode",
                          "speechiness", "tempo", "valence"]
    features = {}

    for i in important_features:
        features[i] = (aggregate(df, i))

    return features


if __name__ == "__main__":

    print(prediction(test))
