# DebateAI 开发总结

> **最后更新**: 2026-05-08  
> **当前分支**: main  
> **最新 commit**: `3b7dbde` — feat: 添加完整后端代码

---

## 📊 项目进度总览

| 模块 | 状态 | 说明 |
|------|------|------|
| 后端核心框架 | ✅ 完成 | FastAPI + SSE 流式输出 |
| LLM 客户端 | ✅ 完成 | httpx 异步，支持流式 |
| 辩论编排器 | ✅ 完成 | 多轮对话 + 共识判定 |
| Prompt 模板 | ✅ 完成 | 中文结构化 Prompt |
| 文件解析器 | ✅ 完成 | PDF / Python / 纯文本 |
| 配置管理 | ✅ 完成 | .env 双 LLM 配置 |
| 前端页面 | ⬜ 待开发 | 需要完整的 UI |
| 集成测试 | ⬜ 待开发 | 端到端测试 |
| 部署配置 | ⬜ 待开发 | Docker / 生产环境 |

---

## ✅ 已完成内容

### 后端 API (`backend/main.py`)
- `POST /api/upload` — 文件上传，支持 `.pdf .py .txt .md .csv .json`
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

---

## 🔜 后续开发计划

### Phase 1: 前端 UI（优先级最高）
**目标**: 用户可上传文件、观看辩论、查看共识结果

需要实现：
1. **文件上传区** — 拖拽上传 + 文件类型识别
2. **辩论展示区** — SSE 实时渲染 Agent A/B 的对话气泡
3. **共识展示区** — Markdown 渲染最终结论
4. **配置面板** — 可选：调整轮次、选择模型

技术选型建议：
- 纯 HTML + CSS + JS（无框架，轻量）
- 或 Vue 3 单文件（如果需要复杂交互）
- 使用 `EventSource` API 接收 SSE
- Markdown 渲染用 `marked.js`

### Phase 2: 功能增强
- [ ] 支持更多文件格式（Word、Jupyter Notebook）
- [ ] 辩论历史保存 / 回放
- [ ] 多语言支持（英文 Prompt 切换）
- [ ] Agent 角色自定义（用户可指定 Agent 的专业领域）

### Phase 3: 部署与优化
- [ ] Docker 化（Dockerfile + docker-compose）
- [ ] 生产环境配置（Gunicorn + Uvicorn workers）
- [ ] API 限流与鉴权
- [ ] 日志与监控

---

## 🏗️ 技术架构

```
用户浏览器
    │
    ▼
┌─────────────────────────┐
│   FastAPI (main.py)     │
│   ├─ /api/upload        │  ← 文件上传
│   ├─ /api/debate (SSE)  │  ← 流式辩论
│   └─ / (静态文件)        │  ← 前端
└─────────┬───────────────┘
          │
    ┌─────┴─────┐
    ▼           ▼
┌────────┐ ┌────────┐
│ LLM A  │ │ LLM B  │  ← 两个独立 LLM 实例
│(建议者) │ │(批评者) │
└────────┘ └────────┘
    │           │
    └─────┬─────┘
          ▼
  ┌──────────────┐
  │  Orchestrator │  ← 辩论编排
  │  + Consensus  │  ← 共识判定
  └──────────────┘
```

---

## ⚙️ 启动方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 LLM API Key

# 3. 启动
cd debate-ai
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📝 开发注意事项

1. **两个 LLM 可以是同一个**：`LLM_A_*` 和 `LLM_B_*` 可以指向同一个 API，只是角色不同
2. **SSE 格式**：事件类型为 `message`（辩论消息）和 `consensus`（共识结论）
3. **共识判定逻辑**：当前是基于关键词的简单策略，后续可改为 LLM 自判断
4. **import 路径**：所有 import 使用 `backend.xxx` 绝对路径，确保从项目根目录运行
