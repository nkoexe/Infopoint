from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from json import load
from database import biblioteca, notizie, galleria

users = load(open(Path(__file__).parent / 'users.json'))

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '_login'


class User:
    def __init__(self, id):
        self.id = id
        self.data = users[id]
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
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

        login_user(User('1'))

        # Questo oppure semplicemente /index
        next = request.args.get('next')
        return redirect(next or '/')


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
