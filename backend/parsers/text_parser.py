# 纯文本解析器 — 读取文本文件内容


async def parse_text(file_bytes: bytes) -> str:
    """解析纯文本文件，返回内容。"""
    return file_bytes.decode("utf-8", errors="replace")
