"""
Connessioni da database a backend / frontend
"""

from .app import socketio
from database import BibliotecaDB, NotizieDB, GalleriaDB, DATABASEPATH as media_path


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()


def aggiorna_frontend():
    socketio.emit('test', 'test')


