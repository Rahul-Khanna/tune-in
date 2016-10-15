from pymongo import MongoClient
import requests
import random
import datetime
import string

def generateRadomString(N):
	temp=''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(N))
	return temp

def selectRandomIds(arrayOfIds,N):
	temp=[]

	size = len(arrayOfIds)
	i=0

	while size:
		size = size - 1
		index = random.randint(0, size)
		elem = arrayOfIds[index]
		arrayOfIds[index] = arrayOfIds[size]
		temp.append(elem)
		i+=1
		if i>N:
			break

	return temp

def attachScores(arrayOfIds):
	temp=[]
	for i in range(0,len(arrayOfIds)):
		temp.append((arrayOfIds[i],random.randrange(0,1000)))

	return temp



client = MongoClient('localhost',27017)

db = client.jacksLittleProject

db.users.drop()
db.artists.drop()
db.notifications.drop()
db.songs.drop()

print "cleared database"


users = db.users

artists = db.artists

notifications = db.notifications

songs = db.songs

# i=0
# while i<10:
# 	requestString="http://api.soundcloud.com/users/"+str(random.randint(1,10000))+"?client_id=bec141287e6a2a78f03e036e0e5f4520"
# 	try:
# 		r=requests.get(requestString)
# 		print r.json()
# 		break
# 	except Exception, e:
# 		print e

artistIds=[]

for i in range(0,50):
	artist= {
		"timeStamp" : datetime.datetime.now(),
		"numberOfUsers" : random.randint(0,10),
		"name" : generateRadomString(16)
	}
	artistIds.append(artists.insert_one(artist).inserted_id)

print ("inserted artists")

notificationIds=[]

for i in range(0,500):

	notification= {
		"spotifyInfo" : {
			"id" : generateRadomString(64),
			"url" : generateRadomString(32)
		},

		"soundcloudInfo" : {
			"id" : generateRadomString(64),
			"url" : generateRadomString(32)
		},

		"artistId" : random.choice(artistIds),

		"timeStamp" : datetime.datetime.now()
	}

	notificationIds.append(notifications.insert_one(notification).inserted_id)

print ("inserted notifications")

songIds=[]

for i in range(0,200):

	song= {
		"spotifyInfo" : {
			"id" : generateRadomString(64),
			"url" : generateRadomString(32)
		},

		"soundcloudInfo" : {
			"id" : generateRadomString(64),
			"url" : generateRadomString(32)
		},

		"artistId" : random.choice(artistIds),

		"name" :generateRadomString(16),

		"timeStamp" : datetime.datetime.now()
	}

	songIds.append(songs.insert_one(song).inserted_id)

print ("inserted songs")

for i in range(0,10):

	percOfTopArtists=random.randint(0,100)

	possibleArtists=attachScores(selectRandomIds(artistIds,random.randint(1,len(artistIds))))
	possibleArtists.sort(key=lambda x: x[1],reverse=True)

	following=[]
	for i in range(0,int((percOfTopArtists/100.0)*len(possibleArtists))):
		following.append(possibleArtists[i][0])

	user={
		"spotifyInfo": {
			"token" : generateRadomString(64),
			"email" : generateRadomString(16),
			"userName" : generateRadomString(16),
			"active" : random.choice([True, False])
		},
		"soundcloudInfo": {
			"token" : generateRadomString(64),
			"email" : generateRadomString(16),
			"userName" : generateRadomString(16),
			"active" : random.choice([True, False])
		},
		"percOfTopArtists" : percOfTopArtists,

		"possibleArtists" : possibleArtists,

		"following" : following,

		"newNotifications" : selectRandomIds(notificationIds,random.randint(0,15)),

		"oldNotifications" : selectRandomIds(notificationIds,random.randint(0,100)),

		"saveSongs" : selectRandomIds(songIds,random.randint(0,30)),

		"timeStamp" : datetime.datetime.now(),

		"timeStamp" : datetime.datetime.now()

	}

	users.insert_one(user).inserted_id

print ("inserted users")

# artistsId = artists.insert_one(artist).inserted_id

# print artistsId
