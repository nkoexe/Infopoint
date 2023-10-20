from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = b'0ee6f27b79730fb025949c4d792f084adadcf4796bfdeb980c6ec1abf1fd7a70'
socketio = SocketIO(app)


import .routes