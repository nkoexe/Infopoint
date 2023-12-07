const template_youtube = `<iframe id="galleria_youtube" src="{src}" type="text/html" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`
const template_video = `<video id="galleria_video" autoplay controls loop><source src="{src}" type="video/mp4"></video>`
const template_immagine = `<img id="galleria_immagine" src="{src}" alt="Qui ci dovrebbe essere un'immagine. Se stai leggendo questo testo, contatta <>" />
`

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
const elemento_galleria = document.getElementById('elemento_galleria');
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


function cambia_elemento_galleria() {
    index_galleria = (index_galleria + 1) % dati_galleria.length;
    let elemento = dati_galleria[index_galleria];

    if (elemento.type === 'youtube') {
        console.log(elemento.path)

        elemento_galleria.innerHTML = template_youtube.replace("{src}", elemento.path + "?autoplay=1&controls=0&disablekb=1&enablejsapi=1&fs=0&hl=it&loop=1&modestbranding=1&iv_load_policy=3")
        elemento_galleria.children[0].setAttribute("allow", "autoplay");
        elemento_galleria.children[0].play();
        galleria_didascalia.innerHTML = elemento.text;

    } else if (elemento.type === 'video') {
        elemento_galleria.innerHTML = template_video.replace("{src}", "galleria/" + elemento.path)
        galleria_didascalia.innerHTML = elemento.text;

    } else if (elemento.type === 'image') {
        elemento_galleria.innerHTML = template_immagine.replace("{src}", "galleria/" + elemento.path)
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
