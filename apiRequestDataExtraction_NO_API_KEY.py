# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import requests
import pickle


############# Checks if program ran before, if not, run this 
if 'movieDF.txt' not in os.listdir(): 
    with open('sampleJsonMovieRequest.txt', 'rb') as file:
        movieRequest, sampleJsonDfConstruction = pickle.load(file)
#Create list of keys and varNames to obtain data of interest
    for i, val in enumerate(list(sampleJsonDfConstruction.keys())):
        print(i, val)
    jsonSelecIndex = [0, 1, 5, 8, 13, 14, 16, 18, 22, 24, 26, 30, 31, 32, 39]    
    jsonSelec = [list(sampleJsonDfConstruction.keys())[i] for i in jsonSelecIndex]
#Create var name vector and movieDF. The last key in the sampleJsonDfConstruction dict is boxOffice, a nested dict, so its keys need to be extracted and joined to the rest of the dict keys next
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
# API request limit of 100 a day, 2 API requests per movie
maxIndex = currentIndex + 50
while currentIndex < maxIndex:
#Status update:
    print("Current index: " + str(currentIndex))
    urlID = "https://imdb-api.com/en/API/SearchMovie/***/" +  movieRequest.title[currentIndex]
#First API request to obtain movie IDs . If found, replaced NaN value in movieRequest.movie_id, if it fails, error message
    try:
        r = requests.get(urlID)
        json_data = r.json()
        movieID = json_data["results"][0]["id"]
        movieRequest.iloc[currentIndex, 0] = [movieID]
    except:
        print("URL ID request for " + movieRequest.iloc[currentIndex, 1] + " failed!")
############# Obtain movie data via id 
    if not pd.isna(movieRequest.movie_id[currentIndex]):
        urlData = "https://imdb-api.com/en/API/Title/***/" +  movieRequest.movie_id[currentIndex]
        try:
            r = requests.get(urlData)
            json_data = r.json()
#Extract data from "JSON" dict
            values = (list(map(lambda x: json_data[x], jsonSelec)))
#Extract nested dict values from boxOffice within "JSON" and add to values
            boxOffice = values[-1]
            del values[-1]
            for key in list(boxOffice.keys()):
                values.append(boxOffice[key])
#Add data to last row of movieDF
            movieDF.loc[len(movieDF.index)] = values
#Change value in movieRequestDF.dataObtained from NaN to 1 or 0, depening on success or failure 
            movieRequest.iloc[currentIndex, 2] = 1
        except:
            print("URL data request or extraction for " + movieRequest.iloc[currentIndex, 2] + "failed!")
        currentIndex += 1    
    else:
        currentIndex += 1
        continue
    
############# Save latest version of movieDF        
with open('movieDF.txt', 'wb') as file:
    pickle.dump([movieDF, movieRequest, jsonSelec, currentIndex], file)


