/*$.ajax({
  import example from "../galleria/example.json";
  dataType: "json",
  success: function (example) {

      $.each(example, function(i,path) {
          $('#galleria').prepend(' <div class = "image fade"><img class="img1" src="'+ "../galleria/files/" + path +'"></div>');
      });
  }
});*/

import jsonData  from "../database/galleria/example.json";

console.log(jsonData);

let index = 0;
displayImages();
function displayImages() {
  let i;
  const images = document.getElementsByClassName("image");
  for (i = 0; i < images.length; i++) {
    images[i].style.display = "none";
  }
  index++;
  if (index > images.length) {
    index = 1;
  }
  images[index-1].style.display = "block";
  setTimeout(displayImages, 2000); 
}

