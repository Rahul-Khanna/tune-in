# from gevent import monkey
# monkey.patch_all()
from pymongo import *
import requests
from bson import ObjectId
from classModules import *
import pdb
from ConfigParser import SafeConfigParser
parser= SafeConfigParser()
from Queue import Queue
from threading import Thread

# parser.read('/Users/rahulkhanna/Documents/tune-in/flaskServer/flaskServer/flaskServer/modules/config.ini')
parser.read('/home/dev/web/www/flaskServer/flaskServer/modules/config.ini')
serverName = parser.get('mongo','server')
database = parser.get('mongo','database')
loginUser = parser.get('mongo','user')
loginPsd = parser.get('mongo','pwd')

MAX_NUMBER_OF_THREADS = 8

def getUser(userId):
	user=None
	try:
		client = MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		userId=ObjectId(str(userId))
		# print type(userId)
		user=db["users"].find_one({"_id":userId})
	finally:
		client.close()
	user=convertJsonToUser(user[0])
	print "got user"
	return user


def getUsers(ids=None):
	users=[]
	temp=None
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		if ids:
			temp=db["users"].find({"_id": {"$in" : ids}})
		else:
			temp=db["users"].find()
	finally:
		client.close()

	for user in temp:
		users.append(convertJsonToUser(user))

	print "got users"
	return users

def createUser(user):
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		userCollection=db["users"]
		temp=userCollection.insert_one(user.getObjectForInsert()).inserted_id
		user._id=temp
	finally:
		print "inserted user"
		client.close()

	return {'user' : user, 'id' : temp}


def getArtist(artistId):
	artist=None
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		artist=db["artists"].find_one({"_id":artistId})
	finally:
		client.close()

	artist=convertJsonToArtist(artist)

	print "got artist"
	return artist

def getArtists(ids=None):
	artists=[]
	temp=None
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		if ids:
			temp=db["artists"].find({"_id":{"$in": ids}})
		else:
			temp=db["artists"].find()
	finally:
		client.close()

	for artist in temp:
		artists.append(convertJsonToArtist(artist))

	if len(artists) > 0:
		print "got artists"
		return artists

	print "no artists in db"
	return

def insertArtists(artists):
	ids=[]
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		artistCollection=db["artists"]
		temp=[]
		for artist in artists:
			temp.append(artist.getObjectForInsert())
		result=artistCollection.insert_many(temp).inserted_ids
		for i in range(len(result)):
			artists[i]._id=result[i]
			ids.append(result[i])
	finally:
		print "inserted artists"
		client.close()

	return {'artists' : artists, 'ids' : ids}

def insertSongs(songs):
	ids=[]
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		songCollection=db["songs"]
		temp=[]
		for song in songs:
			temp.append(song.getObjectForInsert())

		result=songCollection.insert_many(temp).inserted_ids

		for i in range(len(result)):
			songs[i]._id=result[i]
			ids.append(result[i])

	finally:
		print "inserted songs"
		client.close()
	return {'songs' : songs, 'ids' : ids}

def _addSongsToUser(userId, songs, i=None):
	try:
		client = MongoClient(serverName,27017)
		db = client[database]
		db.authenticate(loginUser,loginPsd)
		userId = ObjectId(str(userId))
		while True:
			songId=songs.get()
			db["users"].update_one({"_id": userId},{"$push":{"newSongs":songId}})
			songs.task_done()
	finally:
		client.close()

def addSongsToUser(songIds, userId):
	songs=Queue()
	for i in range(MAX_NUMBER_OF_THREADS):
		worker=Thread(target=_addSongsToUser, name=str(i), args=(userId, songs, i))
		worker.daemon = True
		worker.start()

	for songId in songIds:
		songs.put(songIds)
	
	songs.join()
	print "added songs to a user"
	return True

def updateAlbumsForArtist(artist, newAlbums):
	try:
		client = MongoClient(serverName,27017)
		db = client[database]
		db.authenticate(loginUser,loginPsd)
		artistId = ObjectId(str(artist._id))
		albums = db["artists"].find_one({"_id":artistId})["spotifyAlbums"]
		for albumId in newAlbums:
			if albumId  not in albums:
				albums[albumId] = {}
				artist.spotifyAlbums[albumId]={}

			for regionKey in newAlbums[albumId]:
				if regionKey not in albums[albumId]:
					albums[albumId][regionKey] = 1
					artist.spotifyAlbums[albumId][regionKey]=1

		db["artists"].update_one({"_id":artistId}, {"$set":{"spotifyAlbums":albums}})

	finally:
		client.close()








