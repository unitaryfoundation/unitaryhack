#!/usr/bin/env python3

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class ParsedBounty:
    issue_num: int
    value: int
    repo_key: str
    provider: str


@dataclass(frozen=True)
class ProjectFile:
    path: Path
    title: str
    project_url: str
    repo_key: str
    id: Optional[str]

    @property
    def stem_key(self) -> str:
        return normalize_token(self.path.stem)

    @property
    def title_key(self) -> str:
        return normalize_token(self.title)

    @property
    def id_key(self) -> Optional[str]:
        return normalize_token(self.id) if self.id else None

    @property
    def archive_rank(self) -> int:
        return 1 if "archive" in self.path.parts else 0


def normalize_token(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def first_nonempty(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value and value.strip():
            return value.strip()
    return ""


def parse_money(amount: Optional[str]) -> Optional[int]:
    if not amount:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", amount.replace(",", ""))
    if not match:
        return None
    as_float = float(match.group(1))
    if as_float < 0:
        return None
    return int(as_float)


def parse_repo_key_from_url(url: str) -> Optional[str]:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host.endswith("github.com"):
        parts = [p for p in path.split("/") if p]
        if len(parts) < 2:
            return None
        return f"{parts[0]}/{parts[1]}"

    if host.endswith("gitlab.com"):
        if "/-/" in path:
            return path.split("/-/", 1)[0]
        if path.endswith(".git"):
            path = path[: -len(".git")]
        return path or None

    return None


def parse_provider_from_url(url: str) -> Optional[str]:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    if host.endswith("github.com"):
        return "github"
    if host.endswith("gitlab.com"):
        return "gitlab"
    return None


def parse_namespace_from_url(url: str) -> Optional[tuple[str, str]]:
    url = url.strip()
    if not url:
        return None

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")
    if "/-/" in path:
        path = path.split("/-/", 1)[0]

    parts = [p for p in path.split("/") if p]
    if not parts:
        return None

    if host.endswith("github.com"):
        return ("github", parts[0])
    if host.endswith("gitlab.com"):
        return ("gitlab", parts[0])
    return None


def canonical_repo_url(provider: str, repo_key: str) -> str:
    if provider == "github":
        return f"https://github.com/{repo_key}"
    if provider == "gitlab":
        return f"https://gitlab.com/{repo_key}"
    raise ValueError(f"Unknown provider: {provider}")


def parse_issue_num_from_url(url: str) -> Optional[int]:
    url = url.strip()
    match = re.search(r"/(?:issues|pull|merge_requests)/(\d+)", url)
    if match:
        return int(match.group(1))
    match = re.search(r"/-/issues/(\d+)", url)
    if match:
        return int(match.group(1))
    return None


def parse_bounty(url: Optional[str], amount: Optional[str]) -> Optional[ParsedBounty]:
    if not url:
        return None
    url = url.strip()
    if not url:
        return None

    issue_num = parse_issue_num_from_url(url)
    if issue_num is None:
        return None

    provider = parse_provider_from_url(url)
    if not provider:
        return None

    repo_key = parse_repo_key_from_url(url)
    if not repo_key:
        return None

    value = parse_money(amount)
    if value is None:
        return None

    return ParsedBounty(issue_num=issue_num, value=value, repo_key=repo_key, provider=provider)


def split_front_matter(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("file does not start with YAML front matter delimiter '---'")

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("file does not contain closing YAML front matter delimiter '---'")

    return lines[: end_idx + 1], lines[end_idx + 1 :]


def extract_front_matter_value(
    front_matter_lines: list[str], key: str
) -> Optional[str]:
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*?)\s*$")
    for line in front_matter_lines:
        match = pattern.match(line.rstrip("\r\n"))
        if not match:
            continue
        raw = match.group(1).strip()
        if (raw.startswith('"') and raw.endswith('"')) or (
            raw.startswith("'") and raw.endswith("'")
        ):
            raw = raw[1:-1]
        return raw.strip()
    return None


def load_project_files(projects_dir: Path) -> list[ProjectFile]:
    project_files: list[ProjectFile] = []
    for path in sorted(projects_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        front, _ = split_front_matter(text)
        # front includes the opening and closing '---' lines; metadata is between them.
        front_matter_lines = front[1:-1]

        title = extract_front_matter_value(front_matter_lines, "title") or ""
        project_url = extract_front_matter_value(front_matter_lines, "project_url") or ""
        project_id = extract_front_matter_value(front_matter_lines, "id")
        repo_key = parse_repo_key_from_url(project_url) or ""
        if not title or not project_url or not repo_key:
            # Skip malformed project files rather than crashing.
            continue
        project_files.append(
            ProjectFile(
                path=path,
                title=title,
                project_url=project_url,
                repo_key=repo_key,
                id=project_id,
            )
        )
    return project_files


def choose_project_file(
    row_project_name: str,
    row_project_repo_url: Optional[str],
    project_files: Iterable[ProjectFile],
    repo_key_to_project: dict[str, ProjectFile],
) -> Optional[ProjectFile]:
    row_repo_key = (
        parse_repo_key_from_url(row_project_repo_url) if row_project_repo_url else None
    )
    if row_repo_key:
        matched = repo_key_to_project.get(row_repo_key.lower())
        if matched:
            return matched

    row_key = normalize_token(row_project_name)
    if not row_key:
        return None

    exact_matches: list[ProjectFile] = []
    for project in project_files:
        if row_key in {project.stem_key, project.title_key, project.id_key}:
            exact_matches.append(project)

    if exact_matches:
        exact_matches.sort(key=lambda project: (project.archive_rank, len(project.path.parts)))
        return exact_matches[0]
    return None


def render_bounties_yaml(
    bounties: list[ParsedBounty], *, main_repo_key: str
) -> list[str]:
    lines: list[str] = []
    if not bounties:
        return ["bounties: []\n"]

    lines.append("bounties:\n")
    for bounty in bounties:
        lines.append(f"  - issue_num: {bounty.issue_num}\n")
        lines.append(f"    value: {bounty.value}\n")
        if bounty.repo_key.lower() != main_repo_key.lower():
            lines.append(f"    repo: {bounty.repo_key}\n")
    return lines


def update_bounties_in_markdown(
    text: str, bounties: list[ParsedBounty], *, project_url_override: Optional[str] = None
) -> str:
    front, body = split_front_matter(text)
    front_matter_lines = front[1:-1]

    project_url = extract_front_matter_value(front_matter_lines, "project_url")
    if not project_url:
        raise ValueError("project_url not found in front matter")

    effective_project_url = (project_url_override or project_url).strip()
    main_repo_key = parse_repo_key_from_url(effective_project_url)
    if not main_repo_key:
        raise ValueError(
            f"could not parse repo key from project_url: {effective_project_url}"
        )

    if project_url_override:
        updated_project_url_line = f"project_url: {effective_project_url}\n"
        replaced = False
        for idx, line in enumerate(front_matter_lines):
            if line.startswith("project_url:"):
                front_matter_lines[idx] = updated_project_url_line
                replaced = True
                break
        if not replaced:
            front_matter_lines.append(updated_project_url_line)

    bounty_block = render_bounties_yaml(bounties, main_repo_key=main_repo_key)

    start_idx = None
    for idx, line in enumerate(front_matter_lines):
        if line.rstrip("\r\n") == "bounties:":
            start_idx = idx
            break

    if start_idx is None:
        front_matter_lines.extend(bounty_block)
    else:
        # Replace existing block lines following `bounties:` until the next
        # non-indented, non-empty line (i.e., the next top-level YAML key).
        end_idx = start_idx + 1
        while end_idx < len(front_matter_lines):
            candidate = front_matter_lines[end_idx]
            if candidate.strip() == "":
                end_idx += 1
                continue
            if candidate.startswith((" ", "\t")):
                end_idx += 1
                continue
            break

        front_matter_lines[start_idx:end_idx] = bounty_block

    updated_front = ["---\n", *front_matter_lines, "---\n"]
    return "".join(updated_front + body)


def parse_csv_bounties(row: dict[str, str]) -> list[ParsedBounty]:
    bounties: list[ParsedBounty] = []
    for i in range(1, 7):
        if i == 1:
            url_value = first_nonempty(
                row, "Bounty URL", "Bountry URL", "Bounty 1 URL"
            )
            amt_value = first_nonempty(row, "Bounty Amount", "Bounty 1 Amount")
        else:
            url_value = first_nonempty(row, f"Bounty {i} URL")
            amt_value = first_nonempty(row, f"Bounty {i} Amount")
        bounty = parse_bounty(url_value, amt_value)
        if bounty:
            bounties.append(bounty)
    return bounties


def is_truthy(value: Optional[str]) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "withdrawn"}


def slugify_filename(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled-project"


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def clean_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return value.replace("\u00a0", " ").replace("\r\n", "\n").strip()


def dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(value)
    return ordered


def parse_csv_tags(row: dict[str, str]) -> list[str]:
    raw = first_nonempty(row, "Project Tags")
    if not raw:
        return []
    return dedupe_preserve_order(
        tag.strip() for tag in clean_text(raw).split(",") if tag.strip()
    )


def extract_markdown_body(text: str) -> str:
    _, body = split_front_matter(text)
    return "".join(body).strip()


def parse_csv_created_date(value: str) -> Optional[str]:
    raw = value.strip()
    if not raw:
        return None

    for fmt in ("%m/%d/%Y %I:%M%p", "%m/%d/%Y %H:%M", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def derive_project_id(
    project_url: str,
    project_name: str,
    *,
    preferred_id: Optional[str] = None,
) -> str:
    if preferred_id and preferred_id.strip():
        return preferred_id.strip()

    parsed = urlparse(project_url.strip())
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if parts:
        return parts[-1].removesuffix(".git").lower()

    return slugify_filename(project_name)


def choose_output_path(
    project_name: str, matched_project: Optional[ProjectFile], projects_dir: Path
) -> Path:
    if matched_project:
        if "archive" in matched_project.path.parts:
            return projects_dir / matched_project.path.name
        return matched_project.path
    return projects_dir / f"{slugify_filename(project_name)}.md"


def extract_existing_tags(text: str) -> list[str]:
    front, _ = split_front_matter(text)
    lines = front[1:-1]

    tags: list[str] = []
    capture = False
    for line in lines:
        stripped = line.rstrip("\r\n")
        if stripped == "tags:":
            capture = True
            continue
        if capture:
            if stripped.startswith("  - "):
                tags.append(stripped[4:].strip().strip('"').strip("'"))
                continue
            if stripped.startswith((" ", "\t")) or stripped == "":
                continue
            break
    return tags


def render_tags_yaml(tags: list[str]) -> list[str]:
    if not tags:
        return ["tags: []\n"]

    lines = ["tags:\n"]
    for tag in tags:
        lines.append(f"  - {yaml_scalar(tag)}\n")
    return lines


def render_project_markdown(
    *,
    row: dict[str, str],
    output_path: Path,
    matched_project: Optional[ProjectFile],
    bounties: list[ParsedBounty],
) -> str:
    existing_text = (
        output_path.read_text(encoding="utf-8") if output_path.exists() else None
    )
    matched_text = (
        matched_project.path.read_text(encoding="utf-8")
        if matched_project and matched_project.path.exists()
        else None
    )

    title = clean_text(
        first_nonempty(
            row,
            "Project Name",
            "Please Pick Project Name",
            "Name (from Invited Projects)",
            "Participating Project",
        )
    )
    project_url = clean_text(first_nonempty(row, "Project URL", "Project Repo URL"))
    summary = clean_text(first_nonempty(row, "Project Short Description"))
    emoji = clean_text(first_nonempty(row, "Project Emoji"))
    description = clean_text(first_nonempty(row, "Project Description"))

    if not emoji and existing_text:
        front, _ = split_front_matter(existing_text)
        emoji = clean_text(extract_front_matter_value(front[1:-1], "emoji"))
    if not emoji and matched_text:
        front, _ = split_front_matter(matched_text)
        emoji = clean_text(extract_front_matter_value(front[1:-1], "emoji"))

    project_id = derive_project_id(
        project_url,
        title,
        preferred_id=matched_project.id if matched_project else None,
    )

    meta_description = summary or clean_text(first_nonempty(row, "Project Description"))
    body = (
        description
        or (extract_markdown_body(existing_text) if existing_text else "")
        or (extract_markdown_body(matched_text) if matched_text else "")
        or summary
    )

    tags = parse_csv_tags(row)
    if not tags and existing_text:
        tags = extract_existing_tags(existing_text)
    if not tags and matched_text:
        tags = extract_existing_tags(matched_text)

    existing_date = None
    if existing_text:
        front, _ = split_front_matter(existing_text)
        existing_date = extract_front_matter_value(front[1:-1], "date")
    date_value = (
        parse_csv_created_date(first_nonempty(row, "Created"))
        or existing_date
        or datetime.now().date().isoformat()
    )

    main_repo_key = parse_repo_key_from_url(project_url) or ""

    lines = ["---\n"]
    lines.append(f"title: {yaml_scalar(title)}\n")
    lines.append(f"id: {yaml_scalar(project_id)}\n")
    if emoji:
        lines.append(f"emoji: {yaml_scalar(emoji)}\n")
    else:
        lines.append("emoji:\n")
    lines.append(f"project_url: {yaml_scalar(project_url)}\n")
    lines.append(f"metaDescription: {yaml_scalar(meta_description)}\n")
    lines.append(f"date: {date_value}\n")
    lines.append(f"summary: {yaml_scalar(summary or meta_description)}\n")
    lines.extend(render_tags_yaml(tags))
    lines.extend(render_bounties_yaml(bounties, main_repo_key=main_repo_key))
    lines.append("---\n\n")
    lines.append(body.rstrip() + "\n")
    return "".join(lines)


def ensure_projects_defaults(projects_dir: Path, *, dry_run: bool) -> Optional[Path]:
    defaults_path = projects_dir / "projects.json"
    desired = '{\n  "layout": "project.njk",\n  "permalink": "projects/{{ title | slug }}/index.html",\n  "tags": ["project"]\n}\n'

    if defaults_path.exists():
        current = defaults_path.read_text(encoding="utf-8")
        if current == desired:
            return None
    if not dry_run:
        defaults_path.write_text(desired, encoding="utf-8")
    return defaults_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Populate per-project `bounties:` front matter from a CSV export."
    )
    repo_root = Path(__file__).resolve().parents[2]
    parser.add_argument(
        "csv_path",
        nargs="?",
        help="Optional positional path to the CSV export.",
    )
    parser.add_argument(
        "--csv",
        default=str(repo_root / "Participating Projects-Projects.csv"),
        help="Path to the CSV export (default: repo root CSV).",
    )
    parser.add_argument(
        "--projects-dir",
        default=str(repo_root / "src" / "projects"),
        help="Directory containing project markdown files (default: src/projects).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files.",
    )
    parser.add_argument(
        "--sync-project-url",
        action="store_true",
        help="If the CSV project URL points to a different repo than the markdown `project_url`, update the markdown to match.",
    )
    parser.add_argument(
        "--strict-project-url-match",
        action="store_true",
        help="Fail (non-zero exit) when a CSV row does not match the markdown `project_url`.",
    )
    args = parser.parse_args(argv)

    csv_path = Path(args.csv_path or args.csv)
    projects_dir = Path(args.projects_dir)
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        return 2
    if not projects_dir.exists():
        print(f"Projects dir not found: {projects_dir}", file=sys.stderr)
        return 2

    project_files = load_project_files(projects_dir)
    repo_key_to_project: dict[str, ProjectFile] = {}
    for project in sorted(project_files, key=lambda p: (p.archive_rank, len(p.path.parts))):
        repo_key_to_project.setdefault(project.repo_key.lower(), project)

    created_files: list[Path] = []
    updated_files: list[Path] = []
    defaults_updated: Optional[Path] = ensure_projects_defaults(
        projects_dir, dry_run=args.dry_run
    )
    skipped_rows: list[str] = []
    path_collisions: list[str] = []
    mismatched_project_urls: list[str] = []
    strict_failed = False
    rows_with_bounty_data = 0
    seen_output_paths: dict[Path, str] = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_name = first_nonempty(
                row,
                "Project Name",
                "Please Pick Project Name",
                "Name (from Invited Projects)",
                "Participating Project",
            )
            if not row_name:
                continue

            if is_truthy(first_nonempty(row, "Withdrawn")):
                skipped_rows.append(f"{row_name}: marked withdrawn")
                continue

            row_project_repo_url = (
                first_nonempty(row, "Project URL", "Project Repo URL") or None
            )
            if not row_project_repo_url:
                skipped_rows.append(f"{row_name}: missing Project URL")
                continue

            bounties = parse_csv_bounties(row)
            if bounties:
                rows_with_bounty_data += 1

            project = choose_project_file(
                row_project_name=row_name,
                row_project_repo_url=row_project_repo_url,
                project_files=project_files,
                repo_key_to_project=repo_key_to_project,
            )
            output_path = choose_output_path(row_name, project, projects_dir)

            prior_row = seen_output_paths.get(output_path)
            if prior_row:
                path_collisions.append(
                    f"{prior_row} and {row_name} both map to {output_path}"
                )
                strict_failed = True
                continue
            seen_output_paths[output_path] = row_name

            if output_path.exists():
                existing_text = output_path.read_text(encoding="utf-8")
                existing_front, _ = split_front_matter(existing_text)
                existing_project_url = extract_front_matter_value(
                    existing_front[1:-1], "project_url"
                )
                if (
                    existing_project_url
                    and existing_project_url.strip() != row_project_repo_url.strip()
                ):
                    mismatch_msg = (
                        f"{row_name}: CSV Project URL '{row_project_repo_url}' vs "
                        f"{output_path} project_url '{existing_project_url}'"
                    )
                    mismatched_project_urls.append(mismatch_msg)
                    if args.strict_project_url_match:
                        strict_failed = True
                        continue

            rendered = render_project_markdown(
                row=row,
                output_path=output_path,
                matched_project=project,
                bounties=bounties,
            )

            original = output_path.read_text(encoding="utf-8") if output_path.exists() else None
            if rendered != original:
                if output_path.exists():
                    updated_files.append(output_path)
                else:
                    created_files.append(output_path)
                if not args.dry_run:
                    output_path.write_text(rendered, encoding="utf-8")

    if args.dry_run:
        if defaults_updated:
            print(f"Would update: {defaults_updated}")
        for path in created_files:
            print(f"Would create: {path}")
        for path in updated_files:
            print(f"Would update: {path}")
    else:
        if defaults_updated:
            print(f"Updated: {defaults_updated}")
        for path in created_files:
            print(f"Created: {path}")
        for path in updated_files:
            print(f"Updated: {path}")

    if not project_files:
        print(
            f"No project markdown files found under {projects_dir}.",
            file=sys.stderr,
        )

    if rows_with_bounty_data == 0:
        print(
            "No rows with parseable bounty URL + amount data were found in the CSV.",
            file=sys.stderr,
        )

    if skipped_rows:
        print("Skipped CSV rows:", file=sys.stderr)
        for item in skipped_rows:
            print(f"  - {item}", file=sys.stderr)

    if path_collisions:
        print("Output path collisions:", file=sys.stderr)
        for item in path_collisions:
            print(f"  - {item}", file=sys.stderr)

    if mismatched_project_urls:
        header = "Project URL mismatches (CSV vs markdown `project_url`):"
        if args.strict_project_url_match:
            header += " (strict)"
        print(header, file=sys.stderr)
        for item in mismatched_project_urls:
            print(f"  - {item}", file=sys.stderr)

    if strict_failed:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
