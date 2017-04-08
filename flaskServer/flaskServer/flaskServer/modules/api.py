from gevent import monkey
monkey.patch_all()
import spotifyModule as spotify
import mongoModule as mongo
import classModules as objects
from bson import ObjectId
import sys
from ConfigParser import SafeConfigParser
import pdb
parser= SafeConfigParser()

parser.read('config.ini')


def loginCall(connection,id,topArtists,location=None):
	try :
		if connection == "spotify" :
			artists=[]
			for artist in topArtists:
				artists.append(objects.Artist(name=artist['name'],spotifyId=artist['id'],numberOfUsers=1))

			artistResults=mongo.insertArtists(artists)
			user=objects.User(id=1,possible=artistResults['ids'],following=artistResults['ids'])
			user.spotifyInfo["id"] = id
			user=mongo.createUser(user)['user']

			for artist in artistResults['artists']:
				albums=spotify.getAlbumsForArtist(artist.spotifyId,location="US")
				songs=spotify.getSongsFromAlbumsForArtist(artist.spotifyId,artist._id,albums,True)
				if len(songs):
					songResults=mongo.insertSongs(songs)
					mongo.addSongsToUser(songResults['ids'],user._id)

		return "Success"
	except:
		return "False"
