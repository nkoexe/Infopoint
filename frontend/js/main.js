socket = io('/frontend');

// Marquee dove inserire le notizie
const notizie = document.getElementById('notizie').children[0];

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
            notizie.innerHTML += data[id].text
        }
    }
})