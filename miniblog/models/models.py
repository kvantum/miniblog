import os
import sqlite3
from datetime import datetime
from flask import flash, g
from werkzeug import secure_filename

from miniblog.config.config import DATABASE, UPLOAD_FOLDER, MUSIC_EXTENSIONS, IMAGE_EXTENSIONS, USERNAME, PASSWORD
from miniblog.services.watermarker import resize_image, image_watermark

def init_db():
	"""
	Initializes the database.
	"""
	db = get_db()
	with open(os.path.dirname(DATABASE, 'schema.sql'), mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

def connect_db():
    """
    Connects to the specific database.
    """
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    try:
        g.sqlite_db
    except AttributeError:
        g.sqlite_db = connect_db()
    finally:
        return g.sqlite_db

def get_entries():
    """
    Read entries from the database.
    """
    db = get_db()
    cur = db.execute('SELECT title, text, image, music, posted FROM entries ORDER BY id DESC')
    entries = [dict(title=row[0], text=row[1], image=row[2], music=row[3], posted=row[4]) for row in cur.fetchall()]
    db.close()
    return entries

def save_entry(title, text, image, music):
    """
    Add an entry to the database.
    """
    db = get_db()
    db.execute('INSERT INTO entries (title, text, image, music, posted) \
               VALUES (?, ?, ?, ?, ?)',[title, text, image, music, \
               datetime.now().strftime("%d.%m.%Y %H:%M")])
    db.commit()
    db.close()

# Cheking if files are in allowed list
def allowed_music(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in MUSIC_EXTENSIONS

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMAGE_EXTENSIONS

def upload(file):
    if file and allowed_music(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, 'music/', filename))
        flash("The audio file has been uploaded successfully.")
        return True
    elif file and allowed_image(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, 'image/', filename))
        path = os.path.split(os.path.abspath(file.filename))[0]
        # Path to the folder with processed images.
        # Resizing image to 400 x 300 px
        new_filename = resize_image(os.path.join(
        UPLOAD_FOLDER, 'image/', filename), 400, 300, \
        os.path.join(UPLOAD_FOLDER, 'image/'))
        os.chdir(os.path.join(UPLOAD_FOLDER, 'image/'))
        imagewatermark = 'watermark.png'
        # Add a watermark to the uploaded image
        image_watermark(new_filename, imagewatermark, os.path.join(
                                    UPLOAD_FOLDER, 'image/'), 0.5)
        flash("The image has been uploaded successfully.")
        return True
    else:
        msg = "You can upload a file only with allowed extensions."
        flash(msg)
        return False
