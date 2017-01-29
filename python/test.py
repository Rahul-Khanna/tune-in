import spotifyModule as spotify
import mongoModule as mongo
from classModules import Song as song
from bson import ObjectId
import sys
from ConfigParser import SafeConfigParser
import pdb
parser= SafeConfigParser()

parser.read('config.ini')

secret = parser.get('spotify_info', 'secret')

key = parser.get('spotify_info', 'key')

url = parser.get('spotify_info','redirect')

server=parser.get('main','server')

database=parser.get('main','database')

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
   username = parser.get('spotify_info','jacksUserName')

token=spotify.generateUserToken(username,scope,key,secret,url)


if token:
	notifications={}
	users=mongo.getUsers(server,database)
	artists=mongo.getFollowedArtistsForUsers(server,database,users)
	# for artist in mongo.getFollowedArtistsForUsers(mongo.getUsers(server,database)):

	# this process is to allow us to get songs for every artist in our database
	# it can also be used to get
	for artist in artists:
		albums=spotify.getAlbumsForArtist(artist.spotifyId,location="US")
		songs=spotify.getSongsFromAlbumsForArtist(artist.spotifyId,artist._id,albums)
		# with open("temp","w") as f:
		# 	for song in songs:
		# 		f.write(str(song))
		# 		f.write("\n")
		pdb.set_trace()
		ids=mongo.insertSongs(server,database,songs)
		mongo.addSongsToUser(server,database,ids,users[0]._id)


