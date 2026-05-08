# DebateAI — 双模型对抗辩论平台

> 两个 AI 围绕你的论文/代码展开辩论，互相挑刺、互相改进，最终达成共识。

## 项目背景

在科研和工程实践中，单一 LLM 的输出往往存在盲点。通过让两个不同模型（如 Gemini 和 DeepSeek）进行结构化对抗辩论，可以：
- 暴露单一模型的思维盲区
- 通过互相纠错提升输出质量
- 最终收敛到双方都认可的高质量结论

本项目将这一流程产品化为一个可视化 Web 应用。

## 核心功能

### 1. 材料上传
- 支持 PDF（论文）、Python 代码（.py）、纯文本
- 自动解析内容，提取关键信息作为辩论素材

### 2. 双 Agent 辩论
- 左右分栏实时展示两个 Agent 的对话
- Agent A（建议者）：分析材料，提出改进建议
- Agent B（批评者）：审查建议，指出漏洞，提出替代方案
- 多轮交替辩论，流式输出

### 3. 共识判定
- 当双方不再有实质性分歧时，自动结束辩论
- 提炼最终共识结论
- 如涉及代码，输出合并后的改进代码

### 4. 可配置性
- 支持选择不同的 LLM provider（OpenAI / DeepSeek / Gemini / 本地模型等）
- 可调节辩论轮次上限（默认 6 轮）
- 可自定义 Agent 角色 prompt

## 技术架构

```
┌─────────────────────────────────────────────┐
│                Frontend (SPA)               │
│         HTML + Tailwind + Alpine.js         │
│  ┌──────────────┬──────────────────────┐    │
│  │  Agent A 面板 │  Agent B 面板        │    │
│  │  (左侧)      │  (右侧)              │    │
│  └──────────────┴──────────────────────┘    │
│  ┌──────────────────────────────────────┐   │
│  │  共识结论 + 代码输出区                │   │
│  └──────────────────────────────────────┘   │
└─────────────────────┬───────────────────────┘
                      │ SSE (Server-Sent Events)
                      ▼
┌─────────────────────────────────────────────┐
│             Backend (FastAPI)               │
│                                             │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ File Parser  │  │  Debate Orchestrator │  │
│  │ PDF/Code/Text│  │  轮次控制 + 共识判定  │  │
│  └─────────────┘  └──────────────────────┘  │
│                     │                       │
│         ┌───────────┴───────────┐           │
│         ▼                       ▼           │
│  ┌─────────────┐        ┌─────────────┐    │
│  │  LLM Client │        │  LLM Client │    │
│  │  (Agent A)  │        │  (Agent B)  │    │
│  └─────────────┘        └─────────────┘    │
│                                             │
│  OpenAI 兼容 API，支持多 Provider           │
└─────────────────────────────────────────────┘
```

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML + Tailwind CSS + Alpine.js | 零构建，单文件部署 |
| 后端 | Python + FastAPI + SSE | 轻量高效 |
| LLM | OpenAI 兼容 API | 支持 OpenAI / DeepSeek / Gemini / 任意兼容 provider |
| 文件解析 | PyMuPDF (PDF) + AST (Python) + 标准库 | 纯 Python，无重依赖 |
| 部署 | 本地运行 / Docker | 开发阶段本地，后续可容器化 |

## 项目结构

```
debate-ai/
├── README.md                # 项目说明
├── PROJECT_PLAN.md          # 本文件
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量模板
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── debate/
│   │   ├── orchestrator.py  # 辩论编排器（核心）
│   │   ├── prompts.py       # Agent prompt 模板
│   │   └── consensus.py     # 共识判定逻辑
│   ├── llm/
│   │   ├── client.py        # 统一 LLM 客户端
│   │   └── providers.py     # 多 provider 适配
│   └── parsers/
│       ├── pdf_parser.py    # PDF 解析
│       ├── code_parser.py   # 代码解析
│       └── text_parser.py   # 纯文本处理
├── frontend/
│   └── index.html           # 单页应用（含所有 CSS/JS）
└── docs/
    └── screenshots/         # 截图（上线后补充）
```

## 开发阶段

### Phase 1 — MVP（当前）
- [x] 项目计划书
- [ ] 后端：FastAPI 框架 + 辩论编排器
- [ ] 后端：OpenAI 兼容 LLM 客户端
- [ ] 后端：PDF / 代码文件解析
- [ ] 前端：左右分栏辩论 UI + SSE 实时流
- [ ] 前端：文件上传 + 共识结论展示
- [ ] 本地可运行，README 含使用说明

### Phase 2 — 增强
- [ ] 辩论历史记录 / 导出
- [ ] 多语言支持（中英文）
- [ ] Agent 角色自定义（prompt 编辑器）
- [ ] 辩论质量评分
- [ ] Docker 一键部署

### Phase 3 — 平台化
- [ ] 用户系统 + 历史管理
- [ ] 预设辩论模板（论文审稿 / 代码 review / 方案对比）
- [ ] 支持更多文件格式（Word、Jupyter Notebook）
- [ ] API 开放接口

## 使用流程

1. 启动后端 `python backend/main.py`
2. 浏览器打开 `http://localhost:8000`
3. 配置两个 LLM 的 API Key 和模型名
4. 上传材料（PDF / .py / 文本）
5. 点击「开始辩论」
6. 观察左右两个 Agent 实时辩论
7. 阅读底部共识结论和改进代码

## 环境变量

```bash
# Agent A 的 LLM 配置
LLM_A_BASE_URL=https://api.openai.com/v1
LLM_A_API_KEY=sk-xxx
LLM_A_MODEL=gpt-4o

# Agent B 的 LLM 配置
LLM_B_BASE_URL=https://api.deepseek.com/v1
LLM_B_API_KEY=sk-xxx
LLM_B_MODEL=deepseek-chat
```

## License

MIT
