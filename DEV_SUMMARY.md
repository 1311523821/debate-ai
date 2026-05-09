# DebateAI 开发总结

> **最后更新**: 2026-05-09
> **当前分支**: main
> **最新 commit**: `47a6c99` — feat: Phase 2 - 辩论历史、Prompt编辑器、多语言支持

---

## 📊 项目进度总览

| 模块 | 状态 | 说明 |
|------|------|------|
| 后端核心框架 | ✅ 完成 | FastAPI + SSE 流式输出 |
| LLM 客户端 | ✅ 完成 | httpx 异步，支持流式 |
| 辩论编排器 | ✅ 完成 | 多轮对话 + 共识判定 |
| Prompt 模板 | ✅ 完成 | 中英文结构化 Prompt |
| 文件解析器 | ✅ 完成 | PDF / 代码 / 纯文本（20+ 格式） |
| 配置管理 | ✅ 完成 | .env 双 LLM 配置 + localStorage |
| 前端页面 | ✅ 完成 | Alpine.js + Tailwind 暗色主题 |
| 辩论历史记录 | ✅ 完成 | localStorage 存储 + 侧边栏浏览 |
| 历史导出 | ✅ 完成 | Markdown / JSON 导出 |
| Agent Prompt 编辑器 | ✅ 完成 | 可自定义三个 Prompt |
| 多语言支持 | ✅ 完成 | 中英文一键切换 |
| 更多文件格式 | ✅ 完成 | 支持 20+ 种代码/文本格式 |
| 直接文本输入 | ✅ 完成 | 可跳过文件上传直接粘贴 |
| 集成测试 | ⬜ 待开发 | 端到端测试 |
| 部署配置 | ⬜ 待开发 | Docker / 生产环境 |

---

## ✅ Phase 2 完成内容 (2026-05-09)

### 辩论历史记录 / 导出
- 辩论结束后自动保存到 localStorage（最近 50 条）
- 右上角 📜 按钮打开侧边栏历史面板
- 每条记录显示：文件名、日期、模型、轮次
- 支持 Markdown 和 JSON 两种格式导出
- 单条删除和清空全部

### Agent 角色自定义（Prompt 编辑器）
- 配置面板新增「Prompt 编辑器」标签页
- 可自定义三个系统提示词：
  - Agent A（建议者）
  - Agent B（批评者）
  - 共识总结
- 支持一键重置为默认值
- Prompt 随配置一起持久化到 localStorage

### 多语言支持
- 右上角 EN / 中文 切换按钮
- 所有 UI 文本（按钮、提示、标签）支持中英文
- 语言偏好持久化到 localStorage
- 默认 Prompt 也随语言自动切换

### 更多文件格式
- 支持 20+ 种格式：PDF, .py, .js, .ts, .java, .cpp, .c, .h, .go, .rs, .rb, .php, .html, .css, .yaml, .yml, .toml, .xml, .sh, .sql, .md, .csv, .json

### 直接文本输入
- 新增可折叠的文本输入区
- 可跳过文件上传直接粘贴内容
- 适合快速测试或粘贴代码片段

---

## ✅ Phase 1 完成内容

### 后端 API (`backend/main.py`)
- `POST /api/upload` — 文件上传，支持多种格式
- `POST /api/debate` — SSE 流式辩论接口
- `GET /` — 前端入口
- CORS 全开，静态文件服务

### LLM 客户端 (`backend/llm/client.py`)
- httpx 异步调用 OpenAI 兼容 API
- 流式 / 非流式两种模式
- 统一接口：`async def chat(messages, stream=True)`

### 辩论引擎 (`backend/debate/`)
- **orchestrator.py** — 编排多轮辩论，yield 每条消息
- **prompts.py** — 5 个中文 Prompt 模板（A 初始分析 / B 审查 / A 回应 / B 回应 / 共识总结）
- **consensus.py** — 基于关键词的共识判定（连续 2 轮无新反对意见即达成共识）

### 文件解析 (`backend/parsers/`)
- `pdf_parser.py` — PyMuPDF 提取文本，支持多页
- `code_parser.py` — AST 提取函数/类结构摘要
- `text_parser.py` — UTF-8 文本读取

### 配置 (`backend/config.py`)
- 从 `.env` 读取 `LLM_A_*` 和 `LLM_B_*` 两组配置
- `MAX_ROUNDS` 默认 6 轮

### 前端 (`frontend/index.html`)
- 单 HTML 完整 SPA，零构建
- Alpine.js + Tailwind CSS 暗色主题
- PDF.js 浏览器端 PDF 解析
- marked.js + highlight.js Markdown 渲染 + 代码高亮
- SSE 流式辩论可视化（左右分栏实时展示）
- 配置持久化到 localStorage

---

## 🏗️ 项目结构

```
debate-ai/
├── README.md                    # 项目说明
├── PROJECT_PLAN.md              # 项目计划书
├── DEV_SUMMARY.md               # 本文件 — 开发总结
├── requirements.txt             # Python 依赖
├── __init__.py
├── frontend/
│   └── index.html               # 完整单页应用（含所有 CSS/JS）
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 入口
│   ├── config.py                # 配置管理
│   ├── llm/
│   │   ├── __init__.py
│   │   └── client.py            # LLM 调用客户端
│   ├── debate/
│   │   ├── __init__.py
│   │   ├── orchestrator.py      # 辩论编排器
│   │   ├── prompts.py           # Prompt 模板
│   │   └── consensus.py         # 共识判定
│   └── parsers/
│       ├── __init__.py
│       ├── pdf_parser.py        # PDF 解析
│       ├── code_parser.py       # 代码解析
│       └── text_parser.py       # 文本解析
└── .github/
    └── workflows/
        └── deploy.yml           # GitHub Pages 自动部署
```

---

## 📝 Commit 历史

| Hash | 日期 | 说明 |
|------|------|------|
| `47a6c99` | 2026-05-09 | feat: Phase 2 - 辩论历史、Prompt编辑器、多语言支持 |
| `1a01629` | 2026-05-08 | docs: 添加开发总结，记录进度和后续计划 |
| `3b7dbde` | 2026-05-08 | feat: 添加完整后端代码 |
| `ca5c58e` | 2026-05-08 | feat: static frontend for GitHub Pages deployment |
| `ad62c0b` | 2026-05-08 | init: project plan, README, env template, requirements |

---

## 🔜 后续开发计划

### Phase 3 — 平台化
- [ ] 预设辩论模板（论文审稿 / 代码 review / 方案对比）
- [ ] 辩论质量评分
- [ ] 辩论历史云端同步
- [ ] Docker 化部署（Dockerfile + docker-compose）
- [ ] API 限流与鉴权
- [ ] 日志与监控
