# 统一 LLM 客户端 — 使用 httpx 异步调用 OpenAI 兼容 API
from typing import AsyncGenerator
import httpx
from backend.config import LLMConfig


class LLMClient:
    def __init__(self, cfg: LLMConfig):
        self.base_url = cfg.base_url.rstrip("/")
        self.api_key = cfg.api_key
        self.model = cfg.model
        self._client = httpx.AsyncClient(timeout=120.0)

    async def chat(
        self, messages: list[dict], stream: bool = True
    ) -> AsyncGenerator[str, None]:
        """调用 LLM，流式返回 token。"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": 0.7,
        }

        if stream:
            async with self._client.stream(
                "POST", url, json=payload, headers=headers
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        chunk = __import__("json").loads(data)
                        delta = chunk["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except (ValueError, KeyError, IndexError):
                        continue
        else:
            resp = await self._client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            yield content

    async def close(self):
        await self._client.aclose()
