#!/usr/bin/python
import sys
import logging
activate_this = '/var/www/flaskServer/flaskServer/clouds/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskServer/")

from flaskServer import app as application
#application.secret_key= 'Add your secret key'
