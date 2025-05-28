import json
import os
from collections import defaultdict
from urllib.parse import urlparse

import frontmatter
import github
import gitlab
from dotenv import load_dotenv

load_dotenv("../../.env")

token = os.getenv("GH_TOKEN")
if token is None:
    raise RuntimeError("GH_TOKEN not set")

g = github.Github(token)
gl = gitlab.Gitlab()  # "https://gitlab.com", private_token=os.getenv("GL_TOKEN"))

PROJECT_PATH = "../projects"


def URL_to_repo_key(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc in {"github.com", "gitlab.com"}:
        path = parsed.path.strip("/")
        if path:
            return path
    raise ValueError(f"did not find string match for {url}")


def get_project_info():
    # Sort project files to ensure deterministic processing order
    for filename in sorted(os.listdir(PROJECT_PATH)):
        if filename.endswith(".md"):
            yield frontmatter.load(os.path.join(PROJECT_PATH, filename))


projects = {}
for project in get_project_info():
    project_url = project["project_url"]
    main_project_repo_key = URL_to_repo_key(project_url)
    provider = "gitlab" if "gitlab.com" in project_url else "github"
    project_name = main_project_repo_key.split("/")[-1].lower()

    print(f"Processing project: {project_name} ({provider}.com/{main_project_repo_key})")

    issue_list = []
    amount_available = 0
    total_bounty_amount = 0
    bounties = project.get("bounties", [])
    num_open_bounties = 0
    for bounty in bounties:
        total_bounty_amount += bounty["value"]
        repo_ref = bounty.get("repo")
        repo_key = repo_ref or main_project_repo_key
        repo_provider = (
            "gitlab" if (repo_ref and "gitlab.com" in repo_ref) else provider
        )
        if repo_provider == "github":
            repo = g.get_repo(repo_key)
            issue = repo.get_issue(number=bounty["issue_num"])
            state = bounty.get("state") or issue.state
            assignees_from_issue = [hacker.login for hacker in issue.assignees]
            issue_url = f"https://github.com/{repo_key}/issues/{bounty['issue_num']}"
        else:
            repo = gl.projects.get(repo_key)
            issue = repo.issues.get(bounty["issue_num"])
            state = bounty.get("state") or issue.state
            state = "open" if state == "opened" else state
            assignees_from_issue = [
                a["username"] for a in issue.attributes.get("assignees", [])
            ]
            issue_url = f"https://gitlab.com/{repo_key}/-/issues/{bounty['issue_num']}"
        if state == "open":
            amount_available += bounty["value"]
            num_open_bounties += 1
        extra_assignees = [bounty.get("assignee")] if bounty.get("assignee") else []
        all_assignees = set(assignees_from_issue + extra_assignees)
        issue_list.append(
            {
                "title": issue.title,
                "state": state,
                "assignees": sorted(all_assignees),
                "value": bounty["value"],
                "url": issue_url,
            }
        )

    projects[project_name] = {
        "name": project["title"],
        "emoji": project.get("emoji", ""),
        "url": project["project_url"],
        "bounties": issue_list,
        "amount_available": amount_available,
        "total_amount": total_bounty_amount,
        "num_bounties": len(bounties),
        "num_open_bounties": num_open_bounties,
    }

hack_stats = {
    "num_bounties": 0,
    "total_bounty_value": 0,
    "num_open_bounties": 0,
    "open_bounty_value": 0,
    "num_closed_bounties": 0,
    "closed_bounty_value": 0,
}


hackers = defaultdict(list)
for project, data in sorted(projects.items()):
    for bounty in data["bounties"]:
        hack_stats["num_bounties"] += 1
        hack_stats["total_bounty_value"] += bounty["value"]
        hack_stats["num_open_bounties"] += 1 if bounty["state"] == "open" else 0
        hack_stats["open_bounty_value"] += (
            bounty["value"] if bounty["state"] == "open" else 0
        )
        hack_stats["num_closed_bounties"] += 1 if bounty["state"] == "closed" else 0
        hack_stats["closed_bounty_value"] += (
            bounty["value"] if bounty["state"] == "closed" else 0
        )
        if bounty["state"] == "closed":
            for hacker in bounty["assignees"]:
                hackers[hacker].append(
                    {
                        "url": bounty["url"],
                        "title": bounty["title"],
                        "project": project,
                        "value": int(bounty["value"] / len(bounty["assignees"])),
                    }
                )

hack_stats["num_hackers"] = len(hackers)

leaderboard = {hacker: len(bounties) for hacker, bounties in hackers.items()}
hacker_info = [
    {
        "username": hacker,
        "bounties": bounties,
        "num_projects": len(set(b["project"] for b in bounties)),
        "total_value": sum(b["value"] for b in bounties),
    }
    for hacker, bounties in sorted(hackers.items())
]

with open("hackers.json", "w") as f:
    json.dump(hacker_info, f, indent=2, sort_keys=True)

with open("leaderboard.json", "w") as f:
    json.dump(
        dict(sorted(leaderboard.items(), key=lambda hb: (-hb[1], hb[0]))),
        f,
        indent=2,
        sort_keys=True,
    )

with open("gh.json", "w") as f:
    json.dump(projects, f, indent=2, sort_keys=True)

with open("stats.json", "w") as f:
    json.dump(hack_stats, f, indent=2)
