const body = document.querySelector('body'),
  sidebar = body.querySelector('nav'),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

body.classList.add('hidden');

// Get the saved dark mode state from localStorage
let darkMode = localStorage.getItem('darkMode');

if (darkMode === 'enabled') {
  body.classList.add('dark');
  modeText.innerText = "Light mode";
  modeSwitch.classList.add('active');
} else {
  body.classList.remove('dark');
  modeText.innerText = "Dark mode";
  modeSwitch.classList.remove('active');
}

let sidebarState = localStorage.getItem('sidebarState');

if (sidebarState === 'open') {
  sidebar.classList.remove('close');
} else {
  sidebar.classList.add('close');
}

document.addEventListener("DOMContentLoaded", () => {
  body.classList.remove('hidden');
});

// Toggle sidebar visibility and save the state
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");

  if (sidebar.classList.contains('close')) {
    localStorage.setItem('sidebarState', 'closed');
  } else {
    localStorage.setItem('sidebarState', 'open');
  }
});

// Show sidebar when search button is clicked
searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
  localStorage.setItem('sidebarState', 'open');
});

modeSwitch.addEventListener("click", () => {
  body.classList.toggle('dark');

  // Save the mode to localStorage and update the toggle state
  if (body.classList.contains('dark')) {
    localStorage.setItem('darkMode', 'enabled');
    modeText.innerText = "Light mode";
    modeSwitch.classList.add('active');
  } else {
    localStorage.setItem('darkMode', 'disabled');
    modeText.innerText = "Dark mode";
    modeSwitch.classList.remove('active');
  }
});