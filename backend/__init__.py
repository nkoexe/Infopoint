from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from database import biblioteca, notizie, galleria

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
def _index():
    return render_template('config.html')


@app.route('/login')
def _login():
    return render_template('login.html')


@app.route('/settings')
def _settings():
    return render_template('settings.html')


@app.route('/biblioteca', methods=['GET', 'POST'])
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
def _galleria():
    return render_template('galleria.html')


@app.route('/notizie', methods=['GET', 'POST'])
def _notizie():
    if request.method == 'GET':
        return render_template('news.html', notizie=notizie.data)

    elif request.method == 'POST':
        notizia = request.form['text']

        notizie.add(notizia)

        return redirect('/notizie')


@app.route('/notizie/<id>', methods=['DELETE'])
def _notizie_id(id):
    if request.method == 'DELETE':
        notizie.delete(id)

    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
