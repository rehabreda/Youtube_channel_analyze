# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 18:51:12 2018

@author: rehab
"""

# import libraries
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pandas as pd 
from google_auth_oauthlib.flow import InstalledAppFlow

DEVELOPER_KEY = "AIzaSyBy4Jydi56nak_KmIBZ4kCKTmnTX10YJ_s" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CLIENT_SECRETS_FILE='client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
#authentication

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = credentials)

client= get_authenticated_service()
playlist=[]
# collect playlist in channel
def search_list_by_keyword(client, **kwargs):
 

  response = client.search().list(
    **kwargs
  ).execute()

  return response

response=search_list_by_keyword(client,
    part='snippet',
    maxResults=50,
    channelId='UCelk6aHijZq-GJBBB9YpReA',
    type='playlist'
    )
for i in range(50):
    playlist.append(response['items'][i]['id']['playlistId'])
    


while('nextPageToken' in response):
    next_page=response['nextPageToken']
    response=[]
    response=search_list_by_keyword(client,
    part='snippet',
    maxResults=50,
    channelId='UCelk6aHijZq-GJBBB9YpReA',
    type='playlist',
    pageToken=next_page)
    for i in range(len(response['items'])):
        playlist.append(response['items'][i]['id']['playlistId'])
        

# get playlist items
def playlist_items_list_by_playlist_id(client, **kwargs):
  
  

  response = client.playlistItems().list(
    **kwargs
  ).execute()

  return response        

data=[]
for i in playlist:
    data.append(playlist_items_list_by_playlist_id(client,
        part='snippet,contentDetails',
        maxResults=50,
        playlistId=i ))
    
    
# get all videos id in all playlist
videos=[]
for i in range(66):
    for j in range(len(data[i]['items'])):
        videos.append(data[i]['items'][j]['contentDetails']['videoId'])
        
        
# search for individual videos in channel 


response=search_list_by_keyword(client,
    part='snippet',
    maxResults=50,
    channelId='UCelk6aHijZq-GJBBB9YpReA',
    type='video'
    )  
for i in range(50):
    videos.append(response['items'][i]['id']['videoId']) 
    
    
while('nextPageToken' in response):
    next_page=response['nextPageToken']
    response=[]
    response=search_list_by_keyword(client,
    part='snippet',
    maxResults=50,
    channelId='UCelk6aHijZq-GJBBB9YpReA',
    type='video',
    pageToken=next_page)
    for i in range(len(response['items'])):
        videos.append(response['items'][i]['id']['videoId'])
# get videos data 
def videos_list_by_id(client, **kwargs):
  
  response = client.videos().list(
    **kwargs
  ).execute()

  return response  

video_data=[]
for i in videos:
    video_data.append(videos_list_by_id(client,
    part='snippet,contentDetails,statistics',
    id=i))  

items=[]

for i in range(len(video_data)):
    items.append(video_data[i]['items'])        
    
d=pd.DataFrame()
for i in range(len(items)):
    d=d.append(pd.DataFrame.from_dict(items[i])) 
    
contentDetails=d['contentDetails'].tolist()
contentDetails=pd.DataFrame.from_dict(contentDetails)
duration=pd.DataFrame(contentDetails['duration'])
   
snippet=d['snippet'].tolist()
snippet=pd.DataFrame.from_dict(snippet)

statistics=d['statistics'].tolist()
statistics=pd.DataFrame.from_dict(statistics)

df=pd.concat([snippet, statistics,duration], axis=1 )   


# convert dataframe to csv file
df.to_csv('data.csv',encoding='utf-8-sig',columns = df.columns)
    

    