"""MCP server that proxies tool calls to the deployed AWS HTTP API."""

from __future__ import annotations

from typing import Any

from .remote_client import invoke_remote_agent


def search_aws_docs(
    query: str,
    limit: int = 10,
    product_types: list[str] | None = None,
    guide_types: list[str] | None = None,
    search_intent: str | None = None,
) -> dict[str, Any]:
    arguments = {
        "query": query,
        "limit": limit,
        "product_types": product_types,
        "guide_types": guide_types,
        "search_intent": search_intent,
    }
    return invoke_remote_agent("search_aws_docs", arguments)


def read_aws_doc(url: str, max_chars: int = 12000, start_index: int = 0) -> dict[str, Any]:
    return invoke_remote_agent(
        "read_aws_doc",
        {"url": url, "max_chars": max_chars, "start_index": start_index},
    )


def make_citation_pack(
    topic: str,
    audience: str = "cloud engineering students",
    limit: int = 5,
) -> dict[str, Any]:
    return invoke_remote_agent(
        "make_citation_pack",
        {"topic": topic, "audience": audience, "limit": limit},
    )


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("Install optional dependency with: pip install -e .[mcp]") from exc

    mcp = FastMCP(
        "paperclip.aws-doc-research-agent-remote",
        instructions=(
            "Proxy AWS documentation research requests to the deployed SAM HTTP API. "
            "Always return source URLs for citations."
        ),
    )

    mcp.tool()(search_aws_docs)
    mcp.tool()(read_aws_doc)
    mcp.tool()(make_citation_pack)
    mcp.run()


if __name__ == "__main__":
    main()
