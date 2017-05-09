import time
from bson import ObjectId
import pdb
from Queue import Queue

class Song:

	def __init__(self, name, artistNames, id=None, artistId=None, timeStamp=None, soundCloudInfo=None, spotifyInfo=None, duration=None):

		self.name=name
		self.artistNames=artistNames

		if id:
			self._id=id
		else:
			self._id=-1

		if artistId:
			self.artistId=artistId
		else:
			self.artistId=-1

		if timeStamp:
			self.timeStamp=timeStamp
		else:
			self.timeStamp=time.time()

		if soundCloudInfo:
			self.soundCloudInfo=soundCloudInfo
		else:
			self.soundCloudInfo={}

		if spotifyInfo:
			self.spotifyInfo=spotifyInfo
		else:
			self.spotifyInfo={}

		if duration:
			self.duration = duration
		else:
			self.duration = -1


	# only here because you are manipulating a data structure
	def addSpotifyKeyValue(self,key,value):
		self.spotifyInfo[key]=value

	def addSoundCloudKeyValue(self,key,value):
		self.soundCloudInfo[key]=value

	def getKey(self):
		key = self.name
		for artist in self.artistNames:
			key+=":"
			key+=artist

		return key

	def __eq__(self, other):
		if self.getKey() == other.getKey():
			return True
		return False

	def mergeSpotifyInfo(self, other):
		for key in other.spotifyInfo:
			self.spotifyInfo[key] = other.spotifyInfo[key]

	def getObjectForInsert(self):
		output={
			"name" : self.name,
			"artistNames" : self.artistNames,
			"artistId" : self.artistId,
			"spotifyInfo" : self.spotifyInfo,
			"soundCloudInfo" : self.soundCloudInfo,
			"timeStamp" : self.timeStamp,
			"duration" : self.duration
		}

		return output

	def __repr__(self):
		output={
			"id" : self._id,
			"name" : self.name,
			"artistNames" : self.artistNames,
			"artistId" : self.artistId,
			"spotifyInfo" : self.spotifyInfo,
			"soundCloudInfo" : self.soundCloudInfo,
			"timeStamp" : self.timeStamp,
			"duration" : self.duration
		}

		return str(output)

def convertJsonToSong(json):

	song=Song(json['name'],json['artistNames'])

	if '_id' in json:
		song._id = json['_id']

	if 'artistId' in json:
		song.artistId = json['artistsId']

	if 'spotifyInfo' in json:
		song.spotifyInfo = json['spotifyInfo']

	if 'soundCloudInfo' in json:
		song.soundCloudInfo = json['soundCloudInfo']

	if 'timeStamp' in json:
		song.timeStamp = json['timeStamp']

	if 'duration' in json:
		song.duration = json['duration']

	return song


class Artist:

	def __init__(self,name,id=None,timeStamp=None,soundCloudId=None,spotifyId=None,numberOfUsers=None):

		self.name=name

		if id:
			self._id=id
		else:
			self._id=-1

		if timeStamp:
			self.timeStamp=timeStamp
		else:
			self.timeStamp=time.time()

		if soundCloudId:
			self.soundCloudId=soundCloudId
		else:
			self.soundCloudId=-1

		if spotifyId:
			self.spotifyId=spotifyId
		else:
			self.spotifyId=-1

		if numberOfUsers:
			self.numberOfUsers=numberOfUsers
		else:
			self.numberOfUsers=-1

	def getObjectForInsert(self):
		output={
			"name":self.name,
			"spotifyId":self.spotifyId,
			"soundCloudId":self.soundCloudId,
			"timeStamp":self.timeStamp,
			"numberOfUsers":self.numberOfUsers
		}

		return output

	def __repr__(self):
		output={
			"id":self._id,
			"name":self.name,
			"spotifyId":self.spotifyId,
			"soundCloudId":self.soundCloudId,
			"timeStamp":self.timeStamp,
			"numberOfUsers":self.numberOfUsers
		}

		return str(output)

def convertJsonToArtist(json):

	artist=Artist(json['name'])

	if '_id' in json:
		artist._id=json['_id']

	if 'spotifyId' in json:
		artist.spotifyId=json['spotifyId']

	if 'soundCloudId' in json:
		artist.soundCloudId=json['soundCloudId']

	if 'timeStamp' in json:
		artist.timeStamp=json['timeStamp']

	if 'numberOfUsers' in json:
		artist.numberOfUsers=json['numberOfUsers']

	return artist


