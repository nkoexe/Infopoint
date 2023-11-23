from flask import Blueprint, render_template, abort

from .databaseconnections import m

frontend = Blueprint('frontend', __name__, template_folder='../frontend')

frontend.route('/')
def index():
    return render_template('index.html')


@app.route('/galleria/<path:filename>')
def media(filename):
    return send_from_directory(media_path, filename)