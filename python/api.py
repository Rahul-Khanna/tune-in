import spotifyModule as spotify
import mongoModule as mongo
from classModules import Song as song
from bson import ObjectId
import sys
from ConfigParser import SafeConfigParser
import pdb
parser= SafeConfigParser()

parser.read('config.ini')


def loginCall(userId,location=None):
	try :
		user = mongo.getUser(userId)
		artists = mongo.getFollowedArtistsForUsers(user)

		for artist in artists:
			albums=spotify.getAlbumsForArtist(artist.spotifyId,location="US")
			songs=spotify.getSongsFromAlbumsForArtist(artist.spotifyId,artist._id,albums,True)
			ids=mongo.insertSongs(songs)
			mongo.addSongsToUser(ids,userId)

		return "Success"
	except:
		return "False"
