from miniblog import app
import os

from datetime import datetime
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from werkzeug import secure_filename
from PIL import Image

from miniblog.db import get_db, init_db
from miniblog.watermarker import resize_image, image_watermark

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('SELECT title, text, image, music, posted FROM entries ORDER BY id DESC')
	entries = [dict(title=row[0], text=row[1], image=row[2], music=row[3], posted=row[4]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries = entries)

@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute("INSERT INTO entries (title, text, image, music, posted) \
                VALUES (?, ?, ?, ?, ?)", [request.form['title'], \
                  request.form['text'], request.form['image'], \
                  request.form['music'], datetime.now().strftime(
                                                     "%d.%m.%Y %H:%M")])
    db.commit()
    flash('New post was successfully added')
    return redirect(url_for('show_entries'))

# Cheking if files are in allowed list
def allowed_music(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in MUSIC_EXTENSIONS

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMAGE_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_music(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_MUSIC'], filename))
            return redirect(url_for('show_entries'))
        elif file and allowed_image(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_IMAGE'], filename))
            path = os.path.split(os.path.abspath(file.filename))[0]
            # Path to the folder with processed images.
            # Resizing image to 400 x 300 px
            new_filename = resize_image(os.path.join(app.config['UPLOAD_IMAGE'], filename), \
                                    400, 300, app.config['UPLOAD_IMAGE'])
            os.chdir(app.config['UPLOAD_IMAGE'])
            imagewatermark = "watermark.png"
            # Add a watermark to the upladed image
            image_watermark(new_filename, imagewatermark, app.config['UPLOAD_IMAGE'], 0.5)
            return redirect(url_for('show_entries'))
    return render_template('upload.html')
