"""AWS Lambda entrypoint for direct invoke and API Gateway HTTP API."""

from __future__ import annotations

import base64
import json
from typing import Any

from .tools import make_citation_pack, read_aws_doc, search_aws_docs

TOOLS = {
    "search_aws_docs": search_aws_docs,
    "read_aws_doc": read_aws_doc,
    "make_citation_pack": make_citation_pack,
}


def _run_tool(payload: dict[str, Any]) -> dict[str, Any]:
    tool_name = payload.get("tool")
    arguments = payload.get("arguments") or {}
    if tool_name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {tool_name}"}
    try:
        return {"ok": True, "result": TOOLS[tool_name](**arguments)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _http_response(status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            "access-control-allow-origin": "*",
            "access-control-allow-methods": "POST,OPTIONS",
            "access-control-allow-headers": "content-type,authorization,x-api-key",
        },
        "body": json.dumps(payload, ensure_ascii=False),
    }


def _parse_http_body(event: dict[str, Any]) -> dict[str, Any]:
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    if isinstance(body, dict):
        return body
    return json.loads(body)


def handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    if "requestContext" not in event:
        return _run_tool(event)

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", event.get("httpMethod", ""))
    )
    if method == "OPTIONS":
        return _http_response(204, {"ok": True})
    if method and method != "POST":
        return _http_response(405, {"ok": False, "error": "Method not allowed"})

    try:
        payload = _parse_http_body(event)
    except Exception as exc:
        return _http_response(400, {"ok": False, "error": f"Invalid JSON body: {exc}"})

    result = _run_tool(payload)
    return _http_response(200 if result.get("ok") else 400, result)
