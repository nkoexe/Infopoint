function gallerydel(id) {
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