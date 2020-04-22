import json 
import os 
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from datetime import date 

from secrets import spotify_user_id, spotify_token_1, spotify_token_2

class CreatePlaylist: 

  def __init__(self): 
    self.user_id = spotify_user_id
    self.token = spotify_token_1
    self.token_2 = spotify_token_2 
 

  def getYT(self): 
    pass 

  def getLikedVideos(self): 
    pass 

  def createPlaylist(self): 
    t = date.today() 
    datestring = t.strftime('%m/%d/%Y')
    json_body = json.dumps({ 
      "name": "YT Liked Videos - " + datestring, 
      "description": "YT Liked Videos from " + datestring, 
      "public": False
    })

    q = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id) 
    r = requests.post(
      q, 
      data = json_body, 
      headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.token_2)
      }
    )
    response_json = r.json()
    return response_json["id"]

  def getSpotifyURI(self, song_name, artist): 
    q =  "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
      song_name,
      artist
    )
    r = requests.get(
      q, 
      headers = { 
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.token_2)
      }
    )
    response_json = r.json() 
    songs = response_json["tracks"]["items"]

    uri = songs[0]["uri"]

  def addSong(self): 
    pass

if __name__ == '__main__':
    # cp = CreatePlaylist()
    # cp.addSong()
    print("testing")
    # t = date.today() 
    # datestring = t.strftime('%m/%d/%Y')
    # json_body = json.dumps({ 
    #   "name": "YT Liked Videos - " + datestring, 
    #   "description": "YT Liked Videos from " + datestring, 
    #   "public": False
    # })

    # q = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id) 
    # r = requests.post(
    #   q, 
    #   data = json_body, 
    #   headers={
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer {}".format(spotify_token_2)
    #   }
    # )
    # response_json = r.json()
    # print(response_json)
    # print("--------")
    # song_name = "Suge"
    # artist = "DaBaby"

    # q =  "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
    #   song_name,
    #   artist
    # )
    # r = requests.get(
    #   q, 
    #   headers = { 
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer {}".format(spotify_token_2)
    #   }
    # )
    # response_json = r.json() 

    # songs = response_json["tracks"]["items"]

    # uri = songs[0]["uri"]
    # print(uri)



    