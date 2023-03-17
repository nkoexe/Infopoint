'''
Python interface to the database.
'''

from configparser import ConfigParser
from json import dump, load
from pathlib import Path
import logging
import os

BASEPATH = Path(__file__).resolve().parent.parent / 'database'

config = ConfigParser()
config.read(BASEPATH / 'config.ini')

json_name = config.get('Path', 'json_name')
subdir_name = config.get('Path', 'subdir_name')


class BibliotecaDB:
    def __init__(self):
        self.path = BASEPATH / 'biblioteca' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
        logging.debug('Database Biblioteca aggiornato.')

    def add(self, title: str, descr: str, img):
        '''
        Add a book to the database and set it as the active book.

        :param str title: the title of the book
        :param str descr: the description of the book
        :param file img: the flask file object of the image of the book
        '''
        #! Todo:
        #! - check if file is actually an image

        if len(self.data['books']) == 0:
            id = '1'.zfill(5)
        else:
            # the book's id is the last one incremented by 1
            id = str(int(list(self.data['books'].keys())[-1]) + 1).zfill(5)

        extension = img.filename.rsplit('.', 1)[1].lower()

        if extension not in ('jpg', 'jpeg', 'png', 'gif'):
            # File type not supported
            logging.warning(f'Aggiunta a Biblioteca: Estensione file <{extension}> non supportata.')
            return

        filepath = BASEPATH / 'biblioteca' / subdir_name / (id + '.' + extension)
        print(filepath)

        img.save(filepath)

        logging.debug('Copertina libro salvata in ' + str (filepath))

        # add the book to the database
        self.data['books'][id] = {
            'title': title,
            'descr': descr,
            'img': (id + '.' + extension)
        }

        self.data['active'] = id

        logging.debug(f'Libro con id <{id}> aggiunto e impostato come attivo.')

        self.update()

    def delete(self, id: str):
        '''
        Delete a biblioteca element.

        :param str id: id of the biblioteca element
        '''

        del self.data['books'][id]
        filedir = BASEPATH / 'biblioteca' / subdir_name
        for fname in os.listdir(filedir):
            if fname.startswith(id):
                os.remove(filedir / fname)
        logging.debug(f'Libro con id <{id}> eliminato.')

        self.update()

    def show(self, id: str):
        self.data['active'] = id
        self.update()

    def edit(self, id: str, title: str, descr: str):

        if title is not None and descr is not None and isinstance(title, str) and isinstance(descr, str):
            self.data['books'][id]['title'] = title
            self.data['books'][id]['descr'] = descr
            logging.debug(f'Aggiornato il testo di Notizia con id <{id}>')
        else:
            logging.debug(f"Errore, titolo o descrizione vuoti")

        self.update()
    
    def editImg(self, id: str, title: str, descr: str, img):

        if title is not None and descr is not None and isinstance(title, str) and isinstance(descr, str):
            self.data['books'][id] = {
            'title': title,
            'descr': descr
        }
            logging.debug(f'Aggiornato il testo di Notizia con id <{id}>')
        else:
            logging.debug(f"Errore, titolo o descrizione vuoti")

        extension = img.filename.rsplit('.', 1)[1].lower()

        if extension not in ('jpg', 'jpeg', 'png', 'gif'):
            # File type not supported
            logging.warning(f'Aggiunta a Biblioteca: Estensione file <{extension}> non supportata.')
            return

        filepath = BASEPATH / 'biblioteca' / subdir_name / (id + '.' + extension)
        print(filepath)

        img.save(filepath)

        logging.debug('Copertina libro salvata in ' + str (filepath))

        # add the book to the database
        self.data['books'][id] = {
            'title': title,
            'descr': descr,
            'img': (id + '.' + extension)
        }

        self.data['active'] = id

        logging.debug(f'Libro con id <{id}> aggiunto e impostato come attivo.')

        self.update()

    def editActive(self, id: str, active: bool):
        if active:
            if self.data['active'] != id:
                self.data['active'] = id
                logging.debug(f'Notizia con id <{id}> impostata come ' + 'visibile.')

        self.update()


