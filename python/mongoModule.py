from pymongo import *
import requests
from bson import ObjectId
from classModules import *
import pdb

def getUser(serverName,databaseName,userId):
	user=None
	try:
		client = MongoClient(serverName,27017)
		db=client[databaseName]
		user=db["users"].find({"_id":userId})
	finally:
		client.close()

	user=convertJsonToUser(user)

	return user


def getUsers(serverName,databaseName,ids=None):
	users=[]
	temp=None
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		print("connected")
		if ids:
			temp=db["users"].find({"_id": {"$in" : ids}})
		else:
			temp=db["users"].find()
	finally:
		client.close()

	for user in temp:
		users.append(convertJsonToUser(user))

	return users

def getArtist(serverName,databaseName,artistId):
	artist=None
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		artist=db["artists"].find({"id":artistId})
	finally:
		client.close()

	artist=convertJsonToArtist(artist)

	return artist

def getArtists(serverName,databaseName,ids):
	artists=[]
	temp=None
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		print("connected")
		if ids:
			temp=db["artists"].find({"_id":{"$in": ids}})
		else:
			temp=db["artists"].find()
	finally:
		client.close()

	for artist in temp:
		artists.append(convertJsonToArtist(artist))

	return artists

def insertSongs(serverName,databaseName,songs):
	ids=[]
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		songCollection=db["songs"]
		for song in songs:
			temp=songCollection.insert_one(song.getObjectForInsert()).inserted_id
			song._id=temp
			ids.append(temp)
	finally:
		client.close()

	return ids

def insertNotifications(serverName,databaseName,notifications):
	ids=[]
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		notifCollection=db["notifications"]
		for notif in notifications:
			ids.append(notifCollection.insert_one(eval(str(notif))).inserted_id)
	finally:
		client.close()

	return ids

def addSongsToUser(serverName,databaseName,songIds,userId):
	try:
		client=MongoClient(serverName,27017)
		db=client[databaseName]
		for songId in songIds:
			# print type(notifId)
			db["users"].update_one({"_id": userId},{"$push":{"newSongs":songId}})
	finally:
		client.close()

def getFollowedArtistsForUsers(serverName,databaseName,users):
	allArtists={}
	for user in users:
		temp=getArtists(serverName,databaseName,user.following)
		for artist in temp:
			if artist._id not in allArtists:
				allArtists[artist._id]=artist

	return allArtists.values()



