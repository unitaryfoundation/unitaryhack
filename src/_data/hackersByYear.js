const hackers2023 = require("./hackers_2023.json");
const hackers2024 = require("./hackers_2024.json");
const hackers2026 = require("./hackers.json");

const HACKER_DATA_BY_YEAR = [
  { year: 2023, hackers: hackers2023 },
  { year: 2024, hackers: hackers2024 },
  { year: 2026, hackers: hackers2026 },
];

function getBounties(hacker) {
  return Array.isArray(hacker.bounties) ? hacker.bounties : [];
}

function getTotalValue(hacker) {
  return Number(hacker.total_value || 0);
}

module.exports = () => {
  const hackersByUsername = new Map();

  for (const { year, hackers } of HACKER_DATA_BY_YEAR) {
    for (const hacker of hackers) {
      if (!hacker.username) {
        continue;
      }

      const usernameKey = hacker.username.toLowerCase();
      const bounties = getBounties(hacker);

      if (!hackersByUsername.has(usernameKey)) {
        hackersByUsername.set(usernameKey, {
          username: hacker.username,
          total_value: 0,
          total_bounties: 0,
          projectNames: new Set(),
          years: [],
        });
      }

      const hackerSummary = hackersByUsername.get(usernameKey);
      hackerSummary.total_value += getTotalValue(hacker);
      hackerSummary.total_bounties += bounties.length;
      hackerSummary.years.push({
        year,
        bounties,
        num_projects: Number(hacker.num_projects || 0),
        total_value: getTotalValue(hacker),
      });

      for (const bounty of bounties) {
        if (bounty.project) {
          hackerSummary.projectNames.add(bounty.project);
        }
      }
    }
  }

  return Array.from(hackersByUsername.values())
    .map((hacker) => {
      const { projectNames, ...hackerSummary } = hacker;
      return {
        ...hackerSummary,
        num_projects: projectNames.size,
        years: hackerSummary.years.sort((a, b) => b.year - a.year),
      };
    })
    .sort((a, b) => {
      if (b.total_value !== a.total_value) {
        return b.total_value - a.total_value;
      }
      return a.username.localeCompare(b.username);
    });
};
