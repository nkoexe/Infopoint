function imgdel(id) {
    $.ajax({
        url: "/galleria",
        type: "DELETE",
        data: {
            "id": id
        },
        success: function(data) {

            if (data == "ko"){
                alert("L'elemento selezionato non e' eliminabile in quanto attualmente attivo")
            }
            location.reload();
        }
    });
}

function imgshow(id) {
    $.ajax({
        url: "/galleria",
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