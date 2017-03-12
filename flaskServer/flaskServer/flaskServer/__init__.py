from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import subprocess
import sys
# sys.path.append("/Users/rahulkhanna/tune-in/flaskServer/flaskServer/flaskServer/modules")
sys.path.append("/home/dev/web/www/flaskServer/flaskServer/modules")
from api import *
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
	if not request.json or not 'user' in request.json:
		abort(400)
	value = loginCall(request.json['user'])
	if value == "Success":
		return jsonify({'status' : 'success',  'user' : request.json['user']})
	else:
		return jsonify({'status' : 'false', 'user' : request.json['user']})
if __name__ == "__main__":
	app.run(debug = True)
