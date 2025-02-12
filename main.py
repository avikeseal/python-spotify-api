from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


load_dotenv()

#this will get the value of the env variable, in this case, client id
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET") #and client secret

#print(client_id, client_secret)

#here we will be implementing an API that allows us to query information
#about the spotify library e.g. artists, albums, playlists, songs, tracks, etc

#for out first step we start by requesting an access token.
#we do that by sending client id, client secret and few other information
#to spotify account services
#this service returns us a temp acess token
#with that access token we can then send requests to spotify web api

#we take out client ID concatenate to our client secret and then 
#encode that using a base64 encoding and thats what we need to send to retrieve
#our authorization token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    #url we wanna send reuqest to:
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    result = post(url, headers=headers, data=data)
    #we're gonna be returning some json data in a field known as content:
    #convert that data into a python dict so we can acess information inside
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#when we get the acces to our auth token this is what we'll be using in and
#any future headers when we're trying to send requests to the api to get some artist 
#or playlist information
#whenever we're sending another request:
def get_auth_header(token):
    #we take the token and return the following header
    #thats all you need for the authorization header for any future requests
    #you got to use this API token
    return {'Authorization': 'Bearer ' + token}

#this func is going to search for artists
#we need the token as well as the artist's name
def search_for_artist(token, artist_name):
    #url of search api endpoint
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    #combining queries together:
    query_url = url + query
    result = get(query_url, headers=headers)
    #parsing json result:
    json_result = json.loads(result.content)["artists"]["items"]
    #if the length of my json reult is equal to 0:
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    #else it will print out the very first result:
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, "ACDC")
#to display the artist:
#print(result["name"])
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song["name"]}")