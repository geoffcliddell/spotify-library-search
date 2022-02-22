# spotify searcher

Jupyter notebook exploring the idea of searching a given user's public spotify playlists for a song and returning the playlists it is contained in. This is a function missing from Spotify's UI and not apparently catered for by any plugins currently.

I was suprised this function wasn't there as not being able to search your own library seems like a pretty large hole in Spotify's functionality! But it may also just be because I arrange my music in an awkward way: in monthly playlists. I've been doing this for nearly 4 years, which makes about 48 playlists which are all well under 50 songs. This makes songs easy to file in my memory, but when you have forgotten which month a song is in, it can be tedious to search for. Several people have asked on forums whether it is possible to check playlist membership for your own library, so it might not be an uncomon problem to have.

### Important note for potential users!

Python is not an ideal language to have written this in, JavaScript would make it possible for others to use it easily and also make the privacy/security side easier as there are examples on the web already of how to do this properly! However, what's done is done and so if you want to use this script yourself you will have to take the following steps:

1. Have python installed, sorry! Next project: translate to Javascript!
2. install unidecode, because of accents: ```pip install unidecode```
3. get a Spotify Developer account (easy email sign up process)
4. find your CLIENT ID + CLIENT SECRET. I followed this tutorial https://stmorse.github.io/journal/spotify-api.html
5. add these to the script yourself in place of ```'yourclientid'``` and ```'yourclientsecret'```
6. run the script from the command-line or from an IDE or whatever way you choose

### Possible Extensions

1. Translate to JavaScript/create webapp
2. Clustering, e.g. using tools from sklearn
