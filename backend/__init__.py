from functools import wraps
from hashlib import sha256
from json import load
from pathlib import Path
import logging


from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required as login_richiesto, login_user, logout_user, current_user

from database import BibliotecaDB, NotizieDB, GalleriaDB


biblioteca = BibliotecaDB()
notizie = NotizieDB()
galleria = GalleriaDB()

users = load(open(Path(__file__).parent / 'users.json'))

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'

login_manager = LoginManager()
login_manager.init_app(app)


class User:
    def __init__(self, id):
        self.id = id
        self.username = users[id]['name']
        self.admin = 'admin' in users[id]['roles']
        self.biblioteca = 'biblioteca' in users[id]['roles'] or self.admin
        self.galleria = 'galleria' in users[id]['roles'] or self.admin
        self.notizie = 'notizie' in users[id]['roles'] or self.admin
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id


class ruolo_richiesto:
    '''
    Wrappers per controllare che l'utente che ha mandato la richiesta
    possiede un ruolo richiesto.
    Da usare assieme a (subito dopo) @login_richiesto.
    '''
    def admin(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.admin:
                abort(403)

            return func(*args, **kwargs)
        return wrapper

    def biblioteca(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.biblioteca:
                abort(403)

            return func(*args, **kwargs)
        return wrapper

    def galleria(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.galleria:
                abort(403)

            return func(*args, **kwargs)
        return wrapper

    def notizie(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.notizie:
                abort(403)

            return func(*args, **kwargs)
        return wrapper


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized():
    '''
    Indica cosa fare con richieste di utenti che non hanno
    ancora fatto il login, a pagine che lo richiedono
    '''
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    '''
    Crea un oggetto User per lo user_id passato.
    Chiamato automaticamente da Flask-Login prima di
    processare la richiesta ricevuta.
    '''
    if user_id in users:
        return User(user_id)
    else:
        return None


@app.route('/login', methods=['GET', 'POST'])
def _login():
    if request.method == 'GET':
        # Se l'utente ha già eseguito il login lo reindirizza alla homepage
        if current_user.is_authenticated:
            return redirect('/')

        return render_template('login.html')

    # L'utente sta eseguendo il login
    elif request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        password = sha256(password.encode('utf-8')).hexdigest()

        # Controlla nome utente e password
        for i in users:
            if users[i]['name'] == username and users[i]['hash'] == password:
                login_user(User(i))

                return redirect('/')

        return render_template('login.html', error='Nome utente o password errati')


@app.route('/logout')
@login_richiesto
def _logout():
    logout_user()
    return redirect('/login')


@app.route('/')
@login_richiesto
def _index():
    # Se l'utente ha solo un permesso non mostrare la homepage ma
    # reindirizza direttamente alla pagina a cui si ha accesso.
    # Il controllo viene eseguito sommando booleani, dato che in Python false=0 e true=1
    if sum((current_user.biblioteca, current_user.galleria, current_user.notizie)) == 1:
        if current_user.biblioteca:
            return redirect('/biblioteca')
        elif current_user.galleria:
            return redirect('/galleria')
        elif current_user.notizie:
            return redirect('/notizie')

    # Altrimenti mostra la homepage con pulsanti in base ai propri permessi
    else:
        return render_template('home.html', user=current_user)


@app.route('/impostazioni')
@login_richiesto
@ruolo_richiesto.admin
def _impostazioni():
    return render_template('impostazioni.html')


@app.route('/impostazioni/utenti')
@login_richiesto
@ruolo_richiesto.admin
def _impostazioni_utenti():
    return render_template('utenti.html', users=users)


@app.route('/biblioteca', methods=['GET', 'POST'])
@login_richiesto
@ruolo_richiesto.biblioteca
def _biblioteca():
    if request.method == 'GET':
        return render_template('biblioteca.html', libri=biblioteca.data['books'])

    # Inserimento di un nuovo libro
    elif request.method == 'POST':
        copertina = request.files['copertina']
        titolo = request.form['titolo'].strip()
        descrizione = request.form['descrizione'].strip()

        print(copertina.stream.read())

        if titolo and descrizione and copertina:
            biblioteca.add(titolo, descrizione, copertina)

        return redirect('/biblioteca')


@app.route('/galleria')
@login_richiesto
@ruolo_richiesto.galleria
def _galleria():
    return render_template('galleria.html')


@app.route('/notizie', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_richiesto
@ruolo_richiesto.notizie
def _notizie():
    if request.method == 'GET':
        return render_template('notizie.html', notizie=notizie.data)

    # Eliminazione di una notizia esistente
    elif request.method == 'DELETE':
        id = request.form['id']
        notizie.delete(id)
        app.logger.debug(f'Notizia con id {id} eliminata')

    # Inserimento di una nuova notizia
    elif request.method == 'POST':
        notizia = request.form['text'].strip()

        if notizia:
            notizie.add(notizia)

        return redirect('/notizie')

    # Aggiornamento della notizia
    elif request.method == 'PUT':
        id = request.form['id']

        # Modifica del testo
        if 'text' in request.form:
            notizia = request.form['text'].strip()

            if not notizia:
                return 'ko'

            notizie.edit(id, text=notizia)

        # Modifica dello stato visibile o meno della notizia
        # invertendo il valore precedente
        if 'active' in request.form:
            active = not notizie.data[id]['active']
            notizie.edit(id, active=active)
            return '1' if active else '0'

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
