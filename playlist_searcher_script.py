#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:42:03 2022

@author: geoffreyliddell
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 10:49:29 2022

@author: geoffreyliddell
"""

import requests
import unidecode


# accent removal from:
# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string



#%% AUTHORISATION SECTION

# All courtesy of:
# https://stmorse.github.io/journal/spotify-api.html

CLIENT_ID = 'd4f47f0943cc48c584edb906357648a2'
CLIENT_SECRET = '797dc982d7924038a228159b23a8b6b8'
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'


# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

# create header to input to requests
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}





#%% TAKE USERNAME
user = input('Type your username: ')

# INCOMPLETE!
# filter playlists containing terms: give a comma separated list
filter_input = input('Playlist filter: ').split(',')
playlist_filter = {x.strip() for x in filter_input}





#%% GET ALL USER PLAYLIST URIs

# create a set which will contain strings common to all target playlists, i.e. those organised by month
playlist_uris = []
playlist_names = []

# counters to work around the request limit of 50 items
offset = 0
lim = 50

while True:
    got_playlists = requests.get(BASE_URL + 'users/' + user + '/playlists', 
                                 headers = headers,
                                 params = {'limit': lim, 'offset': offset}).json()


    for playlist in got_playlists['items']:   
        for filt in playlist_filter:           
            if filt in playlist['name'][0:3]: # [0:3] at the end of this line is a special case for MY playlists: removing this will -> less specific search               
                playlist_names.append(playlist['name'])
                playlist_uris.append(playlist['uri'].split(sep = ':')[2]) 


    
    if len(got_playlists['items']) < lim:
        break
        
    offset = offset + lim


playlist_uri_name_dict = dict(zip(playlist_uris, playlist_names))
#playlist_uri_name_dict




#%% CREATE SEARCHABLE DICTIONARY OF TRACKS

tracks_playlist_dict = dict()


for playlist_uri in playlist_uris:
    
    # counters to work around the request limit of 50 items
    offset = 0
    lim = 50
    
    num_tracks = 0
    while True:
        
        # can get away with no iteration here as I believe all my playlists are under 50 tracks long!
        tracks_tmp = requests.get(BASE_URL + 'playlists/' + playlist_uri + '/tracks', 
                          headers = headers,
                          params = {'limit': lim, 'offset': offset}).json()
    
        # extract track URIs + add playlist membership to a dict: add as an actual name for now for transparency
        for track in tracks_tmp['items']:
            num_tracks += 1
            artist_search = ''
            for artist in track['track']['artists']:
                artist_search += ' ' + artist['name'].lower()
                
            search_term = artist_search + ' ' + track['track']['name'].lower() + ' ' + track['track']['album']['name'].lower()
            search_term = unidecode.unidecode(search_term)
            
            tracks_playlist_dict.setdefault(search_term, {track['track']['uri'] : []})

            try:   
                tracks_playlist_dict[search_term][track['track']['uri']].append(playlist_uri_name_dict.get(playlist_uri).lower())
            except KeyError:
                print(search_term)
                print(playlist_uri_name_dict[playlist_uri])
                print(tracks_playlist_dict[search_term])
                print('''
                      Bug!! If a track has been added to a playlist a long time ago, and since then the URI has changed,
                      then the same track has been added to a newer playlist, the old URI will persist in the old 
                      playlist. An error will then throw in the next line, since only one URI is present in the 
                      nested dictionary and it is not the one we want!
                      ''')   
            
        if len(tracks_tmp['items']) < lim:
            break
        
        offset = offset + lim
        
    print('Playlist:  ' + playlist_uri_name_dict[playlist_uri] + '.\t Number of Tracks:  ' + str(num_tracks))



#%% USEABLE SECTION!

print('When you are done searching, exit by pressing CTRL + C')

while True:
    
    search_term = input('Type an artist or song here: ').lower()
    search_term = unidecode.unidecode(search_term)
    
    playlists0 = []

    # quick search in case where there's an exact track name match
    if search_term in tracks_playlist_dict:
    
        # once again sat here accounting for multiple playlists that probably aren't there!! ...hopefully useful in someone else's library
        for playlist in tracks_playlist_dict[search_term].values():
            playlists0.append(playlist)
    
        print('"' + search_term + '"' + ' is in the playlists ' + str(playlists0))

    # if there's no exact match go back and check for partial matches (slower as every string is checked fully)
    else:
        print('Possible matches: ')
        no_matches = 0
        for track in tracks_playlist_dict:
            if search_term in track:
                no_matches += 1
                for playlists in tracks_playlist_dict[track].values():
                    print('\t' + track + '--' + str(playlists))
        
        if no_matches == 0:
            print('There were no matches, please search again.')
            
        
        #print('"' + search_term + '"' + ' is not in any of your playlist')
    #elif search_term not in tracks_playlist_dict: