"""Minimal handler shim for hosted agent runtimes."""

from __future__ import annotations

from typing import Any

from aws_doc_research_agent.tools import make_citation_pack, read_aws_doc, search_aws_docs

TOOLS = {
    "search_aws_docs": search_aws_docs,
    "read_aws_doc": read_aws_doc,
    "make_citation_pack": make_citation_pack,
}


def handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    tool_name = event.get("tool")
    arguments = event.get("arguments") or {}
    if tool_name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {tool_name}"}
    try:
        return {"ok": True, "result": TOOLS[tool_name](**arguments)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

