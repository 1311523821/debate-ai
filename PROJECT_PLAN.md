# DebateAI — 双模型对抗辩论平台

> 两个 AI 围绕你的论文/代码展开辩论，互相挑刺、互相改进，最终达成共识。

## 项目背景

在科研和工程实践中，单一 LLM 的输出往往存在盲点。通过让两个不同模型（如 Gemini 和 DeepSeek）进行结构化对抗辩论，可以：
- 暴露单一模型的思维盲区
- 通过互相纠错提升输出质量
- 最终收敛到双方都认可的高质量结论

本项目将这一流程产品化为一个可视化 Web 应用。

## 技术架构（纯前端）

```
┌─────────────────────────────────────────────┐
│            Browser (纯前端 SPA)             │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  HTML + Tailwind CSS + Alpine.js    │    │
│  │  PDF.js (文件解析)                   │    │
│  │  marked.js + highlight.js (渲染)    │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌──────────────┬──────────────────────┐    │
│  │  Agent A 面板 │  Agent B 面板        │    │
│  │  (左侧/蓝色) │  (右侧/红色)         │    │
│  └──────────────┴──────────────────────┘    │
│  ┌──────────────────────────────────────┐   │
│  │  共识结论 + 代码输出区                │   │
│  └──────────────────────────────────────┘   │
│                                             │
│         fetch + SSE (流式请求)               │
└─────────────────────┬───────────────────────┘
                      │ 直接调用
                      ▼
          任意 OpenAI 兼容 API
       (OpenAI / DeepSeek / Gemini / 本地模型)
```

**关键设计决策：纯前端，零后端。**

- 文件解析在浏览器完成（PDF.js + FileReader）
- LLM 调用直接从浏览器发起（fetch + SSE 流式解析）
- 配置存储在 localStorage
- 部署：GitHub Pages 自动部署，单 HTML 文件

## 核心功能

### 1. 材料上传
- 支持 PDF（论文）、Python 代码（.py）、纯文本
- 浏览器端解析，无需上传到服务器

### 2. 双 Agent 辩论
- 左右分栏实时展示两个 Agent 的对话
- Agent A（建议者）：分析材料，提出改进建议
- Agent B（批评者）：审查建议，指出漏洞，提出替代方案
- 多轮交替辩论，SSE 流式输出

### 3. 共识判定
- 当双方不再有实质性分歧时，自动结束辩论
- 提炼最终共识结论
- 如涉及代码，输出合并后的改进代码

### 4. 可配置性
- 支持选择不同的 LLM provider（OpenAI / DeepSeek / Gemini / 本地模型等）
- 可调节辩论轮次上限（默认 6 轮）
- 配置自动持久化到 localStorage

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 框架 | Alpine.js | 轻量响应式，零构建 |
| 样式 | Tailwind CSS (CDN) | 原子化 CSS，暗色主题 |
| 文件解析 | PDF.js | 浏览器端 PDF 文本提取 |
| Markdown | marked.js | Markdown → HTML |
| 代码高亮 | highlight.js | 语法高亮 |
| LLM 调用 | fetch + SSE | 浏览器原生流式请求 |
| 历史存储 | localStorage | 最近 50 条辩论记录 |
| 国际化 | 内置 i18n | 中英文切换 |
| 部署 | GitHub Pages | 自动部署，零运维 |

## 项目结构

```
debate-ai/
├── README.md                # 项目说明
├── PROJECT_PLAN.md          # 本文件
├── frontend/
│   └── index.html           # 完整单页应用（含所有 CSS/JS）
└── .github/
    └── workflows/
        └── deploy.yml       # GitHub Pages 自动部署
```

## 开发阶段

### Phase 1 — MVP（已完成）
- [x] 项目计划书
- [x] 前端：完整单页应用（文件上传 + 配置 + 辩论 UI + 共识展示）
- [x] 浏览器端 PDF 解析
- [x] SSE 流式 LLM 调用
- [x] GitHub Pages 自动部署

### Phase 2 — 增强
- [x] 辩论历史记录 / 导出（localStorage + Markdown/JSON 导出）
- [x] Agent 角色自定义（prompt 编辑器，三个 Prompt 可编辑）
- [ ] 辩论质量评分
- [x] 多语言支持（中英文一键切换）

### Phase 3 — 平台化
- [ ] 预设辩论模板（论文审稿 / 代码 review / 方案对比）
- [ ] 支持更多文件格式（Word、Jupyter Notebook）
- [ ] 辩论历史云端同步

## 使用流程

1. 打开 `frontend/index.html` 或访问 GitHub Pages 地址
2. 配置两个 LLM 的 API Key、Base URL 和模型名
3. 上传材料（PDF / .py / 文本）
4. 点击「开始辩论」
5. 观察左右两个 Agent 实时辩论
6. 阅读底部共识结论和改进代码

## License

MIT
