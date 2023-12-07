from flask import Blueprint, render_template, abort

from databaseconnections import media_path
from app import socketio
from databaseconnections import biblioteca, notizie, galleria, file_biblioteca, file_galleria

frontend = Blueprint('frontend', __name__, template_folder='../frontend', static_folder='../frontend', url_prefix='/frontend')


@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('biblioteca/<path:path>')
def statc_file_biblioteca(path):
    return file_biblioteca(path)


@frontend.route('galleria/<path:path>')
def static_file_galleria(path):
    return file_galleria(path)


@frontend.route('/<path:path>')
def static_file(path):
    return frontend.send_static_file(path)


@socketio.on('connect', namespace='/frontend')
def connect():
    aggiorna_biblioteca()
    aggiorna_notizie()
    aggiorna_galleria()


# ! Todo: al momento mandiamo tutti i dati, anche quelli nascosti.
def aggiorna_biblioteca():
    socketio.emit('biblioteca', biblioteca.data, namespace='/frontend')


def aggiorna_notizie():
    socketio.emit('notizie', notizie.data, namespace='/frontend')


def aggiorna_galleria():
    socketio.emit('galleria', galleria.data, namespace='/frontend')
