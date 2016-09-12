import os

from flask import abort, flash, g, redirect, render_template, request, session, url_for  
from miniblog.config.config import USERNAME, PASSWORD
from miniblog.models import save_entry, upload, get_entries

def show_entries():
	return render_template('show_entries.html', entries = get_entries())

def add_entry():
    if not session.get('logged_in'):
		flash('You should be logged in.')
		abort(401)
		return redirect(url_for('show_entries'))
    save_entry(request.form['title'], request.form['text'], \
               request.form['image'], request.form['music'])
    flash('New post was added successfully.')
    return redirect(url_for('show_entries'))
    
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != USERNAME) or (
            request.form['password'] != PASSWORD):
			   error = 'Invalid password or username.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error = error)

def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('show_entries'))

def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		upload(file)
		os.chdir('/home/kvm/code/Blog/')
		return redirect(url_for('show_entries'))
	return render_template('upload.html')
	
		
