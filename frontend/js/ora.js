const ui_orologio = document.getElementById('orologio')

setInterval(() => {
    var now = new Date()
    var day = now.getDate();
    var month = now.getMonth() + 1;
    var year = now.getFullYear();

    if (month < 10) { month = '0' + month };
    if (day < 10) { day = '0' + day };
    var date = day + '/' + month + '/' + year;

    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();

    if (hour < 10) { hour = '0' + hour };
    if (minute < 10) { minute = '0' + minute };
    if (second < 10) { second = '0' + second };
    var time = hour + ':' + minute + ':' + second;

    var timedate = date + " - " + time;

    ui_orologio.innerHTML = timedate;

}, 1000);
