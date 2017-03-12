from pymongo import *
import requests
from bson import ObjectId
from classModules import *
import pdb
from ConfigParser import SafeConfigParser
import pdb
parser= SafeConfigParser()

# parser.read('/Users/rahulkhanna/tune-in/flaskServer/flaskServer/flaskServer/modules/config.ini')
parser.read('/home/dev/web/www/flaskServer/flaskServer/modules/config.ini')
serverName = parser.get('mongo','server')
database = parser.get('mongo','database')
loginUser = parser.get('mongo','user')
loginPsd = parser.get('mongo','pwd')


def getUser(userId):
	user=None
	try:
		client = MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		userId=ObjectId(str(userId))
		print type(userId)
		try:
			user=db["users"].find({"_id":userId})
		except:
			print "lol"
	finally:
		client.close()
	user=convertJsonToUser(user[0])
	print str(user)
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

	return users

def getArtist(artistId):
	artist=None
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		artist=db["artists"].find({"id":artistId})
	finally:
		client.close()

	artist=convertJsonToArtist(artist)

	return artist

def getArtists(ids=None):
	artists=[]
	temp=None
	print "hi"
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		print "hi"
		try :
			if ids:
				print "ids"
				temp=db["artists"].find({"_id":{"$in": ids}})
				print "ids2"
			else:
				temp=db["artists"].find()
		except :
			print "nope"
	finally:
		client.close()

	for artist in temp:
		artists.append(convertJsonToArtist(artist))

	print str(artists)

	if len(artists) > 0:
		return artists

	print "no artists in db"
	return

def insertSongs(songs):
	ids=[]
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		songCollection=db["songs"]
		for song in songs:
			temp=songCollection.insert_one(song.getObjectForInsert()).inserted_id
			song._id=temp
			ids.append(temp)
	finally:
		client.close()

	return ids

def addSongsToUser(songIds,userId):
	try:
		client=MongoClient(serverName,27017)
		db=client[database]
		db.authenticate(loginUser,loginPsd)
		for songId in songIds:
			# print type(notifId)
			db["users"].update_one({"_id": userId},{"$push":{"newSongs":songId}})
	finally:
		client.close()

def getFollowedArtistsForUsers(users):
	allArtists={}
	for user in users:
		temp=getArtists(user.following)
		for artist in temp:
			if artist._id not in allArtists:
				allArtists[artist._id]=artist

	return allArtists.values()



