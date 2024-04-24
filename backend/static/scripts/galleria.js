function imgshow(id) {
    $.ajax({
        url: "",
        type: "PUT",
        data: {
            "id": id,
            "active": ""
        },
        success: function (data) {
            location.reload();
        }
    });
}

function imgedit(id) {
    alert("Non implementato, abbi pazienza");
}

function imgdel(id) {
    $.ajax({
        url: "",
        type: "DELETE",
        data: {
            "id": id
        },
        success: function (data) {

            if (data == "ko") {
                alert("L'elemento selezionato non e' eliminabile in quanto attualmente attivo")
            }
            location.reload();
        }
    });
}

