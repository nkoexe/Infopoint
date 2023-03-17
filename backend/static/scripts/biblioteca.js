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