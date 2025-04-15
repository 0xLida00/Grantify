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
  body.classList.add('dark'); // Add the dark mode class
  modeText.innerText = "Light mode"; // Update the toggle text
  modeSwitch.classList.add('active'); // Ensure the toggle reflects the dark mode state
} else {
  body.classList.remove('dark'); // Ensure light mode is applied
  modeText.innerText = "Dark mode"; // Update the toggle text
  modeSwitch.classList.remove('active'); // Ensure the toggle reflects the light mode state
}

// Toggle sidebar visibility
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

// Show sidebar when search button is clicked
searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
});

// Toggle dark mode and update mode text on click
modeSwitch.addEventListener("click", () => {
  // Toggle the dark mode class on the body
  body.classList.toggle('dark');

  // Save the mode to localStorage and update the toggle state
  if (body.classList.contains('dark')) {
    localStorage.setItem('darkMode', 'enabled'); // Save dark mode state
    modeText.innerText = "Light mode"; // Update the toggle text
    modeSwitch.classList.add('active'); // Update the toggle to reflect dark mode
  } else {
    localStorage.setItem('darkMode', 'disabled'); // Save light mode state
    modeText.innerText = "Dark mode"; // Update the toggle text
    modeSwitch.classList.remove('active'); // Update the toggle to reflect light mode
  }
});