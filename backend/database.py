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
    '''
    Add news text to the database and set it as active.

    :param str text: main text of the news
    '''

    # the news' id is the last one incremented by 1
    id = str(int(sorted(notizie.keys())[-1]) + 1)

    notizie[id] = {
        'text': text,
        'active': True
    }

    dump(notizie, open(BASEPATH / 'notizie' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def edit_news(id: int, text: str = None, active: bool = None):
    '''
    Modify a news text.

    :param int id: id of the news
    :param str text: main text of the news
    '''

    if text is not None and isinstance(text, str):
        notizie[str(id)]['text'] = text

    if active is not None and isinstance(active, bool):
        notizie[str(id)]['active'] = active

    dump(notizie, open(BASEPATH / 'notizie' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def delete_news(id: int):
    '''
    Delete a news.

    :param int id: id of the news
    '''

    del notizie[str(id)]

    dump(notizie, open(BASEPATH / 'notizie' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def add_gallery(text: str, active: bool, img=None, link=None):
    '''
    Add a gallery to the database and set it as active.

    :param str text: description of the media
    :param bool active: set the media to active or not
    '''

    if img is None and link is None:
        return

    if img is not None:
        filename = secure_filename(img.filename)
        filepath = BASEPATH / 'biblioteca' / subdir_name / filename
        img.save(filepath)

        if filepath.suffix in ('.jpg', '.jpeg', '.png', '.gif'):
            media_type = 'image'
        elif filepath.suffix in ('.mp4', '.mov', '.avi', '.mpg', '.mpeg'):
            media_type = 'video'
        else:
            # File type not supported
            # todo: modify 
            return

    id = str(int(sorted(galleria.keys())[-1]) + 1)

    galleria[id] = {
        'text': text,
        'type': media_type,
        'path': filepath,
        'active': active
    }

    dump(galleria, open(BASEPATH / 'galleria' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def edit_gallery(id: int, text: str = None, active: bool = None):
    '''
    Modify a media of the gallery.

    :param int id: id of the media
    :param str text: description of the media
    :param bool active: set the media to active or not
    '''

    if text is not None and isinstance(text, str):
        galleria[str(id)]['text'] = text

    if active is not None and isinstance(active, bool):
        galleria[str(id)]['active'] = active

    dump(galleria, open(BASEPATH / 'galleria' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)


def delete_gallery(id: int):
    '''
    Delete a media of the gallery.

    :param int id: id of the media
    '''

    del galleria[str(id)]

    dump(galleria, open(BASEPATH / 'galleria' / json_name, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
