# unitaryHACK 2026 incoming ☄️!

unitaryHACK is back, and coming to a computer near you **Jun 3&ndash;Jun 17 2026**.
This year we'll celebrate the 6th edition of the hackathon, and we're excited to bring you the best edition yet.
Check out the website at [`unitaryhack.dev`](https://unitaryhack.dev) for more information.

Never heard of unitaryHACK before?
Check out previous iterations:

- <a href="https://2025.unitaryhack.dev/">2025.unitaryhack.dev</a>
- <a href="https://2024.unitaryhack.dev/">2024.unitaryhack.dev</a>
- <a href="https://2023.unitaryhack.dev/">2023.unitaryhack.dev</a>
- <a href="https://2022.unitaryhack.dev/">2022.unitaryhack.dev</a>
- <a href="https://2021.unitaryhack.dev/">2021.unitaryhack.dev</a>

---

## 🚀 Website development

Want to help improve the unitaryHACK website?
The website is built with [11ty](https://www.11ty.dev/) and hosted on GitHub Pages.
The Fernfolio template was used to bootstrap the design.
Here are some basic local setup steps to get you started:

### Local environment

- Clone the repo
- Navigate to the directory `cd unitaryhack`
- Install the goods `npm install`
- Run it `npm start`
- You should now be able to see everything running on http://localhost:8080
- Make a pull request to add your changes to github

## 💻 Development Scripts

**`npm start`**: Run 11ty with hot reload at localhost:8080

**`npm run build`**: Generate minified production build

Check out the Eleventy [command line usage docs](https://www.11ty.dev/docs/usage/) for more options.

## 🗄️ Archiving an edition on a year subdomain

When a new unitaryHACK website replaces the current production site, keep the previous
edition available on a year-specific subdomain such as `2025.unitaryhack.dev`.

1. Decide the archive year and target hostname, for example `2025.unitaryhack.dev`.
2. Make sure the old edition builds as a standalone site:
   - run `npm ci`
   - run `INCLUDE_CNAME=false SITE_URL=https://2025.unitaryhack.dev npm run build`
   - open `_site/index.html` or serve `_site/` locally and check that internal links and assets work.
3. Deploy the generated `_site/` directory for the archived edition to its own static hosting target.
   GitHub Pages is preferred when possible because it keeps the archive in GitHub, but Netlify is
   acceptable if the edition still depends on Netlify-specific configuration.
4. Point the DNS record for the year subdomain at the archive host:
   - for GitHub Pages, follow GitHub's custom-domain instructions and add the required `CNAME`
     or `A`/`AAAA` records for the archive target;
   - for Netlify, add the year subdomain to the archived site and follow Netlify's DNS target.
5. Do not keep the production `src/CNAME` value in archive builds unless that archive host is
   meant to serve `unitaryhack.dev`. The current deployment workflow uses `INCLUDE_CNAME=false`
   for non-production GitHub Pages builds for this reason.
6. Update the current year's README history list so the archived edition is linked alongside
   previous years.
7. Update any recap or announcement posts that still point at `unitaryhack.dev` for the archived
   year. For the 2025 move, this includes the 2025 recap post linked from issue
   [`#60`](https://github.com/unitaryfoundation/unitaryhack/issues/60).
8. Verify the archive after DNS propagation:
   - `https://<year>.unitaryhack.dev/` loads over HTTPS;
   - major pages such as `/projects/`, `/bounties/`, `/leaderboard/`, and `/hackers/<username>/`
     return `200`;
   - images, CSS, JavaScript, and canonical links point at the archive hostname instead of the
     new production site.
