# from gevent import monkey
# monkey.patch_all()
import spotipy
import spotipy.util as util
from classModules import Song
from classModules import SetQueue
import datetime
from Queue import Queue
from threading import Thread
import sys

import pdb

maxNumberOfThreads=8

badArtists={
	"0LyfQWJT6nXafLPZqxe9Of" : 1
}

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

def _getAlbumsForArtist(spotifyId,location,q,r,f,i):
	spotify=spotipy.Spotify()
	while True:
		# print "Line 1 of loop, I am thread " + str(i)
		# print "The size of the queue is " + str(q.unfinished_tasks) + " thread: " + str(i)

		offset=q.get()
		# print "Thread Top : " +str(i)
		# print str(int(offset+len(returnedAlbums['items'])))
		# print q.unfinished_tasks
		# print q.qsize()
		# print "Thread Top : "+str(i)
		# print offset
		returnedAlbums=spotify.artist_albums(artist_id=str(spotifyId),country=location,limit=50,offset=offset)
		
		if len(returnedAlbums['items']):
			for album in returnedAlbums['items']:
				r.put(album['id'])
			sucess=q.put(int(offset+len(returnedAlbums['items'])))
			# if not sucess:
			# 	print "got in here"
				# q.task_done()
			# print "I put these items inside " + str(len(returnedAlbums['items'])) + " thread: " +str(i)

		q.task_done()
		# print "Thread : " +str(i)
		# print str(int(offset+len(returnedAlbums['items'])))
		# print q.unfinished_tasks
		# print q.qsize()
		# print "Thread : "+str(i)
		# print "Now the size of the queue is: "+ str(q.unfinished_tasks) + " thread: "+str(i)
		# print str(r.qsize()) + " thread:" +str(i)

		# if len(returnedAlbums['items']):
		# 	# print "put something into queue, thread: "+str(i)
			
			
		# 		print "got here"
				# offset=q.get()
				# print offset
				
		# else:
		# 	print "Thread is done: "+str(i)
		# 	print "Size of the queue is: " + str(q.unfinished_tasks) + " thread: " +str(i)
		# 	# f.put(i)
		

# for a given artist_id return a list of albumIds
def getAlbumsForArtist(spotifyId,location=None):
	albums=[]
	offsets=SetQueue()
	responses=SetQueue()
	finishes=Queue()
	initialOffsets=[0,50,100,150]

	for i in range(len(initialOffsets)):
		worker=Thread(target=_getAlbumsForArtist, name=str(i), args=(spotifyId,location,offsets,responses,finishes,i))
		worker.daemon = True
		worker.start()

	map(offsets.put,initialOffsets)
	# offsets.put(0)
	# offsets.put(50)
	# # offsets.put(100)
	# # offsets.put(150)
	# print offsets.unfinished_tasks
	# print offsets.qsize()
	# print "put tasks in queue"
	# i=0
	# while(i<2):
	# 	val = finishes.get()
	# 	i+=1
	# 	print str(i)
	offsets.join()
	while not responses.empty():
		albums.append(responses.get())

		# returnedAlbums=spotify.artist_albums(artist_id=str(spotifyId),country=location,limit=50,offset=len(albums))
		# # return returnedAlbums
		# if len(returnedAlbums['items'])>0:
		# 	for album in returnedAlbums['items']:
		# 		# for i in range(0,len(album['artists'])):
		# 		# 	names.append((int(i+1),album['artists'][i]['id'],album['artists'][i]['name']))
		# 		# 	if i==0 and str(spotifyId)!=str(album['artists'][i]['id']):
		# 		# 		names.append(album)
		# 		albums.append(album['id'])
		# else:
		# 	# with open("artsits","a+") as f:
		# 	# 	for tup in names:
		# 	# 		f.write(str(tup))
		# 	# 		f.write("\n")
		# 	# with open("albums","a+") as f:
		# 	# 	for i in albums:
		# 	# 		f.write(str(i))
		# 	# 		f.write("\n")
	print "got albums"
	return albums
	# sys.exit(0)

# albums is an array of ids
# artist is the spotify id of the artist
# return song array
def getSongsFromAlbumsForArtist(spotifyId,artistId,albums,recentFilter):
	spotify=spotipy.Spotify()
	count=0
	today=datetime.date.today()
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
			cont2=False
			if recentFilter:

				if album['release_date_precision']=="day":
					releaseDayFields=album['release_date'].split("-")
					releaseDay=datetime.date(int(releaseDayFields[0]),int(releaseDayFields[1]),int(releaseDayFields[2]))
					diff=today-releaseDay
					if diff.days<31:
						cont2=True

				if album['release_date_precision']=="month":
					releaseDayFields=album['release_date'].split("-")
					if today.year==int(releaseDayFields[0]) and today.month==int(releaseDayFields[1]):
						cont2=True
			else:
				cont2=True

			if cont2:
				image=album['images'][0]['url']
				for track in album['tracks']['items']:
					cont=False
					artistNames=[]
					for a in track['artists']:
						if a['id'] not in badArtists:
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
							value['image']=image
							songs[song.name+"-"+song.artistName].addSpotifyKeyValue(key,value)

		if count==len(albums)-1:
			print "got songs from an album from a specific artist perspective"
			return songs.values()





