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


class _biblioteca:
    def __init__(self):
        self.path = BASEPATH / 'biblioteca' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)

    def add(self, title: str, descr: str, img):
        '''
        Add a book to the database and set it as the active book.

        :param str title: the title of the book
        :param str descr: the description of the book
        :param file img: the flask file object of the image of the book
        '''
        #! Todo:
        #! - check if file is actually an image
        #! - save the image with the book id to avoid overwriting

        filename = secure_filename(img.filename)
        filepath = BASEPATH / 'biblioteca' / subdir_name / filename
        img.save(filepath)

        # the book's id is the last one incremented by 1
        id = str(int(sorted(self.data['books'].keys())[-1]) + 1)

        # add the book to the database
        self.data['books'][id] = {
            'title': title,
            'descr': descr,
            'img': filename
        }

        self.data['active'] = id

        self.update()


class _notizie:
    def __init__(self):
        self.path = BASEPATH / 'notizie' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)

    def add(self, text: str):
        '''
        Add news text to the database and set it as active.

        :param str text: main text of the news
        '''

        # the news' id is the last one incremented by 1
        id = str(int(sorted(self.data.keys())[-1]) + 1)

        self.data[id] = {
            'text': text,
            'active': True
        }

        self.update()

    def edit(self, id: int, text: str = None, active: bool = None):
        '''
        Modify a news text.

        :param int id: id of the news
        :param str text: main text of the news
        '''

        if text is not None and isinstance(text, str):
            self.data[str(id)]['text'] = text

        if active is not None and isinstance(active, bool):
            self.data[str(id)]['active'] = active

        self.update()

    def delete(self, id: int or str):
        '''
        Delete a news element.

        :param int id: id of the news
        '''

        if isinstance(id, int):
            id = str(id)

        del self.data[id]

        self.update()


class _galleria:
    def __init__(self):
        self.path = BASEPATH / 'galleria' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)

    def add(self, text: str, active: bool, media=None, link=None):
        '''
        Add a gallery to the database and set it as active.

        :param str text: description of the media
        :param bool active: set the media to active or not
        :param file media: the flask file object of the media
        :param str link: link to the youtube video
        '''

        if media is None and link is None:
            return

        if media is not None:
            filename = secure_filename(media.filename)
            filepath = BASEPATH / 'galleria' / subdir_name / filename
            media.save(filepath)

            if filepath.suffix in ('.jpg', '.jpeg', '.png', '.gif'):
                media_type = 'image'
            elif filepath.suffix in ('.mp4', '.mov', '.avi', '.mpg', '.mpeg'):
                media_type = 'video'
            else:
                # File type not supported
                # todo: modify
                return

        id = str(int(sorted(self.data.keys())[-1]) + 1)

        self.data[id] = {
            'text': text,
            'type': media_type,
            'path': filepath,
            'active': active
        }

        self.update()

    def edit(self, id: int, text: str = None, active: bool = None):
        '''
        Modify a media of the gallery.

        :param int id: id of the media
        :param str text: description of the media
        :param bool active: set the media to active or not
        '''

        if text is not None and isinstance(text, str):
            self.data[str(id)]['text'] = text

        if active is not None and isinstance(active, bool):
            self.data[str(id)]['active'] = active

        self.update()

    def delete(self, id: int or str):
        '''
        Delete a media of the gallery.

        :param int id: id of the media
        '''

        if isinstance(id, int):
            id = str(id)

        del self.data[id]

        self.update()


biblioteca = _biblioteca()
notizie = _notizie()
galleria = _galleria()
