"""
Connessioni da database a backend / frontend
"""

from app import socketio
from database import BibliotecaDB, NotizieDB, GalleriaDB, DATABASEPATH as media_path


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()


def aggiorna_biblioteca():
    socketio.emit('biblioteca', biblioteca.data)


def aggiorna_notizie():
    socketio.emit('notizie', notizie.data)


def aggiorna_galleria():
    socketio.emit('galleria', galleria.data)
