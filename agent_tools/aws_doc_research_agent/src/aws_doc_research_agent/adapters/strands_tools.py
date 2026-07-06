"""Strands-friendly wrappers around the stable tool contract.

Import these functions into a Strands agent and register/decorate them using the
tool API for the installed Strands SDK version.
"""

from __future__ import annotations

from typing import Any

from aws_doc_research_agent.tools import make_citation_pack, read_aws_doc, search_aws_docs


def aws_docs_search_tool(query: str, limit: int = 5) -> dict[str, Any]:
    return search_aws_docs(query=query, limit=limit)


def aws_docs_read_tool(url: str, max_chars: int = 6000) -> dict[str, Any]:
    return read_aws_doc(url=url, max_chars=max_chars)


def aws_citation_pack_tool(topic: str, audience: str = "cloud engineering students") -> dict[str, Any]:
    return make_citation_pack(topic=topic, audience=audience)

