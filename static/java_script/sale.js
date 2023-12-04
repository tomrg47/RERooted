document.addEventListener("DOMContentLoaded", function () {
  const photoInput = document.getElementById("photo");
  const previewImage = document.getElementById("preview");

  photoInput.addEventListener("change", function () {
    // Display a preview of the selected image
    const file = photoInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewImage.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
});
