from app import app
from routes import backend
from json import load
from flask import abort, redirect, render_template, request, url_for
from pathlib import Path
from functools import wraps
from hashlib import sha256
import logging

from flask_login import (
    LoginManager,
    login_required as login_richiesto,
    login_user,
    logout_user,
    current_user,
)

logger = logging.getLogger(__name__)

users = load(open(Path(__file__).parent / "users.json"))

login_manager = LoginManager(app)


class User:
    def __init__(self, id):
        self.id = id
        self.username = users[id]["name"]
        self.admin = "admin" in users[id]["roles"]
        self.biblioteca = "biblioteca" in users[id]["roles"] or self.admin
        self.galleria = "galleria" in users[id]["roles"] or self.admin
        self.notizie = "notizie" in users[id]["roles"] or self.admin
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id


class ruolo_richiesto:
    """
    Wrappers per controllare che l'utente che ha mandato la richiesta
    possiede un ruolo richiesto.
    Da usare assieme a (subito dopo) @login_richiesto.
    """

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


@login_manager.unauthorized_handler
def unauthorized():
    logger.info("richiesta non autorizzata")
    """
    Indica cosa fare con richieste di utenti che non hanno
    ancora fatto il login, a pagine che lo richiedono
    """
    return redirect(url_for("backend.login"))


@login_manager.user_loader
def load_user(user_id):
    """
    Crea un oggetto User per lo user_id passato.
    Chiamato automaticamente da Flask-Login prima di
    processare la richiesta ricevuta.
    """
    if user_id in users:
        return User(user_id)
    else:
        return None


@backend.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        logger.info("login utente")

        # Se l'utente ha già eseguito il login lo reindirizza alla homepage
        if current_user.is_authenticated:
            return redirect(url_for("backend.index"))

        return render_template("login.html")

    # L'utente sta eseguendo il login
    elif request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        password = sha256(password.encode("utf-8")).hexdigest()

        # Controlla nome utente e password
        for i in users:
            if users[i]["name"] == username and users[i]["hash"] == password:
                login_user(User(i))

                return redirect(url_for("backend.index"))

        return render_template("login.html", error="Nome utente o password errati")


@backend.route("/logout")
@login_richiesto
def logout():
    logout_user()
    return redirect(url_for("backend.login"))
