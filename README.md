# unitaryHACK 2025 incoming ☄️!

unitaryHACK is back, and coming to a computer near you **May 28&ndash;Jun 11 2025**.
This year we'll celebrate the 5th edition of the hackathon, and we're excited to bring you the best edition yet.
Check out the website at [`unitaryhack.dev`](https://unitaryhack.dev) for more information.

Never heard of unitaryHACK before?
Check out previous iterations:

- <a href="https://2024.unitaryhack.dev/">2024.unitaryhack.dev</a>
- <a href="https://2023.unitaryhack.dev/">2023.unitaryhack.dev</a>
- <a href="https://2022.unitaryhack.dev/">2022.unitaryhack.dev</a>
- <a href="https://2021.unitaryhack.dev/">2021.unitaryhack.dev</a>

---

## 🚀 Website development

Want to help improve the unitaryHACK website?
The website is built with [11ty](https://www.11ty.dev/) and hosted on GitHub Pages.
The [Fernfolio](https://fernfolio.netlify.app/) template was used to bootstrap the design.
Here are some basic local setup steps to get you started:

### Local environment

- Clone the repo
- Navigate to the directory `cd untitaryhack`
- Install the goods `npm install`
- Run it `npm start`
- You should now be able to see everything running on http://localhost:8080
- Make a pull request to add your changes to github

## 💻 Development Scripts

**`npm start`**: Run 11ty with hot reload at localhost:8080

**`npm run build`**: Generate minified production build

Check out the Eleventy [command line usage docs](https://www.11ty.dev/docs/usage/) for more options.

## 🌐 Deployment

- Pushes to `main` run `.github/workflows/buildsite.yaml`, build with Node, and deploy to GitHub Pages using `PATH_PREFIX=/`, `INCLUDE_CNAME=true`, and `SITE_URL=https://unitaryhack.dev` (so `src/CNAME` is published for the production domain).
- Manual runs expose a `target` input; choose `github-pages` to rebuild with `PATH_PREFIX=/uhack-test/`, skip the `CNAME`, and stamp links with `SITE_URL=https://natestemen.github.io/uhack-test` for testing on a repo-scoped Pages URL.
- Locally you can mirror those targets: `npm run clean && npm run build` for production, or `npm run clean && PATH_PREFIX=/uhack-test/ INCLUDE_CNAME=false SITE_URL=https://natestemen.github.io/uhack-test npm run build` for the GitHub Pages preview.
- Asset URLs already honor `PATH_PREFIX`, and when you open `_site/index.html` directly the build rewrites links for `file://`, though serving `_site` via `npm start` (or any static server) gives the most accurate preview.
