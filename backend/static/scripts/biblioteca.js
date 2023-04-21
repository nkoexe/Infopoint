function bookdel(id) {
    $.ajax({
        url: "/biblioteca",
        type: "DELETE",
        data: {
            "id": id
        },
        success: function(data) {

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
    document.getElementById("break").classList.remove("hidden")
    document.getElementById("bibliosubmit").classList.add("hidden");

    // Valore nascosto per modifica al metodo post
    var method_val = document.getElementById("valore_metodo");
    method_val.value = id;
}

function bookeditcanc() {
    document.getElementById("booksave").classList.add("hidden");
    document.getElementById("bookcanc").classList.add("hidden");
    document.getElementById("bibliosubmit").classList.remove("hidden");

    document.getElementById("input_titolo").value = "";
    document.getElementById("input_descrizione").value = "";
    document.getElementById("preview_copertina").src = "";
    document.getElementById("break").classList.add("hidden")
    document.getElementById("valore_metodo").value = "";
}

function loadFile(event) {
    var reader = new FileReader();
    reader.onload = function(){
        var preview = document.getElementById("preview_copertina");
        preview.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}

function duplicate(id) {
    /*document.getElementById("input_titolo").value = document.getElementById('title.' + id).textContent;
    document.getElementById("input_descrizione").value = document.getElementById('desc.' + id).textContent;
    var img = document.getElementById('img.' + id).value;
    document.getElementById("duplicate").value = img;
    var method_val = document.getElementById("valore_metodo");
    method_val.value = "duplicate";*/
    var titolo = document.getElementById('title.' + id).textContent;
    var descrizione = document.getElementById('desc.' + id).textContent;
    var img = document.getElementById('img.' + id).alt;

    $.ajax({
        url: "/biblioteca",
        type: "POST",
        data: {
            "titolo": titolo,
            "descrizione": descrizione,
            "img_duplicated": img
        },
        success: function(data) {
            sessionStorage.setItem("reloading", "true");
            location.reload();
        }
    });
}

window.onload = function() {
    var reloading = sessionStorage.getItem("reloading");
    if (reloading) {
        console.log(reloading)
        sessionStorage.removeItem("reloading");
        var ul = document.getElementById("blist");
        var lastBook = ul.children[ul.children.length - 1];
        var lastID = lastBook.id;
        bookedit(lastID);
    }
}