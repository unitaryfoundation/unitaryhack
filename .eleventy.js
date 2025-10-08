const eleventyNavigationPlugin = require('@11ty/eleventy-navigation');
const syntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const createImageShortcode = require('./src/_11ty/shortcodes/image-shortcode');
const markdownLibrary = require('./src/_11ty/libraries/markdown-library');
const minifyHtml = require('./src/_11ty/utils/minify-html');
const markdownFilter = require('./src/_11ty/filters/markdown-filter');
const svgFilter = require('./src/_11ty/filters/svg-filter');
const browserSyncConfig = require('./src/_11ty/utils/browser-sync-config');
const { readableDateFilter, machineDateFilter } = require('./src/_11ty/filters/date-filters');

module.exports = function (eleventyConfig) {
  const sanitizePathPrefix = (value) => {
    if (!value || value === '/') {
      return '/';
    }

    let normalized = value.trim();

    if (!normalized.startsWith('/')) {
      normalized = `/${normalized}`;
    }

    if (!normalized.endsWith('/')) {
      normalized = `${normalized}/`;
    }

    return normalized;
  };

  const pathPrefix = sanitizePathPrefix(process.env.PATH_PREFIX);
  eleventyConfig.addGlobalData('sitePathPrefix', pathPrefix);
  const includeCname = process.env.INCLUDE_CNAME !== 'false';
  const imageShortcode = createImageShortcode(pathPrefix);

  // Plugins
  eleventyConfig.addPlugin(eleventyNavigationPlugin);
  eleventyConfig.addPlugin(syntaxHighlight);

  // Filters
  eleventyConfig.addFilter('markdown', markdownFilter);
  eleventyConfig.addFilter('readableDate', readableDateFilter);
  eleventyConfig.addFilter('machineDate', machineDateFilter);
  eleventyConfig.addFilter('svg', svgFilter);
  eleventyConfig.addFilter("sortLeaderboard", function(obj) {
    if (!obj || typeof obj !== "object") return [];

    return Object.entries(obj).sort((a, b) => b[1] - a[1]);
  });

  // Shortcodes
  eleventyConfig.addNunjucksAsyncShortcode('image', imageShortcode);

  // Libraries
  eleventyConfig.setLibrary('md', markdownLibrary);

  // Merge data instead of overriding
  eleventyConfig.setDataDeepMerge(true);

  // Trigger a build when files in this directory change
  eleventyConfig.addWatchTarget('./src/assets/scss/');

  // Minify HTML output
  eleventyConfig.addTransform('htmlmin', minifyHtml);

  // Don't process folders with static assets
  eleventyConfig.addPassthroughCopy('./src/favicon.ico');
  eleventyConfig.addPassthroughCopy('./src/admin');
  eleventyConfig.addPassthroughCopy('./src/assets/img');
  if (includeCname) {
    eleventyConfig.addPassthroughCopy('./src/CNAME');
  }

  // Allow Turbolinks to work in development mode
  eleventyConfig.setBrowserSyncConfig(browserSyncConfig);

  // Sorting
  eleventyConfig.addCollection("sortedProjects", function (collection) {
    return collection.getFilteredByGlob("src/projects/*.md").sort(function (a, b) {
      let nameA = a.data.title.toUpperCase();
      let nameB = b.data.title.toUpperCase();
      if (nameA < nameB) return -1;
      else if (nameA > nameB) return 1;
      else return 0;
    });
  });
  
  // Markdown Plugins
  let markdownIt = require("markdown-it");
  let markdownItAnchor = require("markdown-it-anchor");
  let options = {
    html: true,
    breaks: true,
    linkify: true,
  };
  let opts = {
    permalink: false,
  };

  eleventyConfig.setLibrary(
    "md",
    markdownIt(options).use(markdownItAnchor, opts)
  );

  eleventyConfig.addPairedShortcode("mdRender", (title) => {
    return markdownIt().renderInline(title);
  });


  return {
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',
    passthroughFileCopy: true,
    pathPrefix,
    dir: {
      input: 'src',
      layouts: "_layouts"
    },
  };
};
