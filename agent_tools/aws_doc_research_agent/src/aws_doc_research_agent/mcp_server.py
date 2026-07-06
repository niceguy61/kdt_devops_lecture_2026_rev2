"""Optional MCP server wrapper for the stable AWS doc research tools."""

from __future__ import annotations

from .tools import make_citation_pack, read_aws_doc, search_aws_docs


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("Install optional dependency with: pip install -e .[mcp]") from exc

    mcp = FastMCP(
        "paperclip.aws-doc-research-agent",
        instructions=(
            "Search and read AWS documentation for lecture production. "
            "Always return source URLs for citations."
        ),
    )

    mcp.tool()(search_aws_docs)
    mcp.tool()(read_aws_doc)
    mcp.tool()(make_citation_pack)
    mcp.run()


if __name__ == "__main__":
    main()

