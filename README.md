# 🥊 DebateAI

**双模型对抗辩论平台** — 让两个 AI 围绕你的论文/代码互相挑刺，最终达成共识。

> 🚀 **纯前端应用**，无需后端服务器。直接打开 `index.html` 或部署到 GitHub Pages 即可使用。

## ✨ 功能

- 📄 上传 PDF 论文、Python 代码、纯文本
- 🤖 两个 AI 实时辩论，左右分栏可视化（流式输出）
- 🤝 自动检测共识，输出最终结论 + 改进代码
- ⚙️ 支持任意 OpenAI 兼容 API（OpenAI / DeepSeek / Gemini / 本地模型）
- 🌙 暗色主题，Markdown 渲染 + 代码高亮

## 🚀 使用方式

### 方式一：直接打开

```bash
# 克隆仓库
git clone https://github.com/your-username/debate-ai.git
cd debate-ai

# 直接在浏览器中打开
open frontend/index.html
# 或双击 frontend/index.html
```

### 方式二：GitHub Pages

1. Fork 本仓库
2. 进入仓库 Settings → Pages
3. Source 选择 "GitHub Actions"
4. 推送代码后自动部署到 `https://your-username.github.io/debate-ai/`

### 方式三：本地 HTTP 服务

```bash
cd frontend
python3 -m http.server 8080
# 打开 http://localhost:8080
```

## ⚙️ 配置

在页面上的「LLM 配置」区域填写两个 Agent 的 API 信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| Base URL | OpenAI 兼容 API 地址 | `https://api.openai.com/v1` |
| API Key | API 密钥 | `sk-xxx` |
| Model | 模型名称 | `gpt-4o` |

配置会自动保存到浏览器 localStorage，下次打开自动恢复。

## 🔒 安全提示

- **API Key 仅存储在浏览器本地**（localStorage），不会发送到任何第三方服务器
- 所有 LLM 调用直接从浏览器发起，不经中间服务器
- 请勿在公共设备上保存 API Key

## 📐 架构

```
浏览器（纯前端）
├── 文件解析（PDF.js / FileReader）
├── 辩论编排（多轮交替 + 共识检测）
├── LLM 调用（fetch + SSE 流式解析）
└── UI 渲染（Alpine.js + Tailwind + marked.js）
    ↓
任意 OpenAI 兼容 API
```

零后端，零构建，单 HTML 文件。

## 📋 开发计划

- [x] 核心辩论引擎 + Web UI
- [x] GitHub Pages 自动部署
- [ ] 辩论历史记录 / 导出
- [ ] Agent 角色自定义（prompt 编辑器）
- [ ] 更多文件格式支持（Word、Jupyter Notebook）
- [ ] 多语言支持

## License

MIT
