import spotipy
import spotipy.util as util
from classModules import Song
import datetime

import pdb

def generateUserToken(username,scope,key,secret,url):
	token=None
	count=0
	while(count<4):
		token=util.prompt_for_user_token(username,scope,key,secret,url)

		if token:
			return token
		else:
			count+=1

	return token

# for a given artist_id return a list of albumIds
def getAlbumsForArtist(spotifyId,location=None):
	spotify=spotipy.Spotify()
	albums=[]
	names=[]
	while(True):
		# pdb.set_trace()
		# check if this actually works, not skipping one after every 50
		returnedAlbums=spotify.artist_albums(artist_id=str(spotifyId),country=location,limit=50,offset=len(albums))
		# return returnedAlbums
		if len(returnedAlbums['items'])>0:
			for album in returnedAlbums['items']:
				for i in range(0,len(album['artists'])):
					names.append((int(i+1),album['artists'][i]['id'],album['artists'][i]['name']))
					if i==0 and str(spotifyId)!=str(album['artists'][i]['id']):
						names.append(album)
				albums.append(album['id'])
		else:
			with open("artsits","a+") as f:
				for tup in names:
					f.write(str(tup))
					f.write("\n")
			with open("albums","a+") as f:
				for i in albums:
					f.write(str(i))
					f.write("\n")

			return albums

# albums is an array of ids
# artist is the spotify id of the artist
# return song array
def getSongsFromAlbumsForArtist(spotifyId,artistId,albums):
	spotify=spotipy.Spotify()
	count=0
	songs={}
	while(True):
		temp=[]
		plusTwenty=min(len(albums)-1,count+20)
		while count<plusTwenty:
			temp.append(albums[count])
			count+=1

		# pdb.set_trace()
		# look into next not being None
		returnedAlbums=spotify.albums(temp)

		for album in returnedAlbums['albums']:
			if album['release_date_precision']=="day":
				releaseDayFields=album['release_date'].split("-")
				releaseDay=datetime.date(int(releaseDayFields[0]),int(releaseDayFields[1]),int(releaseDayFields[2]))
				today=datetime.date.today()
				diff=today-releaseDay
				if diff.days<31:
					for track in album['tracks']['items']:
						cont=False
						artistNames=[]
						for a in track['artists']:
							artistNames.append(a['name'])
							if a['id'] == spotifyId:
								cont=True
						if cont:
							songName=track['name']
							song=None

							artistName=""
							if len(artistNames)>1:
								artistName+=artistNames[0]
								artistName+=" feat. "
								for i in range(1,len(artistNames)-1):
									artistName+=artistNames[i]
									artistName+=", "
								artistName+= artistNames[len(artistNames)-1]
							else:
								artistName=artistNames[0]

							# only important when dealing with songs and multiple markets
							# so as long as a country is supplied to the getAlbumsForArtist
							# we shouldn't have to worry about this
							if songName+"-"+artistName in songs:
								song=songs[songName+"-"+artistName]
							else:
								song = Song(songName,artistName)
								song.artistId=artistId
								key=song.name+"-"+song.artistName
								songs[key]=song

							for key in track['available_markets']:
								value={}
								value['id']=track['id']
								value['url']=track['external_urls']['spotify']
								value['uri']=track['uri']
								value['preview_url']=track['preview_url']
								songs[song.name+"-"+song.artistName].addSpotifyKeyValue(key,value)

		if count==len(albums)-1:
			return songs.values()





