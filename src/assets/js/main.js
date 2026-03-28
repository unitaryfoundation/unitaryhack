const Turbolinks = require('turbolinks');
const drawer = require('./drawer');
const darkMode = require('./dark-mode');
const countdown = require('./countdown');

// Initialize Turbolinks
Turbolinks.start();

// Initialize mobile nav drawer
drawer();

// Initialize dark mode toggle
const { enableThemeSwitch } = document.documentElement.dataset;

if (enableThemeSwitch) {
  darkMode();
}

// Initialize countdown timer on home page
document.addEventListener('turbolinks:load', () => {
  const target = new Date('2025-06-12T05:00:00Z');
  countdown('countdown', target);
});
