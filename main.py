from dotenv import load_dotenv
import os
import base64
from requests import post
import json

#
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

token = get_token()
print(token)