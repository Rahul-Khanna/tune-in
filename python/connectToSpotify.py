import sys
import spotipy
import spotipy.util as util
import pdb
from ConfigParser import SafeConfigParser

parser= SafeConfigParser()

parser.read('config.ini')

secret = parser.get('spotify_info', 'secret')

key = parser.get('spotify_info', 'key')

url = parser.get('spotify_info','redirect')


scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

# pdb.set_trace()
token = util.prompt_for_user_token(username, scope,key,secret,url)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
else:
    print "Can't get token for", username