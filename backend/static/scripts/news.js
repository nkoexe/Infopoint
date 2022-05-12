function newsdel(id) {
    $.ajax({
        url: "/notizie/" + id,
        type: "DELETE",
        success: function(data) {
            location.reload();
        }
    });
}