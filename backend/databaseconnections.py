"""
Connessioni da database a backend / frontend
"""

from flask import send_file
from .app import socketio
from database import BibliotecaDB, NotizieDB, GalleriaDB, DATABASEPATH as media_path


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()


def aggiorna_frontend():
    socketio.emit('test', 'test')

def file(cartella, nome_file):
    if not isinstance(nome_file, str):
        raise TypeError('Nome del file da mandare deve essere una stringa.')

    assert '..' not in nome_file  # idk non succede ma se succede almeno nessuno fa danni

    file = cartella / nome_file

    if not file.exists():
        return ValueError(f'File {file} non esiste')

    return send_file(file)


def file_galleria(nome_file):
    return file(media_path / 'galleria', nome_file)

def file_biblioteca(nome_file):
    return file(media_path / 'biblioteca', nome_file)
