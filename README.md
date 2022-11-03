# Description
The aim is to create my own MySQL movie database with data pulled the internet. 

## Steps
1. Automate API requests and data extraction from the IMDB database using Python (DONE)
2. Collect data (within API request limit) (IN PROGRESS)
3. Create SQL database from data (UPCOMING)
4. Automate further data collection and feeding data directly into database 
5. Analyse collected data


## Please note the following: 
* Movie titles have been extracted from another dataset, [Grouplens](https://grouplens.org/datasets/movielens/latest/), in order to use them in the API requests. The data was cleaned and shuffled beforehand (to make the data more interesting for data analysis, since movies were sorted by year and API requests on IMDB are limited on a free account)
* The code for Step 1 was written to work as a program. Upon running ***apiRequestDataExtraction_NO_API_KEY.py***, it checks whether the program was run before and if this is not the case, the file ***sampleJsonMovieRequest.txt*** is loaded, some objects are generated from it and these are then written to file (***movieDF.txt***). **movieDF.txt** will then be loaded every time the program is run again and written to at the end of each execution. 
* The above means that IN ORDER TO RUN SUCCESSFULLY, BOTH the apiRequestDataExtraction_NO_API_KEY.py and the sampleJsonMovieRequest.txt FILES MUST BE STORED IN THE SAME DIRECTORY. Moreover,  my API KEY HAS BEEN REMOVED from the url strings (the place is marked with ***).
* Please note: the ***movieDataOut.csv*** file only shows a single line of data output (due to copyright concerns), in order to show what the generated data file looks like
* To better understand the code:
  * There are two dataframes that are used in the program. The first, movieRequest, contains the title variable containing movie titles as well as two columns, movie_id (containing only NaNs) and dataObtained (containing only 0s). 
  * movieRequest.title is used to query the IMDB API for the movieID, which, if found, is inserted.
  * Then, this movieID is used to query the IMDB API for movie data. If obtained successfully, the 0 in movieRequest.dataObtained is replaced by 1
  * The aim of movieRequest is to provide an overview of the data accumulation process, in order to identify potential erros/ unexpected behaviour. It records which requests have been (un)successful
