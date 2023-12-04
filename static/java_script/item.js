document.addEventListener("DOMContentLoaded", function () {
  // Fetch products from JSON file
  fetch("/get_products")
    .then((response) => response.json())
    .then((products) => displayProducts(products));
});

function displayProducts(products) {
  const marketplace = document.getElementById("marketplace");

  products.forEach((product) => {
    const card = createProductCard(product);
    marketplace.appendChild(card);
    const image = card.querySelector(".product-image");
  });
}

function createProductCard(product) {
  const card = document.createElement("div");
  card.classList.add("product-card");

  const image = document.createElement("img");
  image.src = product.image;
  image.alt = product.name;
  image.classList.add("product-image");
  card.appendChild(image);

  const name = document.createElement("div");
  name.textContent = product.name;
  name.classList.add("product-name");
  card.appendChild(name);

  const price = document.createElement("div");
  price.textContent = `£${product.price.toFixed(2)}`;
  price.classList.add("product-price");
  card.appendChild(price);

  // Add click event to navigate to individual item page
  card.addEventListener("click", function () {
    window.location.href = `/item/${product.id}`;
  });
  return card;
}
