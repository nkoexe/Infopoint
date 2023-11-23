socket = io();

socket.on('biblioteca', (data) => {
    console.log(data)
})