// Grantify/static/js/base.js
document.addEventListener("DOMContentLoaded", function() {
    var menuToggle = document.getElementById("menu-toggle");
    if (menuToggle) {
      menuToggle.addEventListener("click", function(e) {
        e.preventDefault();
        var wrapper = document.getElementById("wrapper");
        if (wrapper) {
          wrapper.classList.toggle("toggled");
        }
      });
    }
  });