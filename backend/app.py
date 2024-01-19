from flask import Flask, redirect, url_for
from flask_socketio import SocketIO
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = b"0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70"

socketio = SocketIO(app)


@app.route("/")
def index():
    return redirect(url_for("backend.index"))


from routes import backend
from frontend import frontend

app.register_blueprint(frontend)
app.register_blueprint(backend)
