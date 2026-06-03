import json
import os
from collections import defaultdict
from pathlib import Path
import re
from typing import Any
from urllib.parse import quote
from urllib.parse import urlparse

import frontmatter
import github
import gitlab
from dotenv import load_dotenv

DATA_DIR = Path(__file__).resolve().parent
REPO_ROOT = DATA_DIR.parents[1]

load_dotenv(REPO_ROOT / ".env")

token = os.getenv("GH_TOKEN")
if token is None:
    raise RuntimeError("GH_TOKEN not set")


def github_client(token: str) -> github.Github:
    auth = getattr(github, "Auth", None)
    token_auth = getattr(auth, "Token", None) if auth else None
    if token_auth:
        try:
            return github.Github(auth=token_auth(token))
        except TypeError:
            pass
    return github.Github(token)


g = github_client(token)
gl_token = os.getenv("GL_TOKEN")
gl = gitlab.Gitlab(private_token=gl_token) if gl_token else None

PROJECT_PATH = REPO_ROOT / "src" / "projects"
CACHE_PATH = Path(
    os.getenv("SCRAPE_GITHUB_CACHE", DATA_DIR / ".cache" / "bounty_issues.json")
)
MIN_GH_REMAINING = int(os.getenv("GH_MIN_RATE_LIMIT_REMAINING", "100"))
CACHE_ENABLED = os.getenv("SCRAPE_GITHUB_NO_CACHE", "").lower() not in {
    "1",
    "true",
    "yes",
}


def load_issue_cache() -> dict[str, dict[str, Any]]:
    if not CACHE_ENABLED or not CACHE_PATH.exists():
        return {}
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        key: value
        for key, value in data.items()
        if isinstance(key, str) and isinstance(value, dict)
    }


