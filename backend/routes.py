import logging

from app import app
from auth import users, login_richiesto, ruolo_richiesto, current_user
from flask import redirect, render_template, request, send_from_directory

from databaseconnections import biblioteca, notizie, galleria, media_path

from .frontend import frontend

app.register_blueprint(frontend, url_prefix='/frontend')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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


@app.route('/biblioteca', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_richiesto
@ruolo_richiesto.biblioteca
def _biblioteca():
    if request.method == 'GET':
        return render_template('biblioteca.html', libri=biblioteca.data['books'])

    # Inserimento di un nuovo libro e modifica
    elif request.method == 'POST':
        if 'img_duplicated' not in request.form:
            copertina = request.files['copertina']
            titolo = request.form['titolo'].strip()
            descrizione = request.form['descrizione'].strip()
            id = request.form['metodo']
            # Inserimento di un libro nuovo
            if id == '0':
                if titolo and descrizione and copertina:
                    biblioteca.add(titolo, descrizione, copertina)
                return redirect('/biblioteca')
            # Modifica di un libro esistente
            elif id != '0' and id != 'duplicate':
                if titolo and descrizione and copertina:
                    biblioteca.editImg(id, titolo, descrizione, copertina)
                elif titolo and descrizione:
                    biblioteca.edit(id, titolo, descrizione)
                return redirect('/biblioteca')

        elif 'img_duplicated' in request.form:
            img = request.form['img_duplicated'].strip()
            titolo = request.form['titolo'].strip()
            descrizione = request.form['descrizione'].strip()
            if titolo and descrizione and img:
                biblioteca.duplicate(titolo, descrizione, img)
            return redirect('/biblioteca')

    elif request.method == 'DELETE':
        id = request.form['id']
        if biblioteca.data['active'] != id:
            biblioteca.delete(id)
        else:
            return 'ko'

    elif request.method == 'PUT':
        id = request.form['id']
        # Modifica dello stato visibile o meno della notizia
        if 'active' in request.form:
            biblioteca.editActive(id, active=True)
    return 'ok'


@app.route('/galleria', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_richiesto
@ruolo_richiesto.galleria
def _galleria():
    if request.method == 'GET':
        return render_template('galleria.html', media=galleria.data)

    elif request.method == 'POST':
        media = request.files['galleria']
        link = request.form['link']
        text = request.form['descrizione']
        if request.form.get('checkbox'):
            active = True
        else:
            active = False
        logging.debug(active)

        if media and text:
            galleria.add(text, active, media, link)

        return redirect('/galleria')

    elif request.method == 'DELETE':
        id = request.form['id']
        galleria.delete(id)

    elif request.method == 'PUT':
        id = request.form['id']
        # Modifica dello stato visibile o meno della notizia
        if 'active' in request.form:
            galleria.editActive(id, active=True)

    return 'ok'


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

@app.route('/frontend')
def frontend():
    return render_template('index.html')
