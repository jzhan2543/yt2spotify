import json 
import os 
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from datetime import date 

from secrets import spotify_user_id, spotify_token_1, spotify_token_2, yt_id 

class CreatePlaylist: 

  def __init__(self): 
    self.user_id = spotify_user_id
    self.token = spotify_token_1
    self.token_2 = spotify_token_2 
    self.youtube_client = self.getYT() 
    self.all_song_info = {}

 

  def getYT(self): 
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
      client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
      api_service_name, api_version, credentials=credentials) 
    return youtube 


  #Getting Liked Videos here 
  def getLikedVideos(self): 
    r = self.youtube_client.videos().list(
      part="snippet,contentDetails,statistics",
      myRating="like",
      maxResults=50
    )
    response = r.execute() 
    for item in response["items"]: 
      title = item["snippet"]["title"]
      print(title)
      youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

      video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
      song = video["track"]
      artist = video["artist"]

      if song is not None and artist is not None: 
        self.all_song_info[title] = { 
          "youtube_url" : youtube_url, 
          "song": song, 
          "arist": artist, 
          "spotify_uri": self.getSpotifyURI(song, artist)
        }

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
    print(song_name)
    print(artist)
    print("-------")
    songs = response_json["tracks"]["items"]

    uri = songs[0]["uri"]
    return uri 

  def addSong(self): 
    self.getLikedVideos() 
    uris=[info["spotify_uri"] for song, info in self.all_song_info.items()]
    playlist_id = self.createPlaylist() 
    request_data = json.dumps(uris)

    q = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id) 
    r = requests.post(
      q, 
      data = request_data, 
      headers = { 
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(self.token_2)
      }
    )
    if r.status_code != 201:
      print("Error Code: " + r.status_code)

    response_json = r.json()
    return response_json


if __name__ == '__main__':
    # cp = CreatePlaylist()
    # cp.addSong()
    print("testing")
    cp = CreatePlaylist()
    cp.addSong()


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



    