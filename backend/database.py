'''
Python interface to the database.
'''

from json import load, dump
from pathlib import Path
from configparser import ConfigParser
from werkzeug.utils import secure_filename


BASEPATH = Path(__file__).parent.parent / 'database'

config = ConfigParser()
config.read(BASEPATH / 'config.ini')

json_name = config.get('Path', 'json_name')
subdir_name = config.get('Path', 'subdir_name')

biblioteca = load(open(BASEPATH / 'biblioteca' / json_name, 'r'))
galleria = load(open(BASEPATH / 'galleria' / json_name, 'r'))
notizie = load(open(BASEPATH / 'notizie' / json_name, 'r'))


def add_book(title: str, descr: str, img):
    '''
    Add a book to the database and set it as the active book.

    :param str title: the title of the book
    :param str descr: the description of the book
    :param file img: the flask file object of the image of the book
    '''

    filename = secure_filename(img.filename)
    filepath = BASEPATH / 'biblioteca' / subdir_name / filename
    img.save(filepath)

    # the book's id is the last one incremented by 1

    id = str(int(sorted(biblioteca['books'].keys())[-1]) + 1)

    # add the book to the database
    biblioteca['books'][id] = {
        'title': title,
        'descr': descr,
        'img': filename
    }

    biblioteca['active'] = id

    # update the json file
    dump(biblioteca, open(BASEPATH / 'biblioteca' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def add_news(text: str):
    id = str(int(sorted(notizie.keys())[-1]) + 1)

    notizie[id] = {
        'text': text,
        'active': True
    }

    dump(notizie, open(BASEPATH / 'notizie' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
