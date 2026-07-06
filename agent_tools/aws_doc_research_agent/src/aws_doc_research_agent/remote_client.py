"""Client for the deployed AWS doc research agent HTTP API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 45


class RemoteAgentError(RuntimeError):
    """Raised when the deployed agent returns an error response."""


def invoke_remote_agent(
    tool: str,
    arguments: dict[str, Any],
    *,
    endpoint_url: str | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    url = endpoint_url or os.environ.get("AWS_DOC_RESEARCH_AGENT_URL")
    if not url:
        raise RemoteAgentError("Set AWS_DOC_RESEARCH_AGENT_URL to the deployed /invoke endpoint.")

    payload = json.dumps({"tool": tool, "arguments": arguments}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"content-type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RemoteAgentError(f"HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RemoteAgentError(f"Could not reach remote agent: {exc}") from exc

    parsed = json.loads(body)
    if not parsed.get("ok"):
        raise RemoteAgentError(str(parsed.get("error", "Remote agent returned ok=false")))
    return parsed["result"]
