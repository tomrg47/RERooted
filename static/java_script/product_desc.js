document.addEventListener("DOMContentLoaded", function () {
  const buyNowButton = document.querySelector(".buy-now-button");
  const offerButton = document.querySelector(".offer-button");

  buyNowButton.addEventListener("click", function () {
    // Handle Buy Now button click
    alert("Buy Now clicked!");
  });

  offerButton.addEventListener("click", function () {
    // Handle Make an Offer button click
    alert("Make an Offer clicked!");
  });
});
