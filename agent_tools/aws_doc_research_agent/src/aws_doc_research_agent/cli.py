"""Command-line interface for local testing."""

from __future__ import annotations

import argparse
import json
from typing import Any

from .tools import make_citation_pack, read_aws_doc, search_aws_docs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aws-doc-research")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=5)

    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("url")
    read_parser.add_argument("--max-chars", type=int, default=6000)
    read_parser.add_argument("--start-index", type=int, default=0)

    pack_parser = subparsers.add_parser("citation-pack")
    pack_parser.add_argument("topic")
    pack_parser.add_argument("--audience", default="cloud engineering students")
    pack_parser.add_argument("--limit", type=int, default=5)

    args = parser.parse_args(argv)
    if args.command == "search":
        payload: dict[str, Any] = search_aws_docs(args.query, limit=args.limit)
    elif args.command == "read":
        payload = read_aws_doc(args.url, max_chars=args.max_chars, start_index=args.start_index)
    else:
        payload = make_citation_pack(args.topic, audience=args.audience, limit=args.limit)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

