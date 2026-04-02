let markdownIt = require('markdown-it');

module.exports = function (str) {
  return markdownIt({
    html: true,
    breaks: true,
    linkify: true,
  }).render(str);
};
