function newsedit(id) {
    var savebtn = document.getElementById("newssave")
    savebtn.classList.remove("hidden");
    savebtn.setAttribute("onclick", "newseditsave(" + id + ")");
    
    var cancbtn = document.getElementById("newscanc");
    cancbtn.classList.remove("hidden");
    cancbtn.setAttribute("onclick", "newseditcanc(" + id + ")");

    document.getElementById("newsinput").value = document.getElementById(id).textContent;
}

function newseditsave(id) {
    $.ajax({
        url: "/notizie/" + id,
        type: "PUT",
        data: {
            "text": document.getElementById("newsinput").value
        },
        success: function(data) {
            if (data == "ok") {
                location.reload();
            } else {
                alert("Errore");
            }
        }
    });
}

function newsdel(id) {
    $.ajax({
        url: "/notizie/" + id,
        type: "DELETE",
        success: function(data) {
            location.reload();
        }
    });
}