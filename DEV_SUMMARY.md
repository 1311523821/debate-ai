# DebateAI 开发总结

> **最后更新**: 2026-05-09
> **当前分支**: main
> **最新 commit**: Phase 2 功能完成

---

## 📊 项目进度总览

| 模块 | 状态 | 说明 |
|------|------|------|
| 后端核心框架 | ✅ 完成 | FastAPI + SSE 流式输出 |
| LLM 客户端 | ✅ 完成 | httpx 异步，支持流式 |
| 辩论编排器 | ✅ 完成 | 多轮对话 + 共识判定 |
| Prompt 模板 | ✅ 完成 | 中英文结构化 Prompt |
| 文件解析器 | ✅ 完成 | PDF / Python / 纯文本 |
| 配置管理 | ✅ 完成 | .env 双 LLM 配置 |
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
- 侧边栏历史面板，显示文件名、日期、模型、轮次
- 支持 Markdown 和 JSON 两种导出格式
- 单条删除和清空全部

### Agent 角色自定义（Prompt 编辑器）
- 配置面板新增 "Prompt 编辑器" 标签页
- 可自定义 Agent A（建议者）、Agent B（批评者）、共识总结 三个系统提示词
- 支持重置为默认值
- Prompt 随配置一起持久化到 localStorage

### 多语言支持
- 右上角中英文切换按钮
- 所有 UI 文本支持中英文
- 语言偏好持久化
- 默认 Prompt 也随语言切换

### 更多文件格式
- 支持 20+ 种格式：PDF, Python, JS, TS, Java, C/C++, Go, Rust, Ruby, PHP, HTML, CSS, YAML, TOML, XML, Shell, SQL, Markdown, CSV, JSON

### 直接文本输入
- 新增可折叠的文本输入区，可跳过文件上传直接粘贴内容
- 适合快速测试或粘贴代码片段

---

## ✅ Phase 1 完成内容

### 后端 API (`backend/main.py`)
- `POST /api/upload` — 文件上传
- `POST /api/debate` — SSE 流式辩论
- `GET /` — 前端入口
- CORS + 静态文件服务

### LLM 客户端 (`backend/llm/client.py`)
- httpx 异步 OpenAI 兼容 API
- 流式 / 非流式统一接口

### 辩论引擎 (`backend/debate/`)
- orchestrator.py — 多轮编排
- prompts.py — 5 个 Prompt 模板
- consensus.py — 关键词共识判定

### 文件解析 (`backend/parsers/`)
- pdf_parser.py — PyMuPDF
- code_parser.py — AST 摘要
- text_parser.py — UTF-8 文本

### 前端 (`frontend/index.html`)
- 单 HTML 完整 SPA
- Alpine.js + Tailwind CSS 暗色主题
- PDF.js 浏览器端 PDF 解析
- marked.js + highlight.js 渲染
- SSE 流式辩论可视化（左右分栏）
- 配置持久化到 localStorage

---

## 🔜 后续开发计划

### Phase 3 — 平台化
- [ ] 预设辩论模板（论文审稿 / 代码 review / 方案对比）
- [ ] 辩论质量评分
- [ ] 辩论历史云端同步
- [ ] Docker 化部署
- [ ] API 限流与鉴权
