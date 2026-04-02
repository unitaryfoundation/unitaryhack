const path = require('path');
const Image = require('@11ty/eleventy-img');

function normalisePathPrefix(prefix) {
  if (!prefix || prefix === '/') {
    return '/';
  }

  let value = prefix.trim();

  if (!value.startsWith('/')) {
    value = `/${value}`;
  }

  if (!value.endsWith('/')) {
    value = `${value}/`;
  }

  return value;
}

module.exports = function createImageShortcode(pathPrefix = '/') {
  const prefix = normalisePathPrefix(pathPrefix);
  const urlPath = path.posix.join(prefix, 'assets/img') + '/';

  return async function imageShortcode(src, alt, sizes, classes, loading = 'lazy') {
    const metadata = await Image(src, {
      widths: [25, 320, 640, 960, 1200, 1800, 2400],
      formats: ['webp', 'jpeg'],
      urlPath,
      outputDir: '_site/assets/img/',
    });

    const imageAttributes = {
      class: classes,
      alt,
      sizes,
      loading,
      decoding: 'async',
    };

    return Image.generateHTML(metadata, imageAttributes);
  };
};
