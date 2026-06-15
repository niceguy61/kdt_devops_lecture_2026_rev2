#!/usr/bin/env python3
"""Export lecture markdown for external upload.

The export keeps source files untouched, mirrors markdown files into out_lecture,
rewrites local image references to GitHub raw URLs, and turns Mermaid fences into
PNG files that are linked from the exported markdown.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'][^>]*>)", re.IGNORECASE)
MERMAID_RE = re.compile(r"(^```mermaid[^\n]*\n)(.*?)(^```[ \t]*$)", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def run_checked(args: list[str], cwd: Path | None = None) -> None:
    result = run(args, cwd=cwd)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Command failed: {' '.join(args)}\n{detail}")


def git_value(args: list[str], default: str = "") -> str:
    result = run(["git", *args])
    if result.returncode != 0:
        return default
    return result.stdout.strip() or default


def raw_base(repo_root: Path, branch: str | None, remote: str | None) -> str:
    branch = branch or git_value(["branch", "--show-current"], "main")
    remote_url = remote or git_value(["remote", "get-url", "origin"])
    owner_repo = ""

    if remote_url.startswith("git@github.com:"):
        owner_repo = remote_url.removeprefix("git@github.com:")
    elif "github.com/" in remote_url:
        owner_repo = remote_url.split("github.com/", 1)[1]

    owner_repo = owner_repo.removesuffix(".git").strip("/")
    if not owner_repo or "/" not in owner_repo:
        raise SystemExit(f"Could not derive GitHub owner/repo from origin remote: {remote_url!r}")

    return f"https://raw.githubusercontent.com/{owner_repo}/{quote(branch, safe='')}/"


def is_external(url: str) -> bool:
    stripped = url.strip()
    return bool(
        re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", stripped)
        or stripped.startswith("#")
        or stripped.startswith("//")
    )


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def find_chrome(explicit: str | None = None) -> str:
    candidates = [explicit] if explicit else []
    candidates.extend(["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"])
    for candidate in candidates:
        if not candidate:
            continue
        resolved = shutil.which(candidate) if os.sep not in candidate else candidate
        if resolved and Path(resolved).exists():
            return resolved
    raise SystemExit("Chrome/Chromium was not found. Install Chrome or pass --chrome /path/to/chrome.")


def localize_pdf_target(target: str, markdown_file: Path, repo_root: Path, base: str) -> str:
    url, suffix = split_link_target(target)
    if url.startswith(base):
        rel = unquote(url.removeprefix(base))
        local = repo_root / rel
        if local.exists():
            return file_uri(local) + suffix
    if not is_external(url):
        local = (markdown_file.parent / url).resolve()
        if local.exists():
            return file_uri(local) + suffix
    return target


def inline_markdown(text: str, markdown_file: Path, repo_root: Path, base: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = escaped.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br>").replace("&lt;br /&gt;", "<br>")
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)

    def image_sub(match: re.Match[str]) -> str:
        alt, target = match.groups()
        src = html.escape(localize_pdf_target(target, markdown_file, repo_root, base), quote=True)
        return f'<img alt="{html.escape(alt, quote=True)}" src="{src}">'

    def link_sub(match: re.Match[str]) -> str:
        label, target = match.groups()
        href = html.escape(localize_pdf_target(target, markdown_file, repo_root, base), quote=True)
        return f'<a href="{href}">{label}</a>'

    escaped = IMAGE_RE.sub(image_sub, escaped)
    escaped = LINK_RE.sub(link_sub, escaped)
    return escaped


def table_html(lines: list[str], markdown_file: Path, repo_root: Path, base: str) -> str:
    rows = []
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        tag = "th" if index == 0 else "td"
        row = "".join(f"<{tag}>{inline_markdown(cell, markdown_file, repo_root, base)}</{tag}>" for cell in cells)
        rows.append(f"<tr>{row}</tr>")
    return "<table>" + "".join(rows) + "</table>"


def markdown_to_html(markdown_file: Path, repo_root: Path, base: str) -> str:
    lines = markdown_file.read_text(encoding="utf-8").splitlines()
    parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    blockquote: list[str] = []
    code_lines: list[str] = []
    in_code = False
    table_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            parts.append(f"<p>{inline_markdown(text, markdown_file, repo_root, base)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{inline_markdown(item, markdown_file, repo_root, base)}</li>" for item in list_items)
            parts.append(f"<ul>{items}</ul>")
            list_items.clear()

    def flush_quote() -> None:
        if blockquote:
            text = "<br>".join(inline_markdown(line, markdown_file, repo_root, base) for line in blockquote)
            parts.append(f"<blockquote>{text}</blockquote>")
            blockquote.clear()

    def flush_table() -> None:
        if table_lines:
            if len(table_lines) >= 2 and re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*", table_lines[1]):
                parts.append(table_html([table_lines[0], *table_lines[2:]], markdown_file, repo_root, base))
            else:
                flush_paragraph()
                paragraph.extend(table_lines)
            table_lines.clear()

    def flush_blocks() -> None:
        flush_table()
        flush_paragraph()
        flush_list()
        flush_quote()

    for line in lines:
        if line.startswith("```"):
            if in_code:
                parts.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_blocks()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_blocks()
            continue

        if line.lstrip().startswith("|") and "|" in line.strip()[1:]:
            flush_paragraph()
            flush_list()
            flush_quote()
            table_lines.append(line)
            continue

        flush_table()
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_blocks()
            level = len(heading.group(1))
            parts.append(f"<h{level}>{inline_markdown(heading.group(2), markdown_file, repo_root, base)}</h{level}>")
            continue

        list_match = re.match(r"^\s*[-*]\s+(.+)$", line)
        if list_match:
            flush_paragraph()
            flush_quote()
            list_items.append(list_match.group(1))
            continue

        quote_match = re.match(r"^\s*>\s?(.*)$", line)
        if quote_match:
            flush_paragraph()
            flush_list()
            blockquote.append(quote_match.group(1))
            continue

        flush_list()
        flush_quote()
        paragraph.append(line)

    flush_blocks()
    if in_code:
        parts.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")

    title = markdown_file.stem.replace("-", " ").title()
    body = "\n".join(parts)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
@page {{ size: A4; margin: 18mm 16mm; }}
body {{
  color: #111827;
  font-family: "Noto Sans CJK KR", "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.62;
}}
h1, h2, h3, h4 {{ line-height: 1.28; margin: 1.1em 0 0.45em; page-break-after: avoid; }}
h1 {{ font-size: 22pt; border-bottom: 2px solid #111827; padding-bottom: 0.25em; }}
h2 {{ font-size: 17pt; border-bottom: 1px solid #d1d5db; padding-bottom: 0.2em; }}
h3 {{ font-size: 13.5pt; }}
p, ul, table, blockquote, pre {{ margin: 0.7em 0; }}
ul {{ padding-left: 1.35em; }}
blockquote {{ border-left: 4px solid #9ca3af; color: #374151; padding-left: 0.9em; }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; page-break-inside: avoid; }}
th, td {{ border: 1px solid #d1d5db; padding: 5px 7px; vertical-align: top; }}
th {{ background: #f3f4f6; font-weight: 700; }}
pre {{ background: #f3f4f6; border: 1px solid #d1d5db; padding: 10px; white-space: pre-wrap; overflow-wrap: anywhere; }}
code {{ font-family: "D2Coding", "Consolas", monospace; font-size: 0.92em; }}
img {{ display: block; max-width: 100%; max-height: 210mm; margin: 0.8em auto; page-break-inside: avoid; }}
a {{ color: #1d4ed8; text-decoration: none; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def render_pdf(markdown_file: Path, output_file: Path, repo_root: Path, base: str, chrome: str) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lecture-pdf-") as tmp:
        html_file = Path(tmp) / "index.html"
        html_file.write_text(markdown_to_html(markdown_file, repo_root, base), encoding="utf-8")
        run_checked(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-breakpad",
                "--disable-crashpad",
                "--disable-crash-reporter",
                "--disable-dev-shm-usage",
                "--disable-features=Crashpad",
                "--noerrdialogs",
                "--allow-file-access-from-files",
                f"--user-data-dir={Path(tmp) / 'chrome-profile'}",
                f"--print-to-pdf={output_file}",
                str(html_file),
            ]
        )


def pdf_sources(out_root: Path) -> list[Path]:
    return sorted(path for path in out_root.rglob("*.md") if path.is_file())


def render_pdfs(markdown_files: list[Path], repo_root: Path, base: str, chrome: str) -> int:
    count = 0
    for markdown_file in markdown_files:
        render_pdf(markdown_file, markdown_file.with_suffix(".pdf"), repo_root, base, chrome)
        count += 1
    return count


def split_link_target(target: str) -> tuple[str, str]:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    match = re.match(r"([^ \t]+)(.*)$", target)
    if not match:
        return target, ""
    return match.group(1), match.group(2)


def raw_url_for_path(repo_root: Path, path: Path, base: str) -> str:
    rel = path.resolve().relative_to(repo_root.resolve()).as_posix()
    return base + quote(rel, safe="/-._~")


def rewrite_image_target(source_file: Path, repo_root: Path, out_file: Path, base: str, target: str, link_mode: str) -> str:
    url, suffix = split_link_target(target)
    if is_external(url):
        return target

    resolved = (source_file.parent / url).resolve()
    if link_mode == "relative":
        try:
            rel = os.path.relpath(resolved, out_file.parent.resolve())
            return Path(rel).as_posix() + suffix
        except ValueError:
            return target

    try:
        return raw_url_for_path(repo_root, resolved, base) + suffix
    except ValueError:
        return target


def rewrite_link_target(source_file: Path, repo_root: Path, out_file: Path, base: str, target: str, link_mode: str) -> str:
    url, suffix = split_link_target(target)
    if is_external(url):
        return target

    resolved = (source_file.parent / url).resolve()
    if not resolved.exists():
        return target

    if link_mode == "relative":
        try:
            rel = os.path.relpath(resolved, out_file.parent.resolve())
            return Path(rel).as_posix() + suffix
        except ValueError:
            return target

    try:
        return raw_url_for_path(repo_root, resolved, base) + suffix
    except ValueError:
        return target


def render_mermaid(mmdc: list[str], code: str, output: Path, theme: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lecture-mermaid-") as tmp:
        tmp_dir = Path(tmp)
        input_file = tmp_dir / "diagram.mmd"
        config_file = tmp_dir / "puppeteer.json"
        input_file.write_text(code.strip() + "\n", encoding="utf-8")
        config_file.write_text('{"args":["--no-sandbox","--disable-setuid-sandbox"]}\n', encoding="utf-8")
        cmd = [
            *mmdc,
            "-i",
            str(input_file),
            "-o",
            str(output),
            "-t",
            theme,
            "-b",
            "white",
            "-p",
            str(config_file),
        ]
        result = run(cmd)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"Mermaid render failed for {output}: {detail}")


def convert_markdown(
    source_file: Path,
    out_file: Path,
    repo_root: Path,
    out_root: Path,
    mermaid_root: Path,
    base: str,
    mmdc: list[str],
    render: bool,
    theme: str,
    link_mode: str,
) -> tuple[int, int]:
    text = source_file.read_text(encoding="utf-8")
    image_count = 0
    link_count = 0
    mermaid_count = 0

    def image_sub(match: re.Match[str]) -> str:
        nonlocal image_count
        alt, target = match.groups()
        rewritten = rewrite_image_target(source_file, repo_root, out_file, base, target, link_mode)
        if rewritten != target:
            image_count += 1
        return f"![{alt}]({rewritten})"

    def html_image_sub(match: re.Match[str]) -> str:
        nonlocal image_count
        prefix, target, suffix = match.groups()
        rewritten = rewrite_image_target(source_file, repo_root, out_file, base, target, link_mode)
        if rewritten != target:
            image_count += 1
        return f"{prefix}{html.escape(rewritten, quote=True)}{suffix}"

    def link_sub(match: re.Match[str]) -> str:
        nonlocal link_count
        label, target = match.groups()
        rewritten = rewrite_link_target(source_file, repo_root, out_file, base, target, link_mode)
        if rewritten != target:
            link_count += 1
        return f"[{label}]({rewritten})"

    text = IMAGE_RE.sub(image_sub, text)
    text = LINK_RE.sub(link_sub, text)
    text = HTML_IMG_RE.sub(html_image_sub, text)

    def mermaid_sub(match: re.Match[str]) -> str:
        nonlocal mermaid_count
        mermaid_count += 1
        rel_source = source_file.relative_to(repo_root)
        stem = rel_source.with_suffix("").as_posix().replace("/", "__")
        image_out = mermaid_root / f"{stem}--diagram-{mermaid_count:02d}.png"
        code = match.group(2)
        if render:
            render_mermaid(mmdc, code, image_out, theme)
        if link_mode == "raw":
            image_url = raw_url_for_path(repo_root, image_out, base)
        else:
            image_url = os.path.relpath(image_out, out_file.parent).replace(os.sep, "/")
        return f"![Mermaid diagram {mermaid_count}]({image_url})"

    text = MERMAID_RE.sub(mermaid_sub, text)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(text, encoding="utf-8")
    return image_count, mermaid_count


def markdown_sources(repo_root: Path, roots: list[str]) -> list[Path]:
    sources: list[Path] = []
    for root in roots:
        path = repo_root / root
        if path.is_file() and path.suffix == ".md":
            sources.append(path)
        elif path.is_dir():
            sources.extend(path.rglob("*.md"))
    return sorted(set(sources))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="out_lecture")
    parser.add_argument("--branch")
    parser.add_argument("--remote")
    parser.add_argument("--no-render-mermaid", action="store_true")
    parser.add_argument("--mmdc", default=os.environ.get("MMDC", "npx -y @mermaid-js/mermaid-cli"))
    parser.add_argument("--theme", default="default")
    parser.add_argument("--link-mode", choices=["raw", "relative"], default="raw")
    parser.add_argument("--pdf", action="store_true", help="Also generate a PDF next to every exported markdown file.")
    parser.add_argument("--pdf-only", action="store_true", help="Generate PDFs from the current --out directory without rebuilding markdown.")
    parser.add_argument("--chrome", help="Chrome/Chromium executable used for PDF generation.")
    parser.add_argument(
        "--mermaid-assets",
        default="lecture_mermaid_assets",
        help="Tracked output directory for rendered Mermaid PNGs when --link-mode=raw.",
    )
    parser.add_argument("roots", nargs="*", default=["week1", "week2", "week3", "week4", "week5"])
    args = parser.parse_args()

    repo_root = Path(git_value(["rev-parse", "--show-toplevel"], ".")).resolve()
    os.chdir(repo_root)
    out_root = (repo_root / args.out).resolve()
    mermaid_root = (repo_root / args.mermaid_assets).resolve()
    if args.link_mode == "relative":
        mermaid_root = out_root / "mermaid-assets"
    base = raw_base(repo_root, args.branch, args.remote)

    if args.pdf_only:
        if not out_root.exists():
            raise SystemExit(f"Output directory does not exist: {out_root}")
        markdown_files = pdf_sources(out_root)
        if not markdown_files:
            raise SystemExit(f"No markdown files found in {out_root}")
        chrome = find_chrome(args.chrome)
        pdf_count = render_pdfs(markdown_files, repo_root, base, chrome)
        print(f"exported_markdown=0")
        print(f"generated_pdfs={pdf_count}")
        try:
            out_label = out_root.relative_to(repo_root)
        except ValueError:
            out_label = out_root
        print(f"out={out_label}")
        return 0

    sources = markdown_sources(repo_root, args.roots)
    if not sources:
        raise SystemExit("No markdown files found.")

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)
    render = not args.no_render_mermaid
    if render and mermaid_root.exists():
        shutil.rmtree(mermaid_root)
    if render:
        mermaid_root.mkdir(parents=True, exist_ok=True)

    mmdc = args.mmdc.split()
    total_images = 0
    total_mermaid = 0

    for source in sources:
        rel = source.relative_to(repo_root)
        out_file = out_root / rel
        images, mermaids = convert_markdown(
            source,
            out_file,
            repo_root,
            out_root,
            mermaid_root,
            base,
            mmdc,
            render,
            args.theme,
            args.link_mode,
        )
        total_images += images
        total_mermaid += mermaids

    print(f"exported_markdown={len(sources)}")
    print(f"rewritten_images={total_images}")
    print(f"rendered_mermaid={total_mermaid if render else 0}")
    print(f"raw_base={base}")
    print(f"link_mode={args.link_mode}")
    if render:
        try:
            mermaid_label = mermaid_root.relative_to(repo_root)
        except ValueError:
            mermaid_label = mermaid_root
        print(f"mermaid_assets={mermaid_label}")
    if args.pdf:
        chrome = find_chrome(args.chrome)
        pdf_count = render_pdfs(pdf_sources(out_root), repo_root, base, chrome)
        print(f"generated_pdfs={pdf_count}")
    try:
        out_label = out_root.relative_to(repo_root)
    except ValueError:
        out_label = out_root
    print(f"out={out_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
