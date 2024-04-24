from flask import Flask, redirect, url_for
from flask_socketio import SocketIO
from secrets import token_hex
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = token_hex(32)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 24 * 60 * 60

socketio = SocketIO(app)


import routes

from frontend import frontend

app.register_blueprint(frontend)
