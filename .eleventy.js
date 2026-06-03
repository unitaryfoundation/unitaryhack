const eleventyNavigationPlugin = require('@11ty/eleventy-navigation');
const syntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const pluginTOC = require('eleventy-plugin-toc');
const imageShortcode = require('./src/_11ty/shortcodes/image-shortcode');
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
  const siteUrl = process.env.SITE_URL || 'https://unitaryhack.dev';
  const normalizedSiteUrl = siteUrl.endsWith('/') ? siteUrl : `${siteUrl}/`;
  eleventyConfig.addGlobalData('sitePathPrefix', pathPrefix);
  const includeCname = process.env.INCLUDE_CNAME !== 'false';

  // Plugins
  eleventyConfig.addPlugin(eleventyNavigationPlugin);
  eleventyConfig.addPlugin(syntaxHighlight);
  eleventyConfig.addPlugin(pluginTOC);

  // Filters
  eleventyConfig.addFilter('markdown', markdownFilter);
  eleventyConfig.addFilter('withPathPrefix', (value) => {
    if (typeof value !== 'string' || !value) {
      return value;
    }

    return value
      .replace(/\]\(\/(?!\/)/g, `](${pathPrefix}`)
      .replace(/href="\/(?!\/)/g, `href="${pathPrefix}`)
      .replace(/src="\/(?!\/)/g, `src="${pathPrefix}`)
      .replace(/href='\/(?!\/)/g, `href='${pathPrefix}`)
      .replace(/src='\/(?!\/)/g, `src='${pathPrefix}`);
  });
  eleventyConfig.addFilter('absoluteUrl', (value) => {
    if (typeof value !== 'string' || !value) {
      return value;
    }

    if (/^https?:\/\//i.test(value)) {
      return value;
    }

    return new URL(value, normalizedSiteUrl).href;
  });
  eleventyConfig.addFilter('isHttpUrl', (value) => {
    return typeof value === 'string' && /^https?:\/\//i.test(value);
  });
  const parseRepoInfo = (value, fallbackProvider = 'github') => {
    if (typeof value !== 'string' || !value.trim()) {
      return { provider: fallbackProvider, repoKey: '' };
    }

    let raw = value.trim().replace(/^['"]|['"]$/g, '');
    if (/^(github|gitlab)\.com\//i.test(raw)) {
      raw = `https://${raw}`;
    }

    try {
      const parsed = new URL(raw);
      const host = parsed.hostname.toLowerCase();
      let path = parsed.pathname.replace(/^\/+|\/+$/g, '');

      if (host.endsWith('github.com')) {
        const parts = path.split('/').filter(Boolean);
        return { provider: 'github', repoKey: parts.slice(0, 2).join('/') };
      }

      if (host.endsWith('gitlab.com')) {
        path = path.split('/-/')[0].replace(/\.git$/i, '');
        return { provider: 'gitlab', repoKey: path };
      }
    } catch (error) {
      // Fall through to the repo-like parser below.
    }

    const repoMatch = raw.match(/^([A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+)(?:$|[:#?\s])/);
    if (repoMatch) {
      return { provider: fallbackProvider, repoKey: repoMatch[1] };
    }

    return { provider: fallbackProvider, repoKey: '' };
  };
  eleventyConfig.addFilter('bountyIssueUrl', (bounty, projectUrl) => {
    if (!bounty) {
      return '#';
    }

    if (bounty.url) {
      return bounty.url;
    }

    const projectRepo = parseRepoInfo(projectUrl);
    const repoInfo = bounty.repo
      ? parseRepoInfo(bounty.repo, projectRepo.provider)
      : projectRepo;
    if (!repoInfo.repoKey || !bounty.issue_num) {
      return '#';
    }

    const kind = bounty.kind || 'issues';
    if (repoInfo.provider === 'gitlab') {
      const gitlabPath = ['merge_requests', 'work_items'].includes(kind)
        ? kind
        : 'issues';
      return `https://gitlab.com/${repoInfo.repoKey}/-/${gitlabPath}/${bounty.issue_num}`;
    }

    if (kind === 'pull') {
      return `https://github.com/${repoInfo.repoKey}/pull/${bounty.issue_num}`;
    }

    return `https://github.com/${repoInfo.repoKey}/issues/${bounty.issue_num}`;
  });
  eleventyConfig.addFilter('bountyIssueLabel', (bounty, projectUrl) => {
    if (!bounty) {
      return 'Issue';
    }

    if (bounty.title) {
      return bounty.title;
    }

    const projectRepo = parseRepoInfo(projectUrl);
    const repoInfo = bounty.repo
      ? parseRepoInfo(bounty.repo, projectRepo.provider)
      : projectRepo;
    if (repoInfo.repoKey && bounty.issue_num) {
      return `${repoInfo.repoKey}#${bounty.issue_num}`;
    }

    return bounty.issue_num ? `Issue #${bounty.issue_num}` : 'Issue';
  });
  eleventyConfig.addFilter('bountyState', (bounty) => {
    return bounty && bounty.state ? bounty.state : 'open';
  });
  eleventyConfig.addFilter('sumBountyValues', (bounties) => {
    if (!Array.isArray(bounties)) {
      return 0;
    }

    return bounties.reduce((total, bounty) => {
      return total + Number(bounty && bounty.value ? bounty.value : 0);
    }, 0);
  });
  eleventyConfig.addFilter('readableDate', readableDateFilter);
  eleventyConfig.addFilter('machineDate', machineDateFilter);
  eleventyConfig.addFilter('svg', svgFilter);
  eleventyConfig.addFilter("sortLeaderboard", function(obj) {
    if (!obj || typeof obj !== "object") return [];

    return Object.entries(obj).sort((a, b) => b[1] - a[1]);
  });

  // Shortcodes
  eleventyConfig.addNunjucksAsyncShortcode('image', imageShortcode(pathPrefix));

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
  eleventyConfig.addCollection('sitemapPages', function (collection) {
    return collection.getAll().filter((item) => {
      return (
        item.url &&
        item.outputPath &&
        item.outputPath.endsWith('.html') &&
        item.url !== '/404.html' &&
        item.data &&
        item.data.sitemap !== false
      );
    }).sort((a, b) => a.url.localeCompare(b.url));
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