class NotizieDB:
    def __init__(self):
        self.path = BASEPATH / 'notizie' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
        logging.debug('Database Notizie aggiornato.')

    def add(self, text: str):
        '''
        Add news text to the database and set it as active.

        :param str text: main text of the news
        '''

        if len(self.data) == 0:
            id = '1'.zfill(5)
        else:
            # the news' id is the last one incremented by 1
            id = str(int(list(self.data.keys())[-1]) + 1).zfill(5)

        self.data[id] = {
            'text': text,
            'active': True
        }

        logging.debug(f'Notizia con id <{id}> aggiunta.')

        self.update()

    def edit(self, id: str, text: str = None, active: bool = None):
        '''
        Modify the text of a news element or set it as visible in the frontend or not.

        :param str id: id of the news element
        :param str text: main text of the news element
        :param bool active: if the news is visible
        '''

        if text is not None and isinstance(text, str):
            self.data[id]['text'] = text
            logging.debug(f'Aggiornato il testo di Notizia con id <{id}>')

        if active is not None and isinstance(active, bool):
            self.data[id]['active'] = active
            logging.debug(f'Notizia con id <{id}> impostata come ' + 'visibile.' if active else 'nascosta.')

        self.update()

        return self.data[id]['active']

    def delete(self, id: str):
        '''
        Delete a news element.

        :param str id: id of the news element
        '''

        del self.data[id]
        logging.debug(f'Notizia con id <{id}> eliminata.')

        self.update()


class GalleriaDB:
    def __init__(self):
        self.path = BASEPATH / 'galleria' / json_name
        self.data = load(open(self.path, 'r'))

    def update(self):
        '''
        Dump the database to the json files.
        '''

        dump(self.data, open(self.path, 'w'), indent=4, sort_keys=True, ensure_ascii=False)
        logging.debug('Database Notizie aggiornato.')

    def add(self, text: str, active: bool, media=None, link=None):
        '''
        Add a gallery to the database and set it as active.

        :param str text: description of the media
        :param bool active: set the media to active or not
        :param file media: the flask file object of the media
        :param str link: link to the youtube video
        '''

        if media is None and link is None:
            logging.warning('Aggiunta a Galleria: File o link non dati, uno dei due è necessario.')
            return

        if len(self.data) == 0:
            id = '1'.zfill(5)
        else:
            id = str(int(list(self.data.keys())[-1]) + 1).zfill(5)

        if media is not None:
            extension = media.filename.rsplit('.', 1)[1].lower()

            if extension in ('.jpg', '.jpeg', '.png', '.gif'):
                media_type = 'image'
            elif extension in ('.mp4', '.mov', '.avi', '.mpg', '.mpeg'):
                media_type = 'video'
            else:
                # File type not supported
                logging.warning(f'Aggiunta a Galleria: Estensione file <{extension}> non supportata.')
                return

            filepath = BASEPATH / 'galleria' / subdir_name / (id + '.' + extension)
            media.save(filepath)

            logging.debug('File salvato in: ' + filepath)

        elif link is not None:
            if link.startswith('https://www.youtube.com/watch?v='):
                media_type = 'youtube'
                filepath = link
            else:
                logging.warning('Link invalido.')
                return

        self.data[id] = {
            'text': text,
            'type': media_type,
            'path': filepath,
            'active': active
        }

        logging.debug(f'Elemento della Galleria con id <{id}> salvato.')

        self.update()

    def edit(self, id: str, text: str = None, active: bool = None):
        '''
        Modify a media of the gallery.

        :param str id: id of the media
        :param str text: description of the media
        :param bool active: set the media to active or not
        '''

        if text is not None and isinstance(text, str):
            self.data[id]['text'] = text
            logging.debug(f'Aggiornato il testo dell\'elemento di Galleria con id <{id}>')

        if active is not None and isinstance(active, bool):
            self.data[id]['active'] = active
            logging.debug(f'Elemento di Galleria con id <{id}> impostata come ' + 'visibile.' if active else 'nascosta.')

        self.update()

    def delete(self, id: str):
        '''
        Delete a media of the gallery.

        :param str id: id of the media
        '''

        del self.data[id]

        logging.debug('Elemento di Galleria con id <{id}> eliminato')

        self.update()
