import ConfigParser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(path,'config.cfg'))

DATABASE = config.get('PATH', 'database')
UPLOAD_FOLDER = config.get('PATH', 'upload_folder')
WATERMARK_PATH = config.get('PATH', 'watermark_path')
USERNAME = config.get('AUTH', 'username')
PASSWORD = config.get('AUTH', 'password')
SECRET_KEY = config.get('OTHER','secret_key')
DEBUG = config.get('OTHER', 'debug')

MUSIC_EXTENSIONS = set(['mp3'])
IMAGE_EXTENSIONS = set(['png', 'jpg', 'bmp'])
