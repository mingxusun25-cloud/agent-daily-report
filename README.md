# GitHub AI Agent 趋势报告自动化

这个项目会自动抓取近期更新的 GitHub AI Agent 相关开源项目，调用 DeepSeek API 生成中文总结，输出 Markdown 报告，并通过 163 邮箱发送报告。项目也提供 GitHub Actions 定时任务，可每天自动运行并把最新报告提交回仓库。

## 项目功能

- 使用 GitHub Search API 搜索 `ai agent`、`llm agent`、`rag agent`、`autonomous agent`、`multi agent` 相关项目
- 优先筛选最近 7 天内更新、Star 数较高、非 fork 的项目
- 使用 DeepSeek OpenAI-compatible API 生成中文趋势总结
- 在未配置 DeepSeek API Key 时自动生成基础规则版总结
- 生成 `reports/latest_report.md`
- 使用 163 SMTP SSL 发送邮件
- 通过 GitHub Actions 每天北京时间 8 点自动执行

## 本地运行方法

1. 创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 复制环境变量模板并填写本地配置：

```bash
cp .env.example .env
```

4. 运行每日流程：

```bash
python scripts/run_daily.py
```

单独执行也可以：

```bash
python scripts/fetch_github.py
python scripts/summarize.py
python scripts/generate_report.py
python scripts/send_email.py
```

## `.env` 配置说明

本地运行会读取项目根目录的 `.env` 文件：

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
EMAIL_USER=your_163_email@example.163.com
EMAIL_PASS=your_163_smtp_authorization_code_here
EMAIL_TO=recipient@example.com
```

说明：

- `DEEPSEEK_API_KEY`：DeepSeek API Key
- `DEEPSEEK_MODEL`：DeepSeek 模型名，默认 `deepseek-chat`
- `EMAIL_USER`：163 邮箱账号
- `EMAIL_PASS`：163 邮箱 SMTP 授权码，不是登录密码
- `EMAIL_TO`：报告接收邮箱

如果没有配置 `DEEPSEEK_API_KEY`，脚本会生成基础规则版总结；如果邮箱变量缺失，脚本会跳过邮件发送。

## GitHub Secrets 配置说明

在 GitHub 仓库的 `Settings -> Secrets and variables -> Actions` 中添加以下 Repository Secrets：

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_MODEL`
- `EMAIL_USER`
- `EMAIL_PASS`
- `EMAIL_TO`

不要把真实密钥、邮箱授权码或 API Key 写入代码、README、日志或提交记录。

## GitHub Actions 定时执行说明

工作流文件位于 `.github/workflows/daily_report.yml`。

- 定时任务：每天 UTC 00:00 执行，对应北京时间 08:00
- 支持在 GitHub Actions 页面通过 `workflow_dispatch` 手动触发
- 运行后会提交更新后的 `reports/latest_report.md` 和 `data/latest_projects.json`

## 安全提醒

`.env` 已加入 `.gitignore`，请不要提交 `.env`。本地敏感信息只放在 `.env`，GitHub Actions 中使用 Repository Secrets 注入。
