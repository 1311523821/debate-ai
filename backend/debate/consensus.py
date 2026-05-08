# 共识判定 — 分析辩论对话，判断是否达成共识
import re


def check_consensus(recent_messages: list[dict], window: int = 2) -> bool:
    """
    简单共识判定策略：
    连续 window 轮（默认2轮）对话中，如果 Agent B 没有提出新的反对意见，
    即视为达成共识。

    判定逻辑：检查最近 window 轮 Agent B 的消息，
    如果其中"不同意"、"问题"、"反对"等关键词数量递减或为零，则认为达成共识。
    """
    if len(recent_messages) < window * 2:
        return False

    # 取最近 window 轮 Agent B 的消息
    b_messages = [
        m for m in recent_messages[-window * 2 :] if m.get("agent") == "B"
    ]

    if len(b_messages) < window:
        return False

    objection_keywords = [
        "不同意", "反对", "问题", "漏洞", "错误", "不足", "质疑",
        "需要改进", "仍然", "依然", "尚未解决", "不充分",
    ]

    objection_scores = []
    for msg in b_messages:
        content = msg.get("content", "")
        score = sum(1 for kw in objection_keywords if kw in content)
        objection_scores.append(score)

    # 如果最近 window 轮的反对分数都很低（<=1），视为达成共识
    return all(score <= 1 for score in objection_scores[-window:])
