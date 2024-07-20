from dotenv import load_dotenv
import os

#
load_dotenv()

#this will get the value of the env variable, in this case, client id
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET") #and client secret

print(client_id, client_secret)

#here we will be implementing an API that allows us to query information
#about the spotify library e.g. artists, albums, playlists, songs, tracks, etc

#for out first step we start by requesting an access token.
#we do that by sending client id, client secret and few other information
#to spotify account services
#this service returns us a temp acess token
#with that access token we can then send requests to spotify web api