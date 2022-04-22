from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('config.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/biblioteca')
def biblioteca():
    return render_template('biblioteca.html')


@app.route('/galleria')
def galleria():
    return render_template('galleria.html')


@app.route('/notizie', methods=['GET', 'POST'])
def notizie():
    if request.method == 'GET':
        return render_template('news.html')

    elif request.method == 'POST':
        notizia = request.form['notizia']
        print(notizia)
        return redirect('/notizie')


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
