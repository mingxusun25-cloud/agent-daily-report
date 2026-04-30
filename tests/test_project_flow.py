import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_report import build_markdown_report
from scripts.summarize import build_rule_based_summary


class ProjectFlowTests(unittest.TestCase):
    def test_rule_based_summary_recommends_top_three_by_stars(self):
        projects = [
            {"name": "low", "full_name": "o/low", "description": "low", "stars": 2, "language": "Python", "url": "https://example.com/low", "updated_at": "2026-04-29T00:00:00Z"},
            {"name": "high", "full_name": "o/high", "description": "high", "stars": 200, "language": "TypeScript", "url": "https://example.com/high", "updated_at": "2026-04-29T00:00:00Z"},
            {"name": "mid", "full_name": "o/mid", "description": "mid", "stars": 50, "language": "Go", "url": "https://example.com/mid", "updated_at": "2026-04-29T00:00:00Z"},
            {"name": "third", "full_name": "o/third", "description": "third", "stars": 75, "language": "Python", "url": "https://example.com/third", "updated_at": "2026-04-29T00:00:00Z"},
        ]

        summary = build_rule_based_summary(projects)

        self.assertIn("overall_summary", summary)
        self.assertEqual([item["name"] for item in summary["recommendation"]], ["high", "third", "mid"])
        self.assertEqual(len(summary["project_summaries"]), 4)

    def test_markdown_report_contains_required_sections_and_project_details(self):
        projects = [
            {
                "name": "agent-demo",
                "full_name": "owner/agent-demo",
                "url": "https://github.com/owner/agent-demo",
                "description": "A demo AI agent project",
                "stars": 123,
                "language": "Python",
                "updated_at": "2026-04-29T12:34:56Z",
            }
        ]
        summary = {
            "overall_summary": "今天 AI Agent 项目保持活跃。",
            "project_summaries": [{"name": "agent-demo", "summary": "适合学习 Agent 工作流。"}],
            "recommendation": [{"name": "agent-demo", "reason": "Star 高且近期活跃。"}],
        }

        report = build_markdown_report(projects, summary, generated_at="2026-04-30 08:00")

        self.assertIn("# 今日 GitHub AI Agent 趋势报告", report)
        self.assertIn("生成时间：2026-04-30 08:00", report)
        self.assertIn("## 一、今日总体趋势", report)
        self.assertIn("### 1. agent-demo", report)
        self.assertIn("- Star：123", report)
        self.assertIn("- AI 总结：适合学习 Agent 工作流。", report)


if __name__ == "__main__":
    unittest.main()
