from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import subprocess
import sys
# sys.path.append("/Users/rahulkhanna/tune-in/flaskServer/flaskServer/flaskServer/modules")
sys.path.append("/home/dev/web/www/flaskServer/flaskServer/modules")
import api
app = Flask(__name__)

@app.route("/")
def hello():
	# cmd = ["python","/Users/rahulkhanna/tune-in/flaskServer/flaskServer/flaskServer/test.py"]
	cmd = ["python","/home/dev/web/www/flaskServer/flaskServer/test.py"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	out,err = p.communicate()
	print out
	#return err
	return out
	#return "Hello World"
	#return "hi"+str(out)

@app.route("/tune_in/api/v1.0/login", methods=['POST'])
def user_log_in():
	if not request.json or not 'user_id' in request.json \
	or not 'topArtists' in request.json:
		abort(400)
	connection=request.json['user_id'].split("|")[1].lower()
	user_name=request.json['user_id'].split("|")[2].lower()
	value = api.loginCall(connection,user_name,request.json['topArtists']["items"])
	if value == "Success":
		return jsonify({'status' : 'success',  'user' : user_name})
	else:
		return jsonify({'status' : 'false', 'user' : user_name})
if __name__ == "__main__":
	app.run(debug = True)
