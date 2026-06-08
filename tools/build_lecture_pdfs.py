#!/usr/bin/env python3
"""Build PDFs from exported lecture markdown sequentially."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PDF_OPTIONS = (
    '{"format":"A4","printBackground":true,'
    '"margin":{"top":"16mm","right":"14mm","bottom":"16mm","left":"14mm"}}'
)
LAUNCH_OPTIONS = '{"args":["--no-sandbox","--disable-setuid-sandbox"]}'


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="out_lecture_pdf_source")
    parser.add_argument("--out", default="out_lecture_pdf")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    source = Path(args.source)
    out = Path(args.out)
    if not source.exists():
        raise SystemExit(f"PDF source does not exist: {source}")

    markdown_files = sorted(source.rglob("*.md"))
    if args.limit:
        markdown_files = markdown_files[: args.limit]

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    failures: list[tuple[Path, str]] = []
    for index, md_file in enumerate(markdown_files, start=1):
        rel = md_file.relative_to(source)
        print(f"[{index}/{len(markdown_files)}] {rel}", flush=True)
        pdf_file = md_file.with_suffix(".pdf")
        if pdf_file.exists():
            pdf_file.unlink()

        result = run(
            [
                "npx",
                "-y",
                "md-to-pdf",
                str(md_file),
                "--basedir",
                ".",
                "--launch-options",
                LAUNCH_OPTIONS,
                "--pdf-options",
                PDF_OPTIONS,
            ]
        )
        if result.returncode != 0 or not pdf_file.exists():
            detail = (result.stderr or result.stdout).strip().splitlines()
            failures.append((rel, detail[-1] if detail else "unknown error"))
            continue

        target = out / rel.with_suffix(".pdf")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf_file, target)

    if failures:
        print("failed:")
        for rel, detail in failures:
            print(f"- {rel}: {detail}")
        return 1

    print(f"generated_pdfs={len(markdown_files)}")
    print(f"out={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
