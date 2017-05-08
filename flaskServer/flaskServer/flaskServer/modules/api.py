# from gevent import monkey
# monkey.patch_all()
import spotifyModule as spotify
import mongoModule as mongo
import classModules as objects
from bson import ObjectId
import sys
from ConfigParser import SafeConfigParser
import pdb
from Queue import Queue
from threading import Thread
parser= SafeConfigParser()

parser.read('config.ini')

def getFollowedArtistsForUsers(users):
	allArtists={}
	for user in users:
		temp = mongo.getArtists(user.following)
		for artist in temp:
			if artist._id not in allArtists:
				allArtists[artist._id] = artist

	print "got artists for users"
	return allArtists.values()

def loginCall(connection,id,topArtists,location=None):
	try :
		if connection == "spotify" :
			artists=[]
			for artist in topArtists:
				artists.append(objects.Artist(name=artist['name'],spotifyId=artist['id'],numberOfUsers=1))

			artistResults=mongo.insertArtists(artists)
			user=objects.User(id=1,possible=artistResults['ids'],following=artistResults['ids'])
			user.spotifyInfo["id"] = id
			userId=mongo.createUser(user)['id']

			for artist in artistResults['artists']:
				albums = spotify.getAlbumsForArtist(artist, location="US")
				
				songQue = Queue()
				threadName = str(artist.spotifyId)+"_1"
				worker1 = Thread(target=spotify.getSongsFromAlbumsForArtist, name=threadName, args=(artist.spotifyId, artist._id, albums.keys(), songQue, True))
				worker1.start()
				
				threadName = str(artist.spotifyId)+"_2"
				worker2 = Thread(target=mongo.updateAlbumsForArtist, name=threadName, args=(artist, albums))
				worker2.start()
				
				worker1.join()
				songs = []
				while not songQue.empty():
					songs.append(songQue.get())
				if len(songs):
					songResults=mongo.insertSongs(songs)
					mongo.addSongsToUser(songResults['ids'], userId)

				worker2.join()


		return "Success"
	except:
		return "False"
