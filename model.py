# model.py

import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from tensorflow.keras.models import load_model

df = pd.read_csv(
    "https://raw.githubusercontent.com/richardOlson/unit4_build/master/data.csv")

first_five = df.iloc[:5]

# getting the clean function
def clean_data_split(df, use_test_split=False):
  """
  This is the function that will clean the data getting it
  ready for use
​
  use_test_split: is set to False and will not split the data.
  When changed to True, will split the data with 5 percent as a test data
​
  If use_test_split is False then will return X, y
  If use_test_split is True will return x_train, x_test, y_train, y_test
​
  """
  dff = df.copy()
  # removed artists, and id from the features
  features = [
      "acousticness",  "popularity", "danceability", "duration_ms", "energy",
      "instrumentalness", "key", "liveness", "loudness", "mode",
      "speechiness", "tempo", "valence"
  ]
  if use_test_split == True:

    target = ["id", "name"]
  else:
    target = ["id"]

  X = dff[features]
  y = dff[target]
  # won't encode the artists

  scaler = MinMaxScaler()
  X = scaler.fit_transform(X)
  # doing the normalization of the data
  #normalizer = Normalizer("max")
  #X = normalizer.fit_transform(X)
  if use_test_split == True:
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.05,
                                                        random_state=42)
    return x_train, x_test, y_train, y_test

  return X,  y


def getPred(playList, neigbor, result_id_dict,  cleanfunc, encoder_model, num_songs_to_return=5):
  """
    This function will return a list of the songs that are suggested
  """
  # Will run each of the songs through the
  # clean method and then will send it through the
  # encoder
  x, y = cleanfunc(playList, use_test_split=False)

  playList_results = encoder_model.predict(x)

  summed_val = 0
  # will loop through the playlist and get the average
  for result in playList_results:
    summed_val = summed_val + result
  # getting the average of the each of the values
  avg_val = summed_val/len(playList)
  # running the avg_val into the nearest neighbor
  closest_ones = neigbor.kneighbors([avg_val], return_distance=False)
  # making the list of ids to check
  y_list = y["id"].tolist()

  suggested_songs = []
  # Looping through the array of the closest_ones
  for i in range(len(closest_ones[0])):

    x = result_id_dict.get(closest_ones[0][i])
    if x not in y_list:
      suggested_songs.append(x)
    if len(suggested_songs) == num_songs_to_return or i == len(closest_ones[0])-1:
      break
  return suggested_songs


infile = open("/content/neighbor.pkl", "rb")
neighbor = pickle.load(infile)
infile.close()

infile = open("/content/getIdDict.pkl", "rb")
result_id_dict = pickle.load(infile)
infile.close()


encoded_full = load_model('/content/content/encoded_complete')

suggested_songs = getPred(
    first_five, neighbor, result_id_dict, clean_data_split, encoded_full)