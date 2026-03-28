const metadata = require('./metadata.json');

module.exports = {
  ...metadata,
  url: process.env.SITE_URL || 'https://unitaryhack.dev',
};
