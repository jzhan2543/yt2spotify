import json 
import os 
import requests
from datetime import date 

from secrets import user_id, token 

class CreatePlaylist: 

  def __init__(self): 
    pass 

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

    q = "https://api.spotify.com/v1/users/{}/playlists".format(user_id) 
    r = requests.post(
      q, 
      data = json_body, 
      headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
      }
    )
    response_json = r.json()
    return response_json["id"]

  def getSpotifyURI(self): 
    pass 

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

    # q = "https://api.spotify.com/v1/users/{}/playlists".format(user_id) 
    # r = requests.post(
    #   q, 
    #   data = json_body, 
    #   headers={
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer {}".format(token)
    #   }
    # )
    # response_json = r.json()


    