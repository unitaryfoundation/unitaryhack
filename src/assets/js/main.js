const Turbolinks = require('turbolinks');
const drawer = require('./drawer');
const darkMode = require('./dark-mode');
const countdown = require('./countdown');

const initRegistrationEmbeds = () => {
  const embedShells = document.querySelectorAll('[data-registration-embed]');

  embedShells.forEach((shell) => {
    const frame = shell.querySelector('iframe');

    if (!frame || shell.dataset.embedInitialized === 'true') {
      return;
    }

    shell.dataset.embedInitialized = 'true';

    frame.addEventListener('load', () => {
      shell.classList.remove('is-loading');
      shell.classList.add('is-loaded');
    }, { once: true });
  });
};

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
  initRegistrationEmbeds();
});
