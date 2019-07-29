import sys
import argparse
import spotipy
import spotipy.util as util
import csv
import pandas as pd

class slider:
    ''' Slider class represents a slider and its tagset'''

    def __init__(self,weight=1,tagset=[]):
        self.weight=weight
        self.tagset=tagset


    '''
    Add tags to a slider
    tags - a list of strings
    '''
    def addTags(self,tags):
        for i in tagset:
            if not i in self.tagset:
                tags+=[i]
    
    '''
    Remove tags from a slider
    tags - a list of strings
    '''
    def removeTags(self,tags):
        for i in tags:
            if i in self.tagset:
                del self.tagset[self.tagset.index(i)]

    '''
    Clear tags from a slider
    '''
    def clearTags(self):
        self.tags=[]


"""
Get all saved songs from a spotify client.
sp - a spotify client
Returns a list of dictionaries.
"""
def fetchAllSongs(sp):
    songs=[]
    i=0
    while i==0 or len(results['items'])>0:
        results = sp.current_user_saved_tracks(limit=50,offset=i*50)
        songs+=(results['items'])
        i+=1
    return songs


def playlistToTag(playlist):
    print("empty")

'''
Returns a list of songs
songs - a list of dicts
'''
def songsToTag(songs):
    print('empty')

'''
Returns dictionary from tags.txt
tags.txt is formatted as follows:
{tagname: [track1, track2, ..., trackn], tagname2: ...}
'''
def importTags():
    #make sure tags.txt exists by opening and closing
    tagfile = open('tags.txt','w')
    tagfile.close()

    tagfile = open('tags.txt','r')
    if len(tagfile.read())!=0:
        return eval(tagfile.read())
    else:
        print("No tags found.")
        return {}

'''
tags - dict of tags (tag is a list of track dicts) 
tagname - name of tag to be added
'''
def addTag(tags,tagname):
    tags[tagname]=[]
    return tags

'''
tags - core dict of tags
songs - list of song dicts to be added to the tags
taglist - list of tag strings to add songs to
'''
def addSongsToTag(tags,songs,taglist):
    for song in songs: #loop through each song dict to be added
        for tagname in taglist: #loop through each string representing a tag
            found=False
            for track in tags[tagname]: #loop through each track already in the tag to make sure no duplicates
                if track['track']['uri']==song['track']['uri']: found=True 
            if not found: tags[tagname].append(song)
    return tags

#def tagFromPlaylist(tags)

'''
Get all playlists from a spotify client.
sp - a spotify client
Returns a list of dictionaries.
'''
def fetchAllPlaylists(sp,username):
    playlists=[]
    i=0
    while i==0 or len(results['items'])>0:
        results = sp.user_playlists(limit=50,offset=i*50,user=username)
        playlists+=(results['items'])
        i+=1
    return playlists

'''
playlist - spotify dict
'''
def songsFromPlaylist(sp,playlist):
    songs=[]
    i=0
    while i==0 or len(results['items'])>0:
        results = sp.user_playlist_tracks(limit=50,offset=i*50)
        songs+=(results['items'])
        i+=1
    return songs


'''
Display songs
songs - a list of dicts
'''
def dispSongs(songs):
    for song in songs:
                print(song['track']['name'] + ' - ' + song['track']['artists'][0]['name'])

'''
Display playlists
playlists - a list of dicts
'''
def dispPlaylists(playlists):
    for playlist in playlists:
            print(playlist['name'] + ' by ' + playlist['owner']['display_name'] + ' (' + str(playlist['tracks']['total']) + ' songs)')


def main(args):

    try:
        username = args.username 
        client_id = args.client_id
        client_secret = args.client_secret
    except Exception as e:
        print("Error while loading args")
        print(e)

    scope='user-top-read user-read-recently-played user-read-playback-state user-read-currently-playing user-modify-playback-state user-library-modify user-library-read streaming app-remote-control user-read-private user-read-email user-follow-modify user-follow-read playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private'
    redirect_uri='http://localhost/'

    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        print("getting songs")
        songs=fetchAllSongs(sp)
        dispSongs(songs)
        print("getting playlists")
        playlists=fetchAllPlaylists(sp,username)
        dispPlaylists(playlists)
        print("importing tags")
        tags = importTags()
        print("complete")
        tags=addTag(tags,"rap")
        print("tags: %s" % tags)
        tags=addSongsToTag(tags,[songs[0],songs[1],songs[2]],['rap'])
        dispSongs(tags['rap'])
        
        
    

if __name__=="__main__":
    print("\n Moodify for Spotify")

    parser=argparse.ArgumentParser()
    parser.add_argument("username",help="Your username")
    parser.add_argument("client_id",help="Client id")
    parser.add_argument("client_secret",help="Client secret")
    args = parser.parse_args()
    main(args)
