# Database Infopoint

Gruppo di cartelle in cui vengono salvati tutti i dati del sistema.

Domande:

- serve un file di configurazione generale per impostazioni varie?
- com'è meglio organizzare il json della biblioteca? pro-contro

## Struttura del database

Il database è suddiviso in 3 cartelle principali: biblioteca, galleria, news.
Ogni cartella contiene un file JSON ('data.json') in cui sono salvati vari dati a riguardo di file salvati o di informazioni da mostrare.
Ogni cartella contiene poi una sottocartella ('files/'), in cui sono organizzati tutti i file (in altre sottocartelle per data??)

## Struttura dei file

Ogni file delle 3 cartelle ha svariati campi di dati, strutturati diversamente.
Qui di seguito

### Biblioteca

_Note:_
L'ISBN non è stato inserito tra i dati richiesti, dato che attualmente non c'è modo di riutilizzare libri aggiunti in precedenza
