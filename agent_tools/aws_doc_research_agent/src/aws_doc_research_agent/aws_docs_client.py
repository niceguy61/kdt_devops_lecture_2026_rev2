"""Small AWS documentation client used by local and deployed tools."""

from __future__ import annotations

import html
import json
import re
import uuid
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import AwsDocSearchResult

SEARCH_API_URL = "https://proxy.search.docs.aws.com/search"
DEFAULT_USER_AGENT = "paperclip-aws-doc-research-agent/0.1"
SESSION_ID = str(uuid.uuid4())


class AwsDocsClientError(RuntimeError):
    """Raised when AWS documentation retrieval fails."""


class _ReadableHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._chunks: list[str] = []
        self._href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if tag in {"h1", "h2", "h3", "h4"}:
            self._chunks.append("\n\n")
        elif tag in {"p", "li", "tr", "pre", "code"}:
            self._chunks.append("\n")
        elif tag == "a":
            self._href = dict(attrs).get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "a":
            self._href = None
        if tag in {"h1", "h2", "h3", "h4", "p", "li", "tr", "pre"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = html.unescape(data).strip()
        if not text:
            return
        if self._href and self._href.startswith("http"):
            self._chunks.append(f"{text} ({self._href}) ")
        else:
            self._chunks.append(text + " ")

    def readable_text(self) -> str:
        text = "".join(self._chunks)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


class AwsDocsClient:
    def __init__(self, user_agent: str = DEFAULT_USER_AGENT, timeout: int = 30) -> None:
        self.user_agent = user_agent
        self.timeout = timeout

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        product_types: list[str] | None = None,
        guide_types: list[str] | None = None,
        search_intent: str = "",
    ) -> dict[str, Any]:
        request_body: dict[str, Any] = {
            "textQuery": {"input": query},
            "contextAttributes": [{"key": "domain", "value": "docs.aws.amazon.com"}],
            "acceptSuggestionBody": "RawText",
            "locales": ["en_us"],
        }
        for product in product_types or []:
            request_body["contextAttributes"].append(
                {"key": "aws-docs-search-product", "value": product}
            )
        for guide in guide_types or []:
            request_body["contextAttributes"].append(
                {"key": "aws-docs-search-guide", "value": guide}
            )

        params = {"session": SESSION_ID}
        if search_intent:
            params["searchIntent"] = search_intent[:512]
        raw = self._request_json(
            SEARCH_API_URL + "?" + urlencode(params),
            method="POST",
            body=request_body,
        )
        results = self._parse_search_results(raw, limit)
        return {
            "query": query,
            "query_id": raw.get("queryId", ""),
            "results": [result.to_dict() for result in results],
            "facets": self._parse_facets(raw.get("facets") or {}),
            "metadata": raw.get("metadata") or {},
        }

    def read(self, url: str, *, max_chars: int = 12000, start_index: int = 0) -> dict[str, Any]:
        self._validate_doc_url(url)
        html_text = self._request_text(url)
        parser = _ReadableHtmlParser()
        parser.feed(html_text)
        text = parser.readable_text()
        end_index = min(len(text), start_index + max_chars)
        return {
            "url": url,
            "start_index": start_index,
            "end_index": end_index,
            "total_chars": len(text),
            "truncated": end_index < len(text),
            "content": text[start_index:end_index],
        }

    def _request_json(self, url: str, *, method: str, body: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(body).encode("utf-8")
        request = Request(
            url,
            method=method,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-MCP-Session-Id": SESSION_ID,
            },
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise AwsDocsClientError(f"AWS docs search failed: {exc}") from exc

    def _request_text(self, url: str) -> str:
        request = Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            raise AwsDocsClientError(f"AWS docs read failed: {exc}") from exc

    @staticmethod
    def _validate_doc_url(url: str) -> None:
        if not re.match(r"^https://docs\.aws\.amazon\.com/.+\.html$", url):
            raise ValueError("URL must be an https://docs.aws.amazon.com/*.html page")

    @staticmethod
    def _parse_facets(raw_facets: dict[str, Any]) -> dict[str, Any]:
        facets: dict[str, Any] = {}
        if "aws-docs-search-product" in raw_facets:
            facets["product_types"] = raw_facets["aws-docs-search-product"]
        if "aws-docs-search-guide" in raw_facets:
            facets["guide_types"] = raw_facets["aws-docs-search-guide"]
        return facets

    @staticmethod
    def _parse_search_results(raw: dict[str, Any], limit: int) -> list[AwsDocSearchResult]:
        parsed: list[AwsDocSearchResult] = []
        for index, suggestion in enumerate(raw.get("suggestions", [])[:limit], start=1):
            text_suggestion = suggestion.get("textExcerptSuggestion")
            if not text_suggestion:
                continue
            metadata = dict(text_suggestion.get("metadata") or {})
            context = (
                metadata.get("seo_abstract")
                or text_suggestion.get("summary")
                or text_suggestion.get("suggestionBody")
            )
            parsed.append(
                AwsDocSearchResult(
                    rank=index,
                    title=text_suggestion.get("title", ""),
                    url=text_suggestion.get("link", ""),
                    context=context,
                    sections=_string_list(metadata.get("sections")),
                    recommended_sections=_string_list(metadata.get("recommended_sections")),
                )
            )
        return parsed


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]

