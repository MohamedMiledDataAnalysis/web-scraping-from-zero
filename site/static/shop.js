// The Gadget Shop page arrives empty. This script asks the hidden API for
// products and adds them to the page, 12 at a time, as you scroll down.
var state = { page: 0, pages: 1, loading: false, gen: 0 };

function card(p) {
  var div = document.createElement("div");
  div.className = "product";
  div.dataset.sku = p.sku;
  div.innerHTML = '<h3 class="name"><a href="/shop/product/' + p.id + '">' + p.name + '</a></h3>' +
    '<p class="price">£' + p.price.toFixed(2) + '</p>' +
    '<p class="rating">' + p.rating + ' / 5</p>' +
    '<p class="stock">' + (p.in_stock ? "In stock" : "Out of stock") + '</p>';
  return div;
}

function loadNext() {
  if (state.loading || state.page >= state.pages) return;
  state.loading = true;
  var gen = state.gen;          // answers from an older list are ignored
  document.getElementById("status").textContent = "Loading products...";
  var params = new URLSearchParams({
    page: state.page + 1,
    category: document.getElementById("category").value,
    sort: document.getElementById("sort").value
  });
  fetch("/shop/api/products?" + params)
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      if (gen !== state.gen) return;
      state.page = data.page; state.pages = data.pages;
      var box = document.getElementById("products");
      data.products.forEach(function (p) { box.appendChild(card(p)); });
      document.getElementById("status").textContent =
        "Showing " + box.children.length + " of " + data.total + " products";
      state.loading = false;
    })
    .catch(function () {          // a failed request must not freeze the shop
      if (gen !== state.gen) return;
      state.loading = false;
      document.getElementById("status").textContent = "Could not load products";
    });
}

function restart() {
  state = { page: 0, pages: 1, loading: false, gen: state.gen + 1 };
  document.getElementById("products").innerHTML = "";
  loadNext();
}

window.addEventListener("scroll", function () {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) loadNext();
});
document.getElementById("category").addEventListener("change", restart);
document.getElementById("sort").addEventListener("change", restart);
loadNext();
