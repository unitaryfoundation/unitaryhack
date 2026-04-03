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

let navDropdownsInitialized = false;

const closeNavDropdownsExcept = (activeDropdown) => {
  const openDropdowns = document.querySelectorAll('[data-nav-dropdown][open]');

  openDropdowns.forEach((dropdown) => {
    if (dropdown !== activeDropdown) {
      dropdown.removeAttribute('open');
    }
  });
};

const initNavDropdowns = () => {
  if (navDropdownsInitialized) {
    return;
  }

  navDropdownsInitialized = true;

  document.addEventListener('click', (event) => {
    const activeDropdown = event.target.closest('[data-nav-dropdown]');
    closeNavDropdownsExcept(activeDropdown);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') {
      return;
    }

    closeNavDropdownsExcept(null);
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
  initNavDropdowns();
  initRegistrationEmbeds();
});
