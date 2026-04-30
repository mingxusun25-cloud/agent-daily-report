from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PROJECTS_PATH = DATA_DIR / "latest_projects.json"
SEARCH_URL = "https://api.github.com/search/repositories"
KEYWORDS = [
    "ai agent",
    "llm agent",
    "rag agent",
    "autonomous agent",
    "multi agent",
]


def _recent_cutoff(days: int = 7) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "github-ai-agent-daily-report",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _normalize_repo(repo: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": repo.get("name") or "",
        "full_name": repo.get("full_name") or "",
        "url": repo.get("html_url") or "",
        "description": repo.get("description") or "",
        "stars": int(repo.get("stargazers_count") or 0),
        "language": repo.get("language") or "Unknown",
        "updated_at": repo.get("pushed_at") or repo.get("updated_at") or "",
    }


def fetch_projects(limit: int = 10) -> list[dict[str, Any]]:
    cutoff = _recent_cutoff(7)
    candidates: dict[str, dict[str, Any]] = {}
    errors: list[str] = []

    for keyword in KEYWORDS:
        params = {
            "q": f'{keyword} pushed:>={cutoff} fork:false',
            "sort": "stars",
            "order": "desc",
            "per_page": 10,
        }
        try:
            response = requests.get(SEARCH_URL, headers=_headers(), params=params, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            errors.append(f"{keyword}: {exc}")
            continue

        for repo in response.json().get("items", []):
            if repo.get("fork"):
                continue
            full_name = repo.get("full_name")
            if full_name:
                candidates[full_name] = _normalize_repo(repo)

    projects = sorted(
        candidates.values(),
        key=lambda item: (item.get("updated_at", ""), item.get("stars", 0)),
        reverse=True,
    )[:limit]

    if not projects and errors:
        print("GitHub Search API 未返回项目，已保存空列表。错误摘要：")
        for error in errors[:3]:
            print(f"- {error}")

    return projects


def save_projects(projects: list[dict[str, Any]], path: Path = PROJECTS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")
    print("开始抓取 GitHub AI Agent 项目...")
    projects = fetch_projects()
    save_projects(projects)
    print(f"已保存 {len(projects)} 个项目到 {PROJECTS_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
