from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT_DIR / "reports" / "latest_report.md"
SMTP_HOST = "smtp.163.com"
SMTP_PORT = 465
SUBJECT = "今日 GitHub AI Agent 趋势报告"


def send_report_email(report_path: Path = REPORT_PATH) -> bool:
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient = os.getenv("EMAIL_TO")
    if not user or not password or not recipient:
        print("邮箱环境变量不完整，跳过邮件发送。请配置 EMAIL_USER、EMAIL_PASS、EMAIL_TO。")
        return False

    if not report_path.exists():
        print(f"报告文件不存在，跳过邮件发送：{report_path}")
        return False

    body = report_path.read_text(encoding="utf-8")
    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = SUBJECT
    message["From"] = user
    message["To"] = recipient

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.login(user, password)
        server.sendmail(user, [recipient], message.as_string())
    print("邮件发送完成。")
    return True


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")
    print("开始发送邮件...")
    send_report_email()


if __name__ == "__main__":
    main()
