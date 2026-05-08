# 🥊 DebateAI

**双模型对抗辩论平台** — 让两个 AI 围绕你的论文/代码互相挑刺，最终达成共识。

## 🎯 为什么需要这个？

单一 LLM 有盲点。但让两个不同模型辩论——一个提建议，一个找漏洞——输出质量会显著提升。

> 这不是假设。这是经过实践验证的方法。

## ✨ 功能

- 📄 上传 PDF 论文、Python 代码、纯文本
- 🤖 两个 AI 实时辩论，左右分栏可视化
- 🤝 自动检测共识，输出最终结论
- ⚙️ 支持任意 OpenAI 兼容 API（OpenAI / DeepSeek / Gemini / 本地模型）

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入两个 LLM 的 API Key

# 3. 启动
python backend/main.py

# 4. 打开浏览器
# http://localhost:8000
```

## 📐 架构

```
用户上传材料
    ↓
┌──────────────────┐
│   File Parser    │  PDF / Code / Text
└──────────────────┘
    ↓
┌──────────────────┐
│ Debate Engine    │  编排多轮辩论
└──────────────────┘
    ↕         ↕
Agent A     Agent B   ← 两个不同 LLM
    ↓
┌──────────────────┐
│ Consensus Judge  │  提炼共识
└──────────────────┘
    ↓
最终结论 + 改进代码
```

## ⚙️ 配置

通过 `.env` 文件配置两个 LLM：

```env
LLM_A_BASE_URL=https://api.openai.com/v1
LLM_A_API_KEY=sk-xxx
LLM_A_MODEL=gpt-4o

LLM_B_BASE_URL=https://api.deepseek.com/v1
LLM_B_API_KEY=sk-xxx
LLM_B_MODEL=deepseek-chat
```

支持任何 OpenAI 兼容 API。

## 📋 开发计划

- [x] 项目计划书
- [ ] MVP：核心辩论引擎 + Web UI
- [ ] 辩论历史导出
- [ ] 自定义 Agent 角色
- [ ] Docker 部署
- [ ] 更多文件格式支持

## License

MIT
