"""
Connessioni da database a backend / frontend
"""

from flask import send_file
from database import BibliotecaDB, NotizieDB, GalleriaDB, DATABASEPATH as media_path


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()


def file(cartella, nome_file):
    if not isinstance(nome_file, str):
        raise TypeError("Nome del file da mandare deve essere una stringa.")

    assert (
        ".." not in nome_file
    )  # idk non succede, ma se succede almeno nessuno fa danni

    file = cartella / nome_file

    if not file.exists():
        raise FileNotFoundError(f"File {file} non esiste")

    return send_file(file, mimetype="image/gif")


def file_galleria(nome_file):
    try:
        return file(media_path / "galleria" / "files", nome_file)
    except FileNotFoundError:
        return ""


def file_biblioteca(nome_file):
    try:
        return file(media_path / "biblioteca" / "files", nome_file)
    except FileNotFoundError:
        return ""