class User:
	def __init__(self,id,soundCloudInfo=None,spotifyInfo=None,percOfTopArtists=100,possible=None,following=None,newSongs=None,oldSongs=None,savedSongs=None,timeStamp=None):
		self._id=id

		if soundCloudInfo:
			self.soundCloudInfo=soundCloudInfo
		else:
			self.soundCloudInfo={}

		if spotifyInfo:
			self.spotifyInfo=spotifyInfo
		else:
			self.spotifyInfo={}

		if percOfTopArtists:
			self.percOfTopArtists=percOfTopArtists

		if possible:
			self.possible=possible
		else:
			self.possible=[]

		if following:
			self.following=following
		else:
			self.following=[]

		if newSongs:
			self.newSongs=newSongs
		else:
			self.newSongs=[]

		if oldSongs:
			self.oldSongs=oldSongs
		else:
			self.oldSongs=[]

		if savedSongs:
			self.savedSongs=savedSongs
		else:
			self.savedSongs=[]

		if timeStamp:
			self.timeStamp=timeStamp
		else:
			self.timeStamp=time.time()

	def addArtistIdsToPossible(self,artistIds):
		self.possible.append(artistIds)

	def removeArtistIdsFromPossible(self,artistIds):
		self.possible=list(set(self.possible)-set(artistIds))


	def addArtistIdsToFollowing(self,artistIds):
		self.following.append(artistIds)

	def removeArtistIdsFromFollowing(self,artistIds):
		self.following=list(set(self.following)-set(artistIds))


	def addSongIdsToNewSongs(self,SongIds):
		self.newSongs.append(SongIds)

	def removeSongIdsFromNewSongs(self,SongIds):
		self.newSongs=list(set(self.newSongs)-set(SongIds))


	def addSongIdsToOldSongs(self,SongIds):
		self.oldSongs.append(SongIds)

	def removeSongIdsFromOldSongs(self,SongIds):
		self.oldSongs=list(set(self.oldSongs)-set(SongIds))


	def addSongIdsToSavedSongs(self,songIds):
		self.savedSongs.append(songIds)

	def removeSongIdsFromSavedSongs(self,songIds):
		self.savedSongs=list(set(self.savedSongs)-set(songIds))

	def getObjectForInsert(self):
		output={
			"soundCloudInfo":self.soundCloudInfo,
			"spotifyInfo":self.spotifyInfo,
			"percOfTopArtists":self.percOfTopArtists,
			"possible":self.possible,
			"following":self.following,
			"newSongs":self.newSongs,
			"oldSongs":self.oldSongs,
			"savedSongs":self.savedSongs,
			"timeStamp":self.timeStamp
		}

		return output

	def __repr__(self):
		output={
			"id": self._id,
			"soundCloudInfo":self.soundCloudInfo,
			"spotifyInfo":self.spotifyInfo,
			"percOfTopArtists":self.percOfTopArtists,
			"possible":self.possible,
			"following":self.following,
			"newSongs":self.newSongs,
			"oldSongs":self.oldSongs,
			"savedSongs":self.savedSongs,
			"timeStamp":self.timeStamp
		}

		return str(output)

def convertJsonToUser(json):

	user=User(json['_id'])

	if 'soundCloudInfo' in json:
		user.soundCloudInfo=json['soundCloudInfo']

	if 'spotifyInfo' in json:
		user.spotifyInfo=json['spotifyInfo']

	if 'percOfTopArtists' in json:
		user.percOfTopArtists=json['percOfTopArtists']

	if 'possible' in json:
		user.possible=json['possible']

	if 'following' in json:
		user.following=json['following']

	if 'newSongs' in json:
		user.newSongs=json['newSongs']

	if 'oldSongs' in json:
		user.oldSongs=json['oldSongs']

	if 'savedSongs' in json:
		user.savedSongs=json['savedSongs']

	if 'timeStamp' in json:
		user.timeStamp=json['timeStamp']

	return user

class SetQueue(Queue):

	def __init__(self, maxsize=0):
		Queue.__init__(self, maxsize)
		self.all_items = {}

	def put(self, item):
		if item.key not in self.all_items:
			Queue.put(self, item) 
			self.all_items[item.key] = item.value

	def get(self):
		item = Queue.get(self)
		if type(item.value) == int:
			if item.value == 1:
				return item.key

		return item

	def checkForKey(self, key):
		if key in self.all_items:
			return True

		return False
	

class QueItem():

	def __init__(self, key, value=1):
		self.key = key
		self.value = value



