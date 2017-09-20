from flask import render_template, flash, redirect
from app import app
from .forms import *
from .extract import Extraction
from flask import request
from flask import send_file

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

def save_csv_on_server(urls):
	extraction = Extraction()
	extraction.run(urls)
	
	
@app.route('/download', methods=['POST'])
def download():
    urls = None
    if request.method == 'POST':
        urls = request.form['urls']
        save_csv_on_server(urls)
        return send_file('static/sites_metadata.csv',
                     mimetype='text/csv',
                     attachment_filename='sites_metadata.csv',
                     as_attachment=True)
    else:
	    abort(401)
    return render_template('base.html',
                           title='Home', urls=urls)
