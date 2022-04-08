from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
        return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
