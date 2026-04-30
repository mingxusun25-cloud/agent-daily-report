from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
STEPS = [
    ("抓取 GitHub 项目", "fetch_github.py"),
    ("生成 DeepSeek 总结", "summarize.py"),
    ("生成 Markdown 报告", "generate_report.py"),
    ("发送 163 邮件", "send_email.py"),
]


def run_step(name: str, script_name: str) -> None:
    script_path = ROOT_DIR / "scripts" / script_name
    print(f"\n==> {name}")
    result = subprocess.run([sys.executable, str(script_path)], cwd=ROOT_DIR, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"{name} 失败，退出码：{result.returncode}")


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")
    print("开始执行每日 GitHub AI Agent 趋势报告流程...")
    for name, script_name in STEPS:
        run_step(name, script_name)
    print("\n每日流程执行结束。")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"流程执行失败：{exc}", file=sys.stderr)
        sys.exit(1)
