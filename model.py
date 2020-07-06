# model.py

import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

df = pd.read_csv(
    "https://raw.githubusercontent.com/richardOlson/unit4_build/master/data.csv")

first_five = df.iloc[:5]

#Variable imports from pickle files
infile = open("clean_scaler.pkl",'rb')
clean_scaler = pickle.load(infile)
infile.close()

infile = open("result_yr_dict.pkl",'rb')
id_dict = pickle.load(infile)
infile.close()

infile = open("yr_scaler.pkl", "rb")
yr_scaler = pickle.load(infile)
infile.close()

encoder_updated = load_model('encoder_updated')

yr_model = load_model("year_model")

infile = open("neighbor_updated.pkl", "rb")
neighbor = pickle.load(infile)
infile.close()

infile = open("getIdDict.pkl", "rb")
result_id_dict = pickle.load(infile)
infile.close()

# getting the clean function
def clean_function(df, scaler=None, use_test_split=False):
  """
    This function will clean and prepare the data for the prediction function.
    If use_test_split is False then will return X, y.
    If use_test_split is True will return x_train, x_test, y_train, y_test.
    """
  dff = df.copy()

  # removing any pause track
  dff = dff[(df["name"] != "Pause Track") & (dff["name"] != "Pause Track - Live")]

  # target for the first model will be the int of the year released.
  # the target is only for the training aspect
  target = ["name", "id"]

  features = [
    "acousticness", "popularity", "danceability", "duration_ms", "energy",
     "instrumentalness", "key", "liveness", "loudness", "mode","speechiness",
     "tempo", "valence"
              ]

  X = dff[features]
  y = dff[target]
  # doing the scaling of the data
  #scaler = MinMaxScaler()
  #scaler = StandardScaler()
  X = scaler.fit(X).transform(X)

  if use_test_split == True:
    x_train , x_test, y_train, y_test = train_test_split(
      X, y, test_size=.05, random_state=42
      )
    return x_train, x_test, y_train, y_test

  return X, y


def getPred(playlist, neighbor_model, result_id_dict, cleanFunction, clean_scaler, encoder,
            model_yr=None, yr_scaler=None, numsongs_return=10):
  """
  This is the function that will be used
  for predicting with using the  year and or explicit features
  """
  # coming out of this function the x is scaled
  # with the standard scaler
  x, y = cleanFunction(playlist, scaler=clean_scaler)
  yr_result = None
  year_empty = 1

  # choosing the type of encoder to use
  if model_yr != None:
    yr_result = model_yr.predict(x)
    yr_result = yr_scaler.fit(yr_result).transform(yr_result)
    year_empty = 0

  # Now need to check if the there are values in the yr_result and the 
  # explicit_result
  if year_empty == 0:
    x = np.hstack((x,yr_result))

  # Will now get the prediction with the encoder
  playList_results = encoder.predict(x)

  summed_val = 0
  # will loop through the playlist and get the average
  for result in playList_results:
    summed_val = summed_val + result
  # getting the average of the each of the values
  avg_val = summed_val/len(playlist)
  # running the avg_val into the nearest neighbor
  closest_ones = neighbor_model.kneighbors(
    [avg_val], return_distance=False, n_neighbors=10
    )
  # making the list of ids to check
  y_list = y["id"].tolist()

  suggested_songs = []
  # Looping through the array of the closest_ones
  for i in range(len(closest_ones[0])):
    x = result_id_dict.get(closest_ones[0][i])
    if x not in y_list:
      suggested_songs.append(x)
    if len(suggested_songs) == numsongs_return or i == len(closest_ones[0])-1:
      break
  return suggested_songs

def mood_check(mood_dict):
    for key in mood_dict:
        if mood_dict[key] != 0:
            return True
    return False

def mood_mult(df, mood):
    new_mood = pd.DataFrame()
    for i in range(len(df)):
        new_mood = pd.concat([new_mood, mood])
    df = pd.concat([df, new_mood])
    return df

encoded_full = load_model('encoded_complete', compile=False)

suggested_songs = getPred(
    df, neighbor_model=neighbor, result_id_dict=id_dict, 
    cleanFunction=clean_function, clean_scaler=clean_scaler, 
    encoder=encoder_updated, model_yr=yr_model, yr_scaler=yr_scaler)



if __name__ == "__main__":
    suggested_songs = getPred(
        df, neighbor_model=neighbor, result_id_dict=id_dict, 
        cleanFunction=clean_function, clean_scaler=clean_scaler, 
        encoder=encoder_updated, model_yr=yr_model, yr_scaler=yr_scaler)

    print(suggested_songs)
