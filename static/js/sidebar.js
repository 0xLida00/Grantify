const body = document.querySelector('body'),
  sidebar = body.querySelector('nav'),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

// Check and apply the saved mode from localStorage
if (localStorage.getItem("darkMode") === "enabled") {
  body.classList.add("dark");
  modeText.innerText = "Light mode";
}

// Toggle sidebar visibility
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

// Show sidebar when search button is clicked
searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
});

// Toggle dark mode and update mode text
modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark");

  // Save the mode to localStorage
  if (body.classList.contains("dark")) {
    localStorage.setItem("darkMode", "enabled");
    modeText.innerText = "Light mode";
  } else {
    localStorage.setItem("darkMode", "disabled");
    modeText.innerText = "Dark mode";
  }
});