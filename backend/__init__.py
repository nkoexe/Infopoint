from hashlib import sha256
from json import load
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from database import biblioteca, galleria, notizie

users = load(open(Path(__file__).parent / 'users.json'))

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'

login_manager = LoginManager()
login_manager.init_app(app)


class User:
    def __init__(self, id):
        self.id = id
        self.username = users[id]['name']
        self.roles = users[id]['roles']
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id


def roles_required(function, roles=['admin']):
    '''
    Wrapper to check if the user has the required roles.
    Use this along with the @login_required decorator.
    '''
    def wrapper(*args, **kw):
        print(current_user)
        return function(*args, **kw)

    return wrapper


@login_manager.unauthorized_handler
def unauthorized():
    '''
    Handles requests without login to pages that require it.
    '''
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    '''
    Creates a User object for the given user_id.
    Called by Flask-Login before each request.
    '''
    if user_id in users:
        return User(user_id)
    else:
        return None


@app.route('/login', methods=['GET', 'POST'])
def _login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password = sha256(password.encode('utf-8')).hexdigest()

        for i in users:
            if users[i]['name'] == username and users[i]['hash'] == password:
                login_user(User(i))

                # next = request.args.get('next')
                return redirect('/')

        return render_template('login.html', error='Nome utente o password errati')


@app.route('/logout')
@login_required
def _logout():
    logout_user()
    return redirect('/login')


@app.route('/')
@login_required
def _index():
    return render_template('config.html')


@app.route('/settings')
@login_required
@roles_required(['admin'])
def _settings():
    return render_template('settings.html')


@app.route('/biblioteca', methods=['GET', 'POST'])
@login_required
def _biblioteca():
    if request.method == 'GET':
        return render_template('biblioteca.html', libri=biblioteca.data['books'])

    elif request.method == 'POST':
        copertina = request.files['copertina']
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']

        biblioteca.add(titolo, descrizione, copertina)

        return redirect('/biblioteca')


@app.route('/galleria')
@login_required
def _galleria():
    return render_template('galleria.html')


@app.route('/notizie', methods=['GET', 'POST'])
@login_required
def _notizie():
    if request.method == 'GET':
        return render_template('news.html', notizie=notizie.data)

    elif request.method == 'POST':
        notizia = request.form['text']

        notizie.add(notizia)

        return redirect('/notizie')


@app.route('/notizie/<id>', methods=['DELETE'])
@login_required
def _notizie_id(id):
    if request.method == 'DELETE':
        notizie.delete(id)

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
