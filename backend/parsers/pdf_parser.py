# PDF 解析器 — 使用 PyMuPDF 提取文本内容
import asyncio
import fitz  # PyMuPDF


async def parse_pdf(file_bytes: bytes) -> str:
    """异步解析 PDF 文件，提取全部文本内容。"""

    def _extract() -> str:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = []
        for i, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                pages.append(f"--- 第 {i + 1} 页 ---\n{text.strip()}")
        doc.close()
        if not pages:
            return "[PDF 解析结果为空，可能是扫描版 PDF]"
        return "\n\n".join(pages)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract)
