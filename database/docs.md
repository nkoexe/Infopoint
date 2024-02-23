# Database Infopoint

Gruppo di cartelle in cui vengono salvati tutti i dati del sistema.

## Struttura del database

Il database è suddiviso in 3 cartelle principali: biblioteca, galleria, notizie.
Ogni cartella contiene un file JSON ('data.json') in cui sono salvati vari dati a riguardo di file salvati o di informazioni da mostrare.
Ogni cartella contiene poi una sottocartella ('files/'), in cui sono salvati immagini o video.

## Struttura dei file

Ogni file JSON delle 3 cartelle ha svariati campi strutturati diversamente.
Qui di seguito la struttura e una descrizione di ogni categoria.

### Biblioteca

JSON di esempio:

    {
      "active": "00001",
      "books": {
        "00001": {
            "descr": "Descrizione del libro",
            "img": "/path/to/img.png",
            "title": "Titolone"
        }
      }
    }

Il riquadro della biblioteca contiene solo un libro per volta, indicato nel primo campo dal numero del suo ID.
Nella sezione "books" sono salvati tutti i libri, ordinati in base al numero del loro ID.
Ogni libro, oltre a titolo e descrizione, ha un campo "img", in cui è indicato il percorso della sua copertina. Questo è un percorso relativo, che parte dalla cartella "files/", quindi per indicare un'immagine salvata in "database/biblioteca/files/img.png", si utilizza "img.png".

### Galleria

JSON di esempio:

    {
      "00001":  {
          "text": "test",
          "type": "image",
          "path": "/data/2022-10/img.png",
          "active": true
      },
      "00002": {
          "text": "test2",
          "type": "video",
          "path": "/path/to/video.mp4",
          "active": false
      },
      "00003": {
          "text": "",
          "type": "youtube",
          "path": "dQw4w9WgXcQ",
          "active": true
      }
    }

Nel riquadro della galleria invece, gli elementi attivi possono essere più di uno. Per questo l'attributo "active" è presente in ogni elemento.
Il campo "text" è la descrizione del media, la didascalia che verrà mostrata assieme ad esso. Può essere un campo vuoto.
Ogni elemento può essere di tre tipi: immagine, video o video da YouTube.
Il tipo è determinato dal campo "type":

- se "type" è "image", il campo "path" contiene il percorso locale dell'immagine;
- se "type" è "video", il campo "path" contiene il percorso locale del video;
- se "type" è "youtube", il campo "path" contiene l'id del video di YouTube.

Come per la biblioteca, i campi "path" per immagini e video locali sono relativi alla cartella "files/" della cartella della galleria (cioè "database/galleria/files/").
L'id del video di YouTube viene estratto dal link che l'utente provvede tramite il backend ed inserito nel database automaticamente, per risalire al link originale basta aggiungere l'url base di Youtube. Ad "https://www.youtube.com/watch?v=" quindi si aggiunge la stringa dell'id.
Similarmente, se si vuole estrarre l'id da un link, bisogna estrarre soltanto il parametro "v" dell'url. Se il link originale è "https://www.youtube.com/watch?v=dQw4w9WgXcQ", l'id del video è "dQw4w9WgXcQ". Per i link brevi ("https://youtu.be/"), scartare tutti i parametri dell'url (tutto quello che segue "?") e inserire soltanto il codice che segue la base dell'url breve. Esempio, da "https://youtu.be/dQw4w9WgXcQ?si=fjpJIurLpmfGxS-_" si scartano i parametri, quindi "https://youtu.be/dQw4w9WgXcQ", e scartando anche la base dell'url si ottiene il codice, "dQw4w9WgXcQ".

### Notizie

JSON di esempio:

    {
      "00001": {
          "active": true,
          "text": "Questa è una notizia di test. Hello, world!"
      },
      "00002": {
          "active": false,
          "text": "Heyoooo figata assurda"
      }
    }

Come per la galleria, gli elementi sono ordinati in base al numero del loro ID (numero incrementale), e il campo "active" per ogni elemento indica se esso deve essere mostrato o meno.
Il campo "text" è il testo della notizia.

_Domande_:

- serve un file di configurazione generale per impostazioni varie?

  - **Risposta**: yeah, ad esempio per i nomi delle cartelle o roba del genere

- Come gestire un dato eliminato?
  - Viene completamente eliminato dal database
  - Viene aggiunto un attributo per indicare che è stato eliminato, nascondendolo dal frontend
- Quali estensioni di file per la galleria sono permesse? (Solo png/jpg/jpeg/gif, mp4/m4a/mov/avi/mpg/mpeg)
- Cosa succede se la bibliotecaria elimina il libro in uso?

_Todo_:

- Sistema di ordinamento personalizzato per notizie e galleria

_Note_:

- L'ISBN non è stato inserito tra i dati richiesti, dato che attualmente non c'è modo di riutilizzare libri aggiunti in precedenza
