# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import requests
import pickle

############# Comment
# Please read the README text in the github directory to better understand this process.

############# Checks if program ran before, if not, run this 
if 'movieDF.txt' not in os.listdir(): 
    with open('sampleJsonMovieRequest.txt', 'rb') as file:
        movieRequest, sampleJsonDfConstruction = pickle.load(file)
#Create list of keys and varNames to obtain data of interest
    for i, val in enumerate(list(sampleJsonDfConstruction.keys())):
        print(i, val)
    jsonSelecIndex = [0, 1, 5, 8, 13, 14, 16, 18, 22, 24, 26, 30, 31, 32, 39]    
    jsonSelec = [list(sampleJsonDfConstruction.keys())[i] for i in jsonSelecIndex]
#Create var name vector and movieDF
    varNames = jsonSelec[0:-1] + list(sampleJsonDfConstruction[jsonSelec[-1]].keys())
    movieDF = pd.DataFrame(columns=varNames)
#Initialize counters
    currentIndex = 0   
    with open('movieDF.txt', 'wb') as file:
        pickle.dump([movieDF, movieRequest, jsonSelec, currentIndex], file)

############# Load previous state
with open('movieDF.txt', 'rb') as file:
    movieDF, movieRequest, jsonSelec, currentIndex = pickle.load(file)
############# Obtain movie ids for movie data API request 
# API request limit of 50 a day
maxIndex = currentIndex + 50
while currentIndex < maxIndex:
#Status update:
    print("Current index: " + str(currentIndex))
    urlID = "https://imdb-api.com/en/API/SearchMovie/***/" +  movieRequest.title[currentIndex]
    try:
        r = requests.get(urlID)
        json_data = r.json()
        movieID = json_data["results"][0]["id"]
        movieRequest.iloc[currentIndex, 0] = [movieID]
    except:
        print("URL ID request for " + movieRequest.iloc[currentIndex, 1] + " failed!")
############# Obtain movie data via id 
    if not pd.isna(movieRequest.movie_id[currentIndex]):
        extraction = movieRequest.movie_id[currentIndex]
        if type(extraction) is list:
            extraction = extraction[0]
        if type(extraction) is not str:
            extraction = str(extraction) 
        urlData = "https://imdb-api.com/en/API/Title/***/" + extraction
        try:
            r = requests.get(urlData)
            json_data = r.json()
            values = (list(map(lambda x: json_data[x], jsonSelec)))
#Extract nested dict values
            boxOffice = values[-1]
            del values[-1]
            for key in list(boxOffice.keys()):
                values.append(boxOffice[key])
            movieDF.loc[len(movieDF.index)] = values
            movieRequest.iloc[currentIndex, 2] = 1
        except:
            movieRequest.iloc[currentIndex, 2] = 0
            print("URL data request or extraction for " + movieRequest.iloc[currentIndex, 2] + "failed!")
        currentIndex += 1    
    else:
        currentIndex += 1
        continue
    
############# Save latest version of movieDF and ouput CSV to put online
with open('movieDF.txt', 'wb') as file:
    pickle.dump([movieDF, movieRequest, jsonSelec, currentIndex], file)
    
movieDF.to_csv("movieDataOut.csv")