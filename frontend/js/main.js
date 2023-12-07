socket = io('/frontend');

// Il nome l'ha scelto David, questo è il riquadro per uscire da schermo intero
const dio = document.getElementById('dio');

// Marquee dove inserire le notizie
const notizie = document.getElementById('notizie').children[0];

// Elementi riquadro biblioteca
const titolobiblioteca = document.getElementById('titolobiblioteca');
const immaginebiblioteca = document.getElementById('immaginebiblioteca');
const descrizionebiblioteca = document.getElementById('descrizionebiblioteca');

let index_galleria = 0;
let dati_galleria;
const galleria_youtube = document.getElementById('galleria_youtube');
const galleria_video = document.getElementById('galleria_video');
const galleria_immagine = document.getElementById('galleria_immagine');
const galleria_didascalia = document.getElementById('didascaliagalleria').children[0];


function esci_da_schermo_intero() {
    document.exitFullscreen();
}

document.onkeydown = (event) => {
    if (event.code === 'Escape') {
        dio.classList.toggle('expanded');
    }
}


// -------------------------------


function cambia_elemento_galleria () {
    index_galleria = (index_galleria + 1) % dati_galleria.length;
    let elemento = dati_galleria[index_galleria];

    console.log(elemento)

    if (elemento.type === 'youtube') {
        galleria_youtube.classList.remove('hidden');
        galleria_video.classList.add('hidden');
        galleria_immagine.classList.add('hidden');

        galleria_youtube.src = elemento.path + "?autoplay=1";
        galleria_didascalia.innerHTML = elemento.text;

    } else if (elemento.type === 'video') {
        galleria_youtube.classList.add('hidden');
        galleria_video.classList.remove('hidden');
        galleria_immagine.classList.add('hidden');

        galleria_video.children[0].src = "galleria/" + elemento.path;
        galleria_didascalia.innerHTML = elemento.text;

    } else if (elemento.type === 'image') {
        galleria_youtube.classList.add('hidden');
        galleria_video.classList.add('hidden');
        galleria_immagine.classList.remove('hidden');

        galleria_immagine.src = "galleria/" + elemento.path;
        galleria_didascalia.innerHTML = elemento.text;
    }
};

setInterval(cambia_elemento_galleria, 5000);



socket.on('biblioteca', (data) => {
    let libro = data.books[data.active];
    titolobiblioteca.innerHTML = libro.title
    immaginebiblioteca.src = "biblioteca/" + libro.img
    descrizionebiblioteca.innerHTML = libro.descr
})

socket.on('galleria', (data) => {
    index_galleria = 0;
    dati_galleria = [];
    for (elemento in data) {
        if (data[elemento].active) {
            dati_galleria.push(data[elemento]);
        }
    }
})

socket.on('notizie', (data) => {
    notizie.innerHTML = ''

    for (const id in data) {

        if (data[id].active) {
            notizie.innerHTML += data[id].text + "&emsp;&emsp;"
        }
    }
})
