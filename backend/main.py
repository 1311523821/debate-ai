# FastAPI 入口 — 提供文件上传、辩论 API 和前端静态文件服务
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from backend.config import config
from backend.llm.client import LLMClient
from backend.debate.orchestrator import DebateOrchestrator
from backend.parsers.pdf_parser import parse_pdf
from backend.parsers.code_parser import parse_code
from backend.parsers.text_parser import parse_text

app = FastAPI(title="DebateAI", description="双模型对抗辩论平台")

# CORS — 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 支持的文件类型映射
PARSERS = {
    ".pdf": parse_pdf,
    ".py": parse_code,
    ".txt": parse_text,
    ".md": parse_text,
    ".csv": parse_text,
    ".json": parse_text,
}


@app.get("/")
async def serve_index():
    """返回前端页面。"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "DebateAI API is running. Frontend not found."}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件并解析内容。"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名为空")

    ext = os.path.splitext(file.filename)[1].lower()
    parser = PARSERS.get(ext)

    if not parser:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {ext}。支持: {', '.join(PARSERS.keys())}",
        )

    try:
        file_bytes = await file.read()
        content = await parser(file_bytes)
        return {
            "filename": file.filename,
            "type": ext,
            "content": content,
            "size": len(file_bytes),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件解析失败: {str(e)}")


@app.post("/api/debate")
async def start_debate(payload: dict):
    """
    启动辩论，通过 SSE 流式返回辩论过程。

    请求体: {"material": "待辩论的内容", "max_rounds": 6}
    """
    material = payload.get("material", "").strip()
    if not material:
        raise HTTPException(status_code=400, detail="material 不能为空")

    max_rounds = payload.get("max_rounds", config.max_rounds)

    client_a = LLMClient(config.llm_a)
    client_b = LLMClient(config.llm_b)
    orchestrator = DebateOrchestrator(client_a, client_b, material, max_rounds)

    async def event_generator():
        try:
            async for event in orchestrator.run():
                yield {"event": event["type"], "data": event}
        except Exception as e:
            yield {"event": "error", "data": {"type": "error", "content": str(e)}}
        finally:
            await client_a.close()
            await client_b.close()

    return EventSourceResponse(event_generator())


# 挂载前端静态文件（如果存在）
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
