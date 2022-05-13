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
      "active": "4",
      "books": {
        "1": {
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
      "1":  {
          "text": "test",
          "type": "image",
          "path": "/data/2022-10/img.png",
          "active": true
      },
      "2": {
          "text": "test2",
          "type": "video",
          "path": "/path/to/video.mp4",
          "active": false
      },
      "3": {
          "text": "test3",
          "type": "youtube",
          "path": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
          "active": true
      }
    }

Nel riquadro della galleria invece, gli elementi attivi possono essere più di uno. Per questo l'attributo "active" è presente in ogni elemento.
Il campo "text" è la descrizione del media.
Ogni elemento può essere di tre tipi: immagine, video o youtube.
Il tipo è determinato dal campo "type":

- se "type" è "image", il campo "path" contiene il percorso dell'immagine;
- se "type" è "video", il campo "path" contiene il percorso del video;
- se "type" è "youtube", il campo "path" contiene il link del video youtube.
  Come per la biblioteca, i campi "path" per immagini e video sono relativi alla cartella "files/" (ovviamente di questa cartella, cioè "database/galleria/files/").

### Notizie

JSON di esempio:

    {
      "1": {
          "active": true,
          "text": "test1"
      },
      "2": {
          "active": false,
          "text": "Heyoooo questa è una notizia di test figata assurda"
      }
    }

Come per la galleria, gli elementi sono ordinati in base al numero del loro ID (numero incrementale), e il campo "active" per ogni elemento indica se esso deve essere mostrato o meno.
Il campo "text" è il testo della notizia miseria è autoesplicativo.

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
