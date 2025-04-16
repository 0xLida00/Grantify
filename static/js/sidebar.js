const body = document.querySelector('body'),
  sidebar = body.querySelector('nav'),
  toggle = body.querySelector(".toggle"),
  searchBtn = body.querySelector(".search-box"),
  modeSwitch = body.querySelector(".toggle-switch"),
  modeText = body.querySelector(".mode-text");

// Get the saved dark mode state from localStorage
let darkMode = localStorage.getItem('darkMode');

// Apply dark mode if it was enabled previously
if (darkMode === 'enabled') {
  body.classList.add('dark');
  modeText.innerText = "Light mode";
  modeSwitch.classList.add('active');
} else {
  body.classList.remove('dark');
  modeText.innerText = "Dark mode";
  modeSwitch.classList.remove('active');
}

// Get the saved sidebar state from localStorage
let sidebarState = localStorage.getItem('sidebarState');

// Apply the saved sidebar state
if (sidebarState === 'open') {
  sidebar.classList.remove('close');
} else {
  sidebar.classList.add('close');
}

// Toggle sidebar visibility and save the state
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");

  // Save the sidebar state to localStorage
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

// Toggle dark mode and update mode text on click
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