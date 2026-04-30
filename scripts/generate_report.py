from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT_DIR / "data" / "latest_projects.json"
SUMMARY_PATH = ROOT_DIR / "data" / "latest_summary.json"
REPORT_PATH = ROOT_DIR / "reports" / "latest_report.md"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _summary_map(summary: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in summary.get("project_summaries", []):
        text = item.get("summary", "")
        for key in (item.get("full_name"), item.get("name")):
            if key:
                mapping[key] = text
    return mapping


def build_markdown_report(
    projects: list[dict[str, Any]],
    summary: dict[str, Any],
    generated_at: str | None = None,
) -> str:
    generated_at = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M")
    summaries = _summary_map(summary)
    lines: list[str] = [
        "# 今日 GitHub AI Agent 趋势报告",
        "",
        f"生成时间：{generated_at}",
        "",
        "## 一、今日总体趋势",
        "",
        summary.get("overall_summary") or "暂无总体趋势总结。",
        "",
        "## 二、热门项目列表",
        "",
    ]

    if not projects:
        lines.extend(["今日暂无项目数据。", ""])
    for index, project in enumerate(projects, start=1):
        full_name = project.get("full_name") or project.get("name") or ""
        ai_summary = summaries.get(full_name) or summaries.get(project.get("name", "")) or "暂无 AI 总结。"
        lines.extend(
            [
                f"### {index}. {project.get('name') or full_name or 'Unknown'}",
                "",
                f"- Star：{project.get('stars', 0)}",
                f"- 语言：{project.get('language') or 'Unknown'}",
                f"- 更新时间：{project.get('updated_at') or 'Unknown'}",
                f"- 地址：{project.get('url') or 'Unknown'}",
                f"- 项目描述：{project.get('description') or '暂无描述'}",
                f"- AI 总结：{ai_summary}",
                "",
            ]
        )

    lines.extend(["## 三、最值得关注的项目", ""])
    recommendations = summary.get("recommendation", [])
    if not recommendations:
        lines.extend(["暂无推荐项目。", ""])
    for index, item in enumerate(recommendations[:3], start=1):
        name = item.get("name") or item.get("full_name") or "Unknown"
        reason = item.get("reason") or "暂无推荐理由。"
        lines.append(f"{index}. {name}：{reason}")
    lines.extend(
        [
            "",
            "## 四、项目说明",
            "",
            "本报告由 GitHub Actions / 本地脚本自动生成，项目数据来自 GitHub Search API，趋势总结由 DeepSeek API 或基础规则版总结生成。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    print("开始生成 Markdown 报告...")
    projects = _load_json(PROJECTS_PATH, [])
    summary = _load_json(SUMMARY_PATH, {"overall_summary": "", "project_summaries": [], "recommendation": []})
    report = build_markdown_report(projects, summary)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"报告已保存到 {REPORT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
