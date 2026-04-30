from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT_DIR / "data" / "latest_projects.json"
SUMMARY_PATH = ROOT_DIR / "data" / "latest_summary.json"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


def load_projects(path: Path = PROJECTS_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def build_rule_based_summary(projects: list[dict[str, Any]]) -> dict[str, Any]:
    if not projects:
        return {
            "overall_summary": "今日未抓取到符合条件的 GitHub AI Agent 项目，可能是 GitHub API 限流、网络异常或搜索结果为空。",
            "project_summaries": [],
            "recommendation": [],
        }

    languages = sorted({project.get("language") or "Unknown" for project in projects})
    top_projects = sorted(projects, key=lambda item: int(item.get("stars") or 0), reverse=True)[:3]
    project_summaries = []
    for project in projects:
        project_summaries.append(
            {
                "name": project.get("name", ""),
                "full_name": project.get("full_name", ""),
                "summary": (
                    f"{project.get('name', '该项目')} 近期保持更新，"
                    f"主要使用 {project.get('language') or 'Unknown'}，"
                    f"当前 Star 数为 {project.get('stars', 0)}。"
                    f"项目描述：{project.get('description') or '暂无描述'}"
                ),
            }
        )

    return {
        "overall_summary": (
            f"今日共发现 {len(projects)} 个近期更新的 AI Agent 相关项目。"
            f"项目主要涉及 {', '.join(languages)} 等技术栈，按 Star 和更新时间综合排序。"
        ),
        "project_summaries": project_summaries,
        "recommendation": [
            {
                "name": project.get("name", ""),
                "full_name": project.get("full_name", ""),
                "reason": f"Star 数较高（{project.get('stars', 0)}）且近期有更新，值得优先关注其 Agent 设计和实现方式。",
            }
            for project in top_projects
        ],
    }


def _extract_json(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def summarize_with_deepseek(projects: list[dict[str, Any]]) -> dict[str, Any]:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    model = os.getenv("DEEPSEEK_MODEL") or DEFAULT_MODEL
    if not api_key:
        print("未配置 DEEPSEEK_API_KEY，使用基础规则版总结。")
        return build_rule_based_summary(projects)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        prompt = (
            "你是技术趋势分析师。请基于下面的 GitHub AI Agent 项目列表生成中文结构化总结。"
            "只输出 JSON，不要 Markdown，不要额外解释。JSON 字段必须为："
            "overall_summary 字符串；project_summaries 数组，每项包含 name、full_name、summary；"
            "recommendation 数组，列出最值得关注的 3 个项目，每项包含 name、full_name、reason。\n\n"
            f"项目列表：\n{json.dumps(projects, ensure_ascii=False, indent=2)}"
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你擅长总结开源 AI Agent 项目的技术价值和趋势。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        content = completion.choices[0].message.content or ""
        summary = _extract_json(content)
        for key in ("overall_summary", "project_summaries", "recommendation"):
            summary.setdefault(key, [] if key != "overall_summary" else "")
        return summary
    except Exception as exc:
        print(f"DeepSeek 总结失败，已切换到基础规则版总结：{exc}")
        return build_rule_based_summary(projects)


def save_summary(summary: dict[str, Any], path: Path = SUMMARY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")
    print("开始生成项目总结...")
    projects = load_projects()
    summary = summarize_with_deepseek(projects)
    save_summary(summary)
    print(f"总结已保存到 {SUMMARY_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