def save_issue_cache(cache: dict[str, dict[str, Any]]) -> None:
    if not CACHE_ENABLED:
        return
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(cache, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


issue_cache = load_issue_cache()
network_fetches = 0


def cache_key(provider: str, repo_key: str, kind: str, issue_num: int) -> str:
    return f"{provider}:{repo_key}:{kind}:{issue_num}"


def github_core_remaining() -> int:
    overview = g.get_rate_limit()

    core = getattr(overview, "core", None)
    if core is not None:
        return core.remaining

    resources = getattr(overview, "resources", None)
    core = getattr(resources, "core", None) if resources is not None else None
    if core is not None:
        return core.remaining

    rate = getattr(overview, "rate", None)
    if rate is not None:
        return rate.remaining

    raw_data = getattr(overview, "raw_data", {})
    if isinstance(raw_data, dict):
        remaining = (
            raw_data.get("resources", {})
            .get("core", {})
            .get("remaining")
        )
        if remaining is None:
            remaining = raw_data.get("rate", {}).get("remaining")
        if remaining is not None:
            return int(remaining)

    raise RuntimeError("Could not read GitHub API rate limit remaining count.")


def ensure_github_rate_limit_budget() -> None:
    remaining = github_core_remaining()
    if remaining <= MIN_GH_REMAINING:
        raise RuntimeError(
            "GitHub API rate limit remaining "
            f"({remaining}) is at or below reserve ({MIN_GH_REMAINING}). "
            "Rerun later, lower GH_MIN_RATE_LIMIT_REMAINING, or use the cache."
        )


def cached_issue(
    provider: str,
    repo_key: str,
    kind: str,
    issue_num: int,
    fetch: Any,
) -> dict[str, Any]:
    global network_fetches

    key = cache_key(provider, repo_key, kind, issue_num)
    if key in issue_cache:
        return issue_cache[key]

    if provider == "github":
        ensure_github_rate_limit_budget()

    data = fetch()
    issue_cache[key] = data
    network_fetches += 1
    save_issue_cache(issue_cache)
    return data


def should_skip_provider(provider: str) -> bool:
    return provider == "gitlab" and gl is None


def URL_to_repo_info(url: str, fallback_provider: str = "github") -> tuple[str, str]:
    raw = url.strip().strip('"').strip("'")
    if raw.startswith(("github.com/", "gitlab.com/")):
        raw = f"https://{raw}"

    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host.endswith("github.com"):
        parts = [p for p in path.split("/") if p]
        if parts:
            return "github", "/".join(parts[:2])

    if host.endswith("gitlab.com"):
        if "/-/" in path:
            path = path.split("/-/", 1)[0]
        if path.endswith(".git"):
            path = path[: -len(".git")]
        if path:
            return "gitlab", path

    repo_like = re.match(r"^([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:$|[:#?\s])", raw)
    if repo_like:
        return fallback_provider, repo_like.group(1)

    raise ValueError(f"did not find string match for {url}")


def URL_to_repo_key(url: str) -> str:
    return URL_to_repo_info(url)[1]


def normalize_gitlab_state(state: str | None) -> str:
    if state == "opened":
        return "open"
    return state or "open"


def gitlab_usernames(values: list[Any]) -> list[str]:
    usernames: list[str] = []
    for value in values:
        if isinstance(value, dict):
            username = value.get("username")
            if username:
                usernames.append(username)
        elif isinstance(value, str):
            usernames.append(value)
    return usernames


def work_item_assignees(work_item: dict[str, Any]) -> list[str]:
    if isinstance(work_item.get("assignees"), list):
        return gitlab_usernames(work_item["assignees"])

    for widget in work_item.get("widgets", []):
        if not isinstance(widget, dict):
            continue
        if widget.get("type") != "assignees":
            continue
        for key in ("assignees", "users"):
            if isinstance(widget.get(key), list):
                return gitlab_usernames(widget[key])
    return []


def get_gitlab_work_item(repo_key: str, issue_num: int) -> dict[str, Any]:
    if gl is None:
        raise RuntimeError("GL_TOKEN not set; cannot fetch GitLab work items")
    project_id = quote(repo_key, safe="")
    return gl.http_get(f"/projects/{project_id}/work_items/{issue_num}")


def github_issue_url(repo_key: str, issue_num: int, kind: str) -> str:
    github_path = "pull" if kind == "pull" else "issues"
    return f"https://github.com/{repo_key}/{github_path}/{issue_num}"


def gitlab_issue_url(repo_key: str, issue_num: int, kind: str) -> str:
    gitlab_path = kind if kind in {"merge_requests", "work_items"} else "issues"
    return f"https://gitlab.com/{repo_key}/-/{gitlab_path}/{issue_num}"


def fetch_github_issue(repo_key: str, issue_num: int, kind: str) -> dict[str, Any]:
    repo = g.get_repo(repo_key)
    issue = repo.get_issue(number=issue_num)
    return {
        "title": issue.title,
        "state": issue.state,
        "assignees": [hacker.login for hacker in issue.assignees],
        "url": github_issue_url(repo_key, issue_num, kind),
    }


def fetch_gitlab_issue(repo_key: str, issue_num: int, kind: str) -> dict[str, Any]:
    if gl is None:
        raise RuntimeError("GL_TOKEN not set; cannot fetch GitLab issues")
    repo = gl.projects.get(repo_key)
    issue = repo.issues.get(issue_num)
    return {
        "title": issue.title,
        "state": normalize_gitlab_state(issue.state),
        "assignees": gitlab_usernames(issue.attributes.get("assignees", [])),
        "url": issue.attributes.get("web_url")
        or gitlab_issue_url(repo_key, issue_num, kind),
    }


def fetch_gitlab_merge_request(
    repo_key: str, issue_num: int, kind: str
) -> dict[str, Any]:
    if gl is None:
        raise RuntimeError("GL_TOKEN not set; cannot fetch GitLab merge requests")
    repo = gl.projects.get(repo_key)
    merge_request = repo.mergerequests.get(issue_num)
    return {
        "title": merge_request.title,
        "state": normalize_gitlab_state(merge_request.state),
        "assignees": gitlab_usernames(
            merge_request.attributes.get("assignees", [])
        ),
        "url": gitlab_issue_url(repo_key, issue_num, kind),
    }


def fetch_gitlab_work_item(repo_key: str, issue_num: int, kind: str) -> dict[str, Any]:
    try:
        work_item = get_gitlab_work_item(repo_key, issue_num)
    except gitlab.exceptions.GitlabHttpError as exc:
        if getattr(exc, "response_code", None) == 404:
            return fetch_gitlab_issue(repo_key, issue_num, kind)
        raise
    return {
        "title": work_item.get("title") or f"{repo_key}#{issue_num}",
        "state": normalize_gitlab_state(work_item.get("state")),
        "assignees": work_item_assignees(work_item),
        "url": gitlab_issue_url(repo_key, issue_num, kind),
    }


def fetch_bounty_issue(
    provider: str, repo_key: str, issue_num: int, kind: str
) -> dict[str, Any]:
    if provider == "github":
        return fetch_github_issue(repo_key, issue_num, kind)
    if kind == "merge_requests":
        return fetch_gitlab_merge_request(repo_key, issue_num, kind)
    if kind == "work_items":
        return fetch_gitlab_work_item(repo_key, issue_num, kind)
    return fetch_gitlab_issue(repo_key, issue_num, kind)


def get_project_info():
    # Sort project files to ensure deterministic processing order
    for path in sorted(PROJECT_PATH.glob("*.md")):
        yield frontmatter.load(str(path))


projects = {}
if gl is None:
    print("GL_TOKEN not set; skipping GitLab projects and bounties.")

for project in get_project_info():
    project_url = project["project_url"]
    provider, main_project_repo_key = URL_to_repo_info(project_url)
    project_key = project.get("id") or project["title"].lower()

    print(f"Processing project: {project_key} ({provider}.com/{main_project_repo_key})")

    if should_skip_provider(provider):
        print(f"Skipping project: {project_key} (GitLab token unavailable)")
        continue

    issue_list = []
    amount_available = 0
    total_bounty_amount = 0
    bounties = project.get("bounties", [])
    num_open_bounties = 0
    for bounty in bounties:
        repo_ref = bounty.get("repo")
        repo_provider, repo_key = (
            URL_to_repo_info(repo_ref, provider)
            if repo_ref
            else (provider, main_project_repo_key)
        )
        if should_skip_provider(repo_provider):
            print(
                "Skipping bounty: "
                f"{project_key} {repo_key}#{bounty['issue_num']} "
                "(GitLab token unavailable)"
            )
            continue

        total_bounty_amount += bounty["value"]
        bounty_kind = bounty.get("kind", "issues")
        issue_data = cached_issue(
            repo_provider,
            repo_key,
            bounty_kind,
            bounty["issue_num"],
            lambda: fetch_bounty_issue(
                repo_provider,
                repo_key,
                bounty["issue_num"],
                bounty_kind,
            ),
        )
        state = bounty.get("state") or issue_data.get("state", "open")
        assignees_from_issue = (
            [bounty.get("assignee")]
            if bounty.get("assignee")
            else issue_data.get("assignees", [])
        )
        if state == "open":
            amount_available += bounty["value"]
            num_open_bounties += 1
        # extra_assignees = [bounty.get("assignee")] if bounty.get("assignee") else []
        # all_assignees = set(assignees_from_issue + extra_assignees)
        issue_list.append(
            {
                "title": bounty.get("title")
                or issue_data.get("title")
                or f"{repo_key}#{bounty['issue_num']}",
                "state": state,
                "assignees": sorted(assignees_from_issue),
                "value": bounty["value"],
                "url": issue_data.get("url")
                or (
                    github_issue_url(repo_key, bounty["issue_num"], bounty_kind)
                    if repo_provider == "github"
                    else gitlab_issue_url(repo_key, bounty["issue_num"], bounty_kind)
                ),
            }
        )

    projects[project_key] = {
        "name": project["title"],
        "emoji": project.get("emoji", ""),
        "url": project["project_url"],
        "bounties": issue_list,
        "amount_available": amount_available,
        "total_amount": total_bounty_amount,
        "num_bounties": len(issue_list),
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

with (DATA_DIR / "hackers.json").open("w") as f:
    json.dump(hacker_info, f, indent=2, sort_keys=True)

with (DATA_DIR / "leaderboard.json").open("w") as f:
    json.dump(
        dict(sorted(leaderboard.items(), key=lambda hb: (-hb[1], hb[0]))),
        f,
        indent=2,
        sort_keys=True,
    )

with (DATA_DIR / "gh.json").open("w") as f:
    json.dump(projects, f, indent=2, sort_keys=True)

with (DATA_DIR / "stats.json").open("w") as f:
    json.dump(hack_stats, f, indent=2)

print(
    f"Fetched {network_fetches} issue records from APIs; "
    f"{len(issue_cache)} cached records available."
)
