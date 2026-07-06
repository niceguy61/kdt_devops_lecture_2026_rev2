"""Stable tool contract for AWS documentation lecture research."""

from __future__ import annotations

from typing import Any

from .aws_docs_client import AwsDocsClient
from .models import CitationSource


def search_aws_docs(
    query: str,
    limit: int = 10,
    product_types: list[str] | None = None,
    guide_types: list[str] | None = None,
    search_intent: str = "",
) -> dict[str, Any]:
    """Search AWS documentation and return normalized candidate sources."""
    client = AwsDocsClient()
    return client.search(
        query,
        limit=limit,
        product_types=product_types,
        guide_types=guide_types,
        search_intent=search_intent,
    )


def read_aws_doc(url: str, max_chars: int = 12000, start_index: int = 0) -> dict[str, Any]:
    """Read and compact an AWS documentation page."""
    client = AwsDocsClient()
    return client.read(url, max_chars=max_chars, start_index=start_index)


def make_citation_pack(
    topic: str,
    audience: str = "cloud engineering students",
    limit: int = 5,
) -> dict[str, Any]:
    """Build a lecture-ready evidence pack from AWS documentation."""
    search_intent = (
        f"Find authoritative AWS documentation for a lecture about {topic} "
        f"for {audience}. Prefer conceptual, getting started, security, and "
        "implementation guidance pages."
    )
    search = search_aws_docs(topic, limit=limit, search_intent=search_intent)
    sources = [
        CitationSource(
            title=result["title"],
            url=result["url"],
            context=result.get("context"),
            usable_for=_infer_usable_for(result),
            confidence=max(0.25, 1.0 - ((result["rank"] - 1) * 0.12)),
        ).to_dict()
        for result in search["results"]
        if result.get("url")
    ]
    return {
        "topic": topic,
        "audience": audience,
        "summary": f"Candidate AWS documentation sources for lecture topic: {topic}",
        "sources": sources,
        "teaching_angles": _teaching_angles(topic, sources),
        "risks": [
            "Verify service availability and feature status before publishing.",
            "Use document URLs as citations in slides and lab guides.",
            "For hands-on labs, validate console and CLI behavior in the target region.",
        ],
        "search_query_id": search.get("query_id", ""),
    }


def _infer_usable_for(result: dict[str, Any]) -> list[str]:
    title = (result.get("title") or "").lower()
    context = (result.get("context") or "").lower()
    combined = f"{title} {context}"
    usable = ["concept"]
    if any(term in combined for term in ["getting started", "tutorial", "create", "configure"]):
        usable.append("lab")
    if any(term in combined for term in ["security", "iam", "policy", "permission"]):
        usable.append("security note")
    if any(term in combined for term in ["pricing", "quota", "limit"]):
        usable.append("operations note")
    if result.get("recommended_sections"):
        usable.append("targeted reading")
    return usable


def _teaching_angles(topic: str, sources: list[dict[str, Any]]) -> list[str]:
    angles = [
        f"Define the operational problem that makes {topic} useful.",
        "Separate core concept, AWS implementation detail, and lab validation step.",
    ]
    if any("security note" in source["usable_for"] for source in sources):
        angles.append("Call out identity, permission, and least-privilege implications.")
    if any("lab" in source["usable_for"] for source in sources):
        angles.append("Turn the most procedural source into a guided student lab.")
    return angles

