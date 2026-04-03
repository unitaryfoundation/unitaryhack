const metadata = require('./metadata.json');

const plausibleScriptSrc = process.env.PLAUSIBLE_SCRIPT_SRC || '';
const plausibleEndpoint = process.env.PLAUSIBLE_ENDPOINT || '';
const defaultPlausible = metadata.plausible || null;

module.exports = {
  ...metadata,
  url: process.env.SITE_URL || 'https://unitaryhack.dev',
  plausible: plausibleScriptSrc
    ? {
        scriptSrc: plausibleScriptSrc,
        endpoint: plausibleEndpoint || null,
      }
    : defaultPlausible,
};
