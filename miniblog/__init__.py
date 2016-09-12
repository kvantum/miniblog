from flask import Flask
from config.config import DATABASE, SECRET_KEY, USERNAME, PASSWORD, DEBUG, UPLOAD_FOLDER, MUSIC_EXTENSIONS, IMAGE_EXTENSIONS, WATERMARK_PATH
import os


app = Flask(__name__, static_url_path = '/static')

from miniblog import models, views

APP_DIR=os.path.dirname(os.path.realpath(__file__))
print(APP_DIR)
app.config.update(DATABASE = DATABASE,
                  SECRET_KEY = SECRET_KEY,
                  USERNAME = USERNAME,
                  PASSWORD = PASSWORD,
                  DEBUG = DEBUG,
                  UPLOAD_FOLDER = UPLOAD_FOLDER,
                  MUSIC_EXTENSIONS = MUSIC_EXTENSIONS,
                  IMAGE_EXTENSIONS = IMAGE_EXTENSIONS,
                  WATERMARK_PATH = WATERMARK_PATH
                  )

app.add_url_rule('/', view_func = views.show_entries, methods=['GET'])
app.add_url_rule('/login', view_func = views.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func = views.logout, methods=['GET'])
app.add_url_rule('/add', view_func = views.add_entry, methods=['POST'])
app.add_url_rule('/upload', view_func = views.upload_file, methods=['GET', 'POST'])
