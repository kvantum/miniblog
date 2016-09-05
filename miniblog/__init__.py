import os
from flask import Flask


# Configuration parameters 
APP_DIR=os.path.dirname(os.path.realpath(__file__))
DATABASE=os.path.join(APP_DIR, 'blog.db')
UPLOAD_MUSIC = os.path.join(APP_DIR, 'static/music')
UPLOAD_IMAGE = os.path.join(APP_DIR, 'static/image')
MUSIC_EXTENSIONS = set(['mp3'])
IMAGE_EXTENSIONS = set(['png', 'jpg'])
DEBUG = True
SECRET_KEY = 'averysecretkey'
USERNAME = 'admin'
PASSWORD = 'admin'

# Create our application
app = Flask(__name__)
app.config.from_object(__name__)

import miniblog.views
import miniblog.login_logout
import miniblog.db
import miniblog.watermarker
import miniblog.test


