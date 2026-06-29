import json
import csv
from pathlib import Path

BOUNTY_WINNER_FORM = "https://airtable.com/appfhkqSH4zVtjha0/pagAP2GlpYyheivGA/form"
DATA_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = DATA_DIR / "emails.csv"

def extract_username(github_field):
    """Extracts the GitHub username from a URL or returns the username as-is."""
    github_field = github_field.strip()
    if github_field.startswith("http"):
        return github_field.rstrip("/").split("/")[-1].lower()
    return github_field.lower()

with (DATA_DIR / "hackers.json").open() as f:
    hackers = json.load(f)

username_email_map = {}
with (DATA_DIR / "signups.csv").open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for line in reader:
        raw_github = line["GitHub Username"]
        if not raw_github:
            continue
        username = extract_username(raw_github)
        if line["Email"]:
            username_email_map[username] = line["Email"]

def build_email_body(hacker, username):
    email_contents = f"Hey {username}!\n\nCongrats on a successful hackathon!"
    if len(hacker["bounties"]) > 1:
        email_contents += f""" We're so happy to see you were able to close {len(hacker["bounties"])} issues across {hacker["num_projects"]} projects. Here are the bounties we believe you should be rewarded for:\n\n"""
        for bounty in hacker["bounties"]:
            email_contents += (
                f'- [{bounty["title"]}]({bounty["url"]}): ${bounty["value"]}\n'
            )
        email_contents += "\n"
    else:
        bounty = hacker["bounties"][0]
        email_contents += f' Our records indicate you were responsible for closing "[{bounty["title"]}]({bounty["url"]})" worth ${bounty["value"]}. '

    email_contents += f"Hence, your total payout is **${hacker['total_value']}USD**! This information is also summarized at https://unitaryhack.dev/hackers/{username}/."
    email_contents += f""" It's now time to get you paid! We'll need to collect some information from you in order to make this happen. Would you please submit a (single!) response to [this form]({BOUNTY_WINNER_FORM}) at your earliest convenience? Once we have the necessary information, we can begin processing your payment."""
    email_contents += f" Additionally, if you'd like a certificate of participation, please reply to this email with the full name that you'd like to see on it."
    return email_contents


missing_registrations = []
with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["email address", "Github username", "Email body"],
    )
    writer.writeheader()
    for hacker in hackers:
        username = hacker["username"].lower()
        email = username_email_map.get(username, "")
        if not email:
            missing_registrations.append(username)
        writer.writerow(
            {
                "email address": email,
                "Github username": username,
                "Email body": build_email_body(hacker, username),
            }
        )

print(f"Wrote {len(hackers)} email rows to {OUTPUT_CSV}")
if missing_registrations:
    print(
        "Missing registration emails for: "
        + ", ".join(sorted(missing_registrations))
    )
