function newsshow(id) {
    /* Toggle the visibility of a news element */

    // Icon and text of the element
    var showbtn = document.getElementById("newsshowicon"+id);
    var newstext = document.getElementById(id);

    // Send the request to the server
    $.ajax({
        url: "/notizie/" + id,
        type: "PUT",
        data: {
            // To reverse the visibility just send this, the server will do the rest
            "active": ""
        },
        success: function(data) {
            if (data == "ko") {
                alert("Errore");
            } else if (data == '1') {
                // If the element is now visible, change the icon and text opacity
                showbtn.innerHTML = "visibility";
                newstext.classList.remove("disabled");
            } else {
                // If the element is now hidden, change the icon and text opacity
                showbtn.innerHTML = "visibility_off";
                newstext.classList.add("disabled");
            }
        }
    });
}

function newsedit(id) {
    /* Cliks on the edit button of an existing news element */

    // Unhide the 'Save' and 'Cancel' buttons, add functionality to them
    var savebtn = document.getElementById("newssave")
    savebtn.classList.remove("hidden");
    savebtn.setAttribute("onclick", "newseditsave('" + id + "')"); // id is still a string - "00021", not 21
    
    var cancbtn = document.getElementById("newscanc");
    cancbtn.classList.remove("hidden");
    cancbtn.setAttribute("onclick", "newseditcanc('" + id + "')");

    // Take the text of the news element and put it in the textarea
    document.getElementById("newsinput").value = document.getElementById(id).textContent;
}

function newseditsave(id) {
    /* Save the edited news text */

    // Check if the textarea is empty
    var text = document.getElementById("newsinput").value.trim();
    if (text == "") {
        alert("Inserisci il testo della notizia");
        return;
    }

    // Send the new text to the server
    $.ajax({
        url: "/notizie/" + id,
        type: "PUT",
        data: {
            "text": text
        },
        success: function(data) {
            // On success, reload the page, otherwise show the error
            if (data == "ok") {
                location.reload();
            } else {
                // TODO: show the error
                alert("C'è stato un errore nella modifica della notizia");
            }
        }
    });
}

function newseditcanc(id) {
    /* Cancel the edit of the news text */

    // Hide the 'Save' and 'Cancel' buttons
    var savebtn = document.getElementById("newssave");
    savebtn.classList.add("hidden");
    savebtn.removeAttribute("onclick");

    var cancbtn = document.getElementById("newscanc");
    cancbtn.classList.add("hidden");
    cancbtn.removeAttribute("onclick");

    // Remove the text from the textarea
    document.getElementById("newsinput").value = "";
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