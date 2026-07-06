"""Data models for AWS documentation research results."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AwsDocSearchResult:
    rank: int
    title: str
    url: str
    context: str | None = None
    sections: list[str] = field(default_factory=list)
    recommended_sections: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CitationSource:
    title: str
    url: str
    context: str | None
    usable_for: list[str]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

