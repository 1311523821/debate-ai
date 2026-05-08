# 配置管理 — 从 .env 读取 LLM 和辩论参数
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    base_url: str = ""
    api_key: str = ""
    model: str = ""


@dataclass
class AppConfig:
    llm_a: LLMConfig = field(default_factory=LLMConfig)
    llm_b: LLMConfig = field(default_factory=LLMConfig)
    max_rounds: int = 6

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            llm_a=LLMConfig(
                base_url=os.getenv("LLM_A_BASE_URL", "https://api.openai.com/v1"),
                api_key=os.getenv("LLM_A_API_KEY", ""),
                model=os.getenv("LLM_A_MODEL", "gpt-4o"),
            ),
            llm_b=LLMConfig(
                base_url=os.getenv("LLM_B_BASE_URL", "https://api.openai.com/v1"),
                api_key=os.getenv("LLM_B_API_KEY", ""),
                model=os.getenv("LLM_B_MODEL", "gpt-4o"),
            ),
            max_rounds=int(os.getenv("MAX_ROUNDS", "6")),
        )


# 全局配置单例
config = AppConfig.from_env()
