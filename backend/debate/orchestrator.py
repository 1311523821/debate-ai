# 辩论编排器 — 核心逻辑，驱动两个 Agent 多轮辩论
from typing import AsyncGenerator
from backend.llm.client import LLMClient
from backend.debate.prompts import (
    AGENT_A_INITIAL,
    AGENT_B_REVIEW,
    AGENT_A_RESPOND,
    AGENT_B_RESPOND,
    CONSENSUS_PROMPT,
)
from backend.debate.consensus import check_consensus


class DebateOrchestrator:
    def __init__(
        self,
        client_a: LLMClient,
        client_b: LLMClient,
        material: str,
        max_rounds: int = 6,
    ):
        self.client_a = client_a
        self.client_b = client_b
        self.material = material
        self.max_rounds = max_rounds
        # 完整对话历史
        self.history: list[dict] = []

    async def _stream_agent(
        self, client: LLMClient, messages: list[dict]
    ) -> str:
        """调用 LLM 并收集完整输出。"""
        chunks = []
        async for token in client.chat(messages, stream=True):
            chunks.append(token)
        return "".join(chunks)

    async def run(self) -> AsyncGenerator[dict, None]:
        """执行多轮辩论，通过 yield 流式返回每条消息。"""

        # Round 1: Agent A 分析材料
        messages_a = [
            {"role": "system", "content": AGENT_A_INITIAL},
            {"role": "user", "content": f"以下是待分析的材料：\n\n{self.material}"},
        ]
        content_a = await self._stream_agent(self.client_a, messages_a)
        msg_a = {"type": "message", "agent": "A", "content": content_a, "round": 1}
        self.history.append(msg_a)
        yield msg_a

        # Round 1: Agent B 审查
        messages_b = [
            {"role": "system", "content": AGENT_B_REVIEW},
            {
                "role": "user",
                "content": f"原始材料：\n{self.material}\n\nAgent A 的分析：\n{content_a}",
            },
        ]
        content_b = await self._stream_agent(self.client_b, messages_b)
        msg_b = {"type": "message", "agent": "B", "content": content_b, "round": 1}
        self.history.append(msg_b)
        yield msg_b

        # 后续轮次
        for round_num in range(2, self.max_rounds + 1):
            # 检查是否达成共识
            if check_consensus(self.history):
                break

            # Agent A 回应
            history_text = self._format_history()
            messages_a = [
                {"role": "system", "content": AGENT_A_RESPOND},
                {
                    "role": "user",
                    "content": f"原始材料：\n{self.material}\n\n辩论历史：\n{history_text}",
                },
            ]
            content_a = await self._stream_agent(self.client_a, messages_a)
            msg_a = {
                "type": "message",
                "agent": "A",
                "content": content_a,
                "round": round_num,
            }
            self.history.append(msg_a)
            yield msg_a

            # 再次检查共识
            if check_consensus(self.history):
                break

            # Agent B 回应
            history_text = self._format_history()
            messages_b = [
                {"role": "system", "content": AGENT_B_RESPOND},
                {
                    "role": "user",
                    "content": f"原始材料：\n{self.material}\n\n辩论历史：\n{history_text}",
                },
            ]
            content_b = await self._stream_agent(self.client_b, messages_b)
            msg_b = {
                "type": "message",
                "agent": "B",
                "content": content_b,
                "round": round_num,
            }
            self.history.append(msg_b)
            yield msg_b

        # 生成共识结论
        history_text = self._format_history()
        consensus_messages = [
            {"role": "system", "content": "你是一位公正的总结者。"},
            {
                "role": "user",
                "content": CONSENSUS_PROMPT.format(debate_history=history_text),
            },
        ]
        consensus_content = await self._stream_agent(
            self.client_a, consensus_messages
        )
        yield {"type": "consensus", "content": consensus_content}

    def _format_history(self) -> str:
        """将对话历史格式化为文本。"""
        lines = []
        for msg in self.history:
            agent_name = "Agent A（建议者）" if msg["agent"] == "A" else "Agent B（批评者）"
            lines.append(f"### {agent_name} - 第{msg['round']}轮\n{msg['content']}\n")
        return "\n".join(lines)
