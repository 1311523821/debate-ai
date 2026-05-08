# 代码解析器 — 读取 Python 文件并用 AST 提取结构摘要
import ast
import asyncio


async def parse_code(file_bytes: bytes) -> str:
    """异步解析 Python 代码文件，提取源码和结构摘要。"""

    def _extract() -> str:
        source = file_bytes.decode("utf-8", errors="replace")
        parts = [source]

        try:
            tree = ast.parse(source)
            summary_lines = ["\n## 代码结构摘要\n"]

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [a.arg for a in node.args.args]
                    summary_lines.append(
                        f"- 函数 `{node.name}({', '.join(args)})` (第 {node.lineno} 行)"
                    )
                elif isinstance(node, ast.ClassDef):
                    bases = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                    base_str = f"({', '.join(bases)})" if bases else ""
                    methods = [
                        n.name
                        for n in ast.iter_child_nodes(node)
                        if isinstance(n, ast.FunctionDef)
                    ]
                    summary_lines.append(
                        f"- 类 `{node.name}{base_str}` (第 {node.lineno} 行)"
                    )
                    for method in methods:
                        summary_lines.append(f"  - 方法 `{method}`")

            if len(summary_lines) > 1:
                parts.append("\n".join(summary_lines))
        except SyntaxError:
            parts.append("\n## 代码结构摘要\n[语法错误，无法解析 AST]")

        return "\n".join(parts)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract)
