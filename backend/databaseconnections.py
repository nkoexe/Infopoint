"""
Connessioni da database a backend / frontend
"""

<<<<<<< HEAD
from flask import send_file
from .app import socketio
=======
from app import socketio
>>>>>>> 17c96d17e4f68b4f0ed86536f645590458a30aba
from database import BibliotecaDB, NotizieDB, GalleriaDB, DATABASEPATH as media_path


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()


def aggiorna_biblioteca():
    socketio.emit('biblioteca', biblioteca.data)

def file(cartella, nome_file):
    if not isinstance(nome_file, str):
        raise TypeError('Nome del file da mandare deve essere una stringa.')

<<<<<<< HEAD
    assert '..' not in nome_file  # idk non succede ma se succede almeno nessuno fa danni

    file = cartella / nome_file

    if not file.exists():
        return ValueError(f'File {file} non esiste')

    return send_file(file)


def file_galleria(nome_file):
    return file(media_path / 'galleria', nome_file)

def file_biblioteca(nome_file):
    return file(media_path / 'biblioteca', nome_file)
=======
def aggiorna_notizie():
    socketio.emit('notizie', notizie.data)


def aggiorna_galleria():
    socketio.emit('galleria', galleria.data)
>>>>>>> 17c96d17e4f68b4f0ed86536f645590458a30aba
