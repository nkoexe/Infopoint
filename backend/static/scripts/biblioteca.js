function bookdel(id) {
    $.ajax({
        url: "/biblioteca",
        type: "DELETE",
        data: {
            "id": id
        },
        success: function(data) {
            // Remove list element instead of reloading.
            // add an id to the element ("list0002"), find it, .remove() it
            if (data == "ko"){
                alert("Il libro selezionato non e' eliminabile in quanto attualmente attivo")
            }
            location.reload();
        }
    });
}

function bookshow(id) {
    $.ajax({
        url: "/biblioteca",
        type: "PUT",
        data: {
            "id": id,
            "active": ""
        },
        success: function(data) {
            // Remove list element instead of reloading.
            // add an id to the element ("list0002"), find it, .remove() it
            location.reload();
        }
    });
}

function bookedit(id) {
    var savebtn = document.getElementById("booksave")
    savebtn.classList.remove("hidden");
    savebtn.setAttribute("onclick", "bookeditsave('" + id + "')"); // id is still a string - "00021", not 21

    var cancbtn = document.getElementById("bookcanc");
    cancbtn.classList.remove("hidden");
    cancbtn.setAttribute("onclick", "bookeditcanc('" + id + "')");

    // Take the text of the news element and put it in the textarea
    document.getElementById("input_titolo").value = document.getElementById('title.' + id).textContent;
    document.getElementById("input_descrizione").value = document.getElementById('desc.' + id).textContent;
    document.getElementById("preview_copertina").src = document.getElementById('img.' + id).src;
}

function bookeditsave(id) {
    var title = document.getElementById("input_titolo").value
    var descr = document.getElementById("input_descrizione").value
    //var img = document.getElementById("input_copertina").files[0].name
    
    $.ajax({
        url: "/biblioteca",
        type: "PUT",
        data: {
            "id": id,
            "title": title,
            "descr": descr//,
            //"img": img
        },
        success: function(data) {
            if (data == "ok") {
                location.reload();
            } else {
                // TODO: show the error
                alert("C'è stato un errore nella modifica della notizia");
            }
            location.reload();
        }
    });
}

function bookeditcanc(id) {
    document.getElementById("booksave").classList.add("hidden");
    document.getElementById("bookcanc").classList.add("hidden");

    document.getElementById("input_titolo").value = "";
    document.getElementById("input_descrizione").value = "";
    document.getElementById("preview_copertina").src = "";
}

function loadFile(event) {
    var preview = document.getElementById("preview_copertina");
    preview.src = URL.createObjectURL(event.target.files[0]);
    preview.onload = function() {
        URL.revokeObjectURL(output.src)
    }
}