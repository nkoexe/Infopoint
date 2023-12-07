socket = io('/frontend');

// Marquee dove inserire le notizie
const notizie = document.getElementById('notizie').children[0];

const dio = document.getElementById('dio');

function esci_da_schermo_intero() {
    document.exitFullscreen();
}

document.onkeydown = (event) => {
    if (event.code === 'Escape') {
        dio.classList.toggle('expanded');
    }
}

socket.on('biblioteca', (data) => {
    console.log(data)
})

socket.on('galleria', (data) => {
    console.log(data)
})

socket.on('notizie', (data) => {
    notizie.innerHTML = ''

    for (const id in data) {

        if (data[id].active) {
            notizie.innerHTML += data[id].text + "&emsp;&emsp;"
        }
    }
})
