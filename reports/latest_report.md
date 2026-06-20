# 今日 GitHub AI Agent 趋势报告

生成时间：2026-06-20 02:05

## 一、今日总体趋势

当前开源AI Agent领域呈现出多范式并进的繁荣态势。一方面，以LangChain、Langflow、Dify和CrewAI为代表的框架层项目持续深耕Agent编排与工作流构建，提供从低代码到编程SDK的完整工具链；另一方面，以Cherry Studio、Eliza、ZeroClaw为代表的终端应用层项目聚焦于打造跨平台、高性能的个人AI助手或生产力工具。值得关注的是，Google推出的Gemini CLI和NousResearch的Hermes Agent分别代表了科技巨头和前沿研究机构在Agent化终端交互与自主成长Agent上的探索。整体趋势表明，Agent正从单一对话助手向具备自主规划、工具调用、多Agent协作能力的复杂系统演进，且技术栈以TypeScript和Python为主，Rust语言在追求高性能的轻量级基础设施中崭露头角。

## 二、热门项目列表

### 1. cherry-studio

- Star：47557
- 语言：TypeScript
- 更新时间：2026-06-20T02:04:16Z
- 地址：https://github.com/CherryHQ/cherry-studio
- 项目描述：AI productivity studio with smart chat, autonomous agents, and 300+ assistants. Unified access to frontier LLMs
- AI 总结：AI生产力工作室，提供智能聊天、自主Agent和300+预设助手，统一接入前沿大语言模型，旨在打造一站式的AI工作环境。

### 2. eliza

- Star：18606
- 语言：TypeScript
- 更新时间：2026-06-20T01:59:50Z
- 地址：https://github.com/elizaOS/eliza
- 项目描述：Open source agentic operating system
- AI 总结：开源Agent操作系统，致力于构建一个通用的、可扩展的Agent运行环境，让Agent能够像操作系统管理进程一样被管理和调度。

### 3. zeroclaw

- Star：31958
- 语言：Rust
- 更新时间：2026-06-20T01:57:39Z
- 地址：https://github.com/zeroclaw-labs/zeroclaw
- 项目描述：Fast, small, and fully autonomous AI personal assistant infrastructure, any OS, any platform — deploy anywhere, swap anything 🦀
- AI 总结：快速、小巧且完全自主的AI个人助手基础设施，使用Rust编写，支持任何操作系统和平台，强调可部署性和组件可替换性。

### 4. cline

- Star：63540
- 语言：TypeScript
- 更新时间：2026-06-20T01:57:23Z
- 地址：https://github.com/cline/cline
- 项目描述：Autonomous coding agent as an SDK, IDE extension, or CLI assistant.
- AI 总结：自主编码Agent，以SDK、IDE扩展或CLI助手的形式提供，旨在将AI编码能力深度集成到开发者的工作流中。

### 5. hermes-agent

- Star：197675
- 语言：Python
- 更新时间：2026-06-20T01:52:51Z
- 地址：https://github.com/NousResearch/hermes-agent
- 项目描述：The agent that grows with you
- AI 总结：一个与用户共同成长的Agent，由NousResearch开发，强调Agent的持续学习和个性化适应能力。

### 6. gemini-cli

- Star：105415
- 语言：TypeScript
- 更新时间：2026-06-20T01:40:00Z
- 地址：https://github.com/google-gemini/gemini-cli
- 项目描述：An open-source AI agent that brings the power of Gemini directly into your terminal.
- AI 总结：Google推出的开源AI Agent，将Gemini模型的能力直接带入终端，实现命令行界面的智能交互与任务自动化。

### 7. langflow

- Star：149854
- 语言：Python
- 更新时间：2026-06-20T01:39:47Z
- 地址：https://github.com/langflow-ai/langflow
- 项目描述：Langflow is a powerful tool for building and deploying AI-powered agents and workflows.
- AI 总结：强大的AI Agent和工作流构建与部署工具，提供可视化界面，降低Agent开发门槛，支持快速原型设计和生产级部署。

### 8. langchain

- Star：139721
- 语言：Python
- 更新时间：2026-06-19T23:48:07Z
- 地址：https://github.com/langchain-ai/langchain
- 项目描述：The agent engineering platform.
- AI 总结：Agent工程平台，提供构建、测试和部署AI Agent的完整框架和工具链，是当前最流行的Agent开发框架之一。

### 9. dify

- Star：145854
- 语言：TypeScript
- 更新时间：2026-06-19T23:46:03Z
- 地址：https://github.com/langgenius/dify
- 项目描述：Production-ready platform for agentic workflow development.
- AI 总结：生产就绪的Agent工作流开发平台，专注于帮助企业级用户快速构建和部署可靠的Agent应用。

### 10. crewAI

- Star：54000
- 语言：Python
- 更新时间：2026-06-19T22:58:19Z
- 地址：https://github.com/crewAIInc/crewAI
- 项目描述：Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks.
- AI 总结：多Agent协作框架，通过角色扮演和自主Agent编排，实现Agent间的协同智能，共同完成复杂任务。

## 三、最值得关注的项目

1. hermes-agent：拥有近20万星标，代表前沿研究机构在Agent自主成长与持续学习方向上的探索，其'与用户共同成长'的理念可能引领下一代个性化Agent的发展方向。
2. gemini-cli：由Google官方推出，将顶级大模型Gemini与终端深度结合，代表了科技巨头对Agent化CLI的重视，具有极高的技术示范效应和生态潜力。
3. zeroclaw：采用Rust语言开发，聚焦于高性能、跨平台和完全自主的轻量级Agent基础设施，在追求极致性能和低资源消耗的场景下具有独特优势，代表了Agent基础设施向系统级语言发展的趋势。

## 四、项目说明

本报告由 GitHub Actions / 本地脚本自动生成，项目数据来自 GitHub Search API，趋势总结由 DeepSeek API 或基础规则版总结生成。
