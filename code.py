import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = '667b885478864cdaa451d528aa6b1730'
secret = '29f10790089b4ca5a0208c72199d2105'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result=sp.search('WWE',type='playlist')

ids={}
for i in range(len(result['playlists']['items'])):
    ids[i]=result['playlists']['items'][i]['id']

def show_tracks(results,uri_array):
    for i, item in enumerate(results['items']):
        track=item['track']
        uri_array.append(track['id'])

def get_playlist_track_id(ids):
    trackId=[]
    for i in range(len(ids)):
        results=sp.playlist(ids[i])
        tracks=results['tracks']
        show_tracks(tracks,trackId)
        while tracks['next']:
            tracks=sp.next(tracks)
            show_tracks(tracks,trackId)
    return trackId

name=[]
dance=[]
energy=[]
loud=[]
speech=[]
valence=[
acoustic=[]
instru=[]
live=[]
tempo=[]
for track in range(len(track_ids)):
    af=sp.audio_features(track_ids[track])[0]
    name.append(sp.track(af['id'])['name'])
    dance.append(af['danceability'])
    energy.append(af['energy'])
    loud.append(af['loudness'])
    speech.append(af['speechiness'])
    acoustic.append(af['acousticness'])
    instru.append(af['instrumentalness'])
    live.append(af['liveness'])
    valence.append(af['valence'])
    tempo.append(af['tempo'])

df=pd.DataFrame()

df['track_name']=name
df['danceability']=dance
df['energy']=energy
df['loudness']=loud
df['speechiness']=speech
df['valence']=valence
df['acousticness']=acoustic
df['instrumentalness']=instru
df['liveness']=live
df['tempo']=tempo

performer=[]
for track in range(len(df)):
    try:
        performer.append(df.track_name[track].split('(')[1].replace(')',''))
    except:
        performer.append(np.nan)
        
df['performer']=performer
df.dropna(inplace=True)
df.drop_duplicates(keep='first',inplace=True,subset=['performer'])
df.reset_index(drop=True,inplace=True)
df.drop('track_name',axis=1,inplace=True)
df.to_csv('wwe_theme.csv',index=False)