socket = io('/frontend');

socket.on('biblioteca', (data) => {
    console.log(data)
})

socket.on('galleria', (data) => {
    console.log(data)
})

socket.on('notizie', (data) => {
    console.log(data)
})
