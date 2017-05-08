# from gevent import monkey
# monkey.patch_all()
import spotipy
import spotipy.util as util
from classModules import Song
from classModules import QueItem
from classModules import SetQueue
import datetime
from Queue import Queue
from threading import Thread
import sys

import pdb

MAX_NUMBER_OF_THREADS = 8

BAD_ARTISTS = {
	"0LyfQWJT6nXafLPZqxe9Of" : 1
}

MONTH = "month"
DAY = "day"

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

def _getAlbumsForArtist(spotifyId, location, offsets, responses, i):
	spotify=spotipy.Spotify()
	while True:
		offset=offsets.get()
		returnedAlbums=spotify.artist_albums(artist_id=str(spotifyId),country=location,limit=50,offset=offset)
		
		if len(returnedAlbums['items']):
			for album in returnedAlbums['items']:
				responses.put(QueItem(album['id']))
			offsets.put(QueItem(int(offset+len(returnedAlbums['items']))))

		offsets.task_done()

		

# for a given artist_id return a list of albumIds
def getAlbumsForArtist(spotifyId,location=None):
	albums=[]
	offsets=SetQueue()
	responses=SetQueue()
	initialOffsets=[QueItem(0), QueItem(50), QueItem(100), QueItem(150)]

	for i in range(len(initialOffsets)):
		worker=Thread(target=_getAlbumsForArtist, name=str(i), args=(spotifyId,location,offsets,responses,i))
		worker.daemon = True
		worker.start()

	map(offsets.put,initialOffsets)
	offsets.join()
	while not responses.empty():
		albums.append(responses.get())

	return albums

def _getSongsFromAlbumsForArtist(spotifyId, artistId, albums, intervals, songs, songAdditions, recentFilter = True, i = None):
	today=datetime.date.today()
	spotify=spotipy.Spotify()
	while True:
		interval=intervals.get().key
		returnedAlbums=spotify.albums(interval)

		for album in returnedAlbums['albums']:
			recent=True
			if recentFilter:
				if album['release_date_precision'] == DAY:
					releaseDayFields=album['release_date'].split("-")
					releaseDay=datetime.date(int(releaseDayFields[0]),int(releaseDayFields[1]),int(releaseDayFields[2]))
					diff=today-releaseDay
					if diff.days>31:
						recent = False

				elif album['release_date_precision'] == MONTH:
					releaseDayFields=album['release_date'].split("-")
					if not (today.year==int(releaseDayFields[0]) and today.month==int(releaseDayFields[1])):
						recent = False

				else:
					recent = False

			if recent:
				image = album['images'][0]['url']
				for track in album['tracks']['items']:
					relevant = False
					artistNames = []
					for a in track['artists']:
						if a['id'] not in BAD_ARTISTS:
							artistNames.append(a['name'])
							if a['id'] == spotifyId:
								relevant = True
					if relevant:
						songName=track['name']
						song = Song(songName,artistNames)
						song.artistId=artistId

						for key in track['available_markets']:
							value={}
							value['id']=track['id']
							value['url']=track['external_urls']['spotify']
							value['uri']=track['uri']
							value['preview_url']=track['preview_url']
							value['image']=image
							value['album_id'] = album['id']
							song.addSpotifyKeyValue(key,value)

						key = song.getKey()

						if songs.checkForKey(key):
							songAdditions.put(QueItem(key,song))
						else:
							songs.put(QueItem(key,song))
		intervals.task_done()

def getSongsFromAlbumsForArtist(spotifyId, artistId, albums, recentFilter = True):
	"""
		Gets all songs for an array of album ids associated with a Spotify artists

		Params:
			spotifyId          (str) : artist's spotify id
			artistId (bson.ObjectId) : mongo id associated with the artist
			albums             (arr) : array of spotify album ids
			recentFilter      (bool) : indicates whether albums should be checked for recency

		Returns:
			(arr) : songs
	"""
	intervals=Queue()
	songQue=SetQueue()
	songAdditionsQue=Queue()

	for i in range(MAX_NUMBER_OF_THREADS):
		worker=Thread(target=_getSongsFromAlbumsForArtist, name=str(i), args=(spotifyId, artistId, albums, intervals, songQue,
																				songAdditionsQue, recentFilter, i))
		worker.daemon = True
		worker.start()


	count=0
	while(count<len(albums)):
		temp=[]
		plusTwenty=min(len(albums)-1,count+19)
		while count<=plusTwenty:
			temp.append(albums[count])
			count+=1
		intervals.put(QueItem(temp))

	intervals.join()

	songs = {}
	while not songQue.empty():
		item = songQue.get()
		songs[item.key] = item.value

	while not songAdditionsQue.empty():
		item = songAdditionsQue.get()
		if item.key in songs:
			song = songs[item.key]
			song.mergeSpotifyInfo(item.value)
			songs[item.key] = song

	print "got songs from an album from a specific artist perspective"
	return songs.values()





