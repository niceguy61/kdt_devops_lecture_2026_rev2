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
from urllib.parse import quote


IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'][^>]*>)", re.IGNORECASE)
MERMAID_RE = re.compile(r"(^```mermaid[^\n]*\n)(.*?)(^```[ \t]*$)", re.MULTILINE | re.DOTALL)


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


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
    base: str,
    mmdc: list[str],
    render: bool,
    theme: str,
    link_mode: str,
) -> tuple[int, int]:
    text = source_file.read_text(encoding="utf-8")
    image_count = 0
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

    text = IMAGE_RE.sub(image_sub, text)
    text = HTML_IMG_RE.sub(html_image_sub, text)

    def mermaid_sub(match: re.Match[str]) -> str:
        nonlocal mermaid_count
        mermaid_count += 1
        rel_source = source_file.relative_to(repo_root)
        stem = rel_source.with_suffix("").as_posix().replace("/", "__")
        image_rel = Path("mermaid-assets") / f"{stem}--diagram-{mermaid_count:02d}.png"
        image_out = out_root / image_rel
        code = match.group(2)
        if render:
            render_mermaid(mmdc, code, image_out, theme)
        if link_mode == "relative":
            image_url = os.path.relpath(image_out, out_file.parent).replace(os.sep, "/")
        else:
            image_url = base + quote((out_root.name + "/" + image_rel.as_posix()), safe="/-._~")
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
    parser.add_argument("roots", nargs="*", default=["week1", "week2", "week3", "week4", "week5", "week6"])
    args = parser.parse_args()

    repo_root = Path(git_value(["rev-parse", "--show-toplevel"], ".")).resolve()
    os.chdir(repo_root)
    out_root = (repo_root / args.out).resolve()
    base = raw_base(repo_root, args.branch, args.remote)
    sources = markdown_sources(repo_root, args.roots)
    if not sources:
        raise SystemExit("No markdown files found.")

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)

    render = not args.no_render_mermaid
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
    try:
        out_label = out_root.relative_to(repo_root)
    except ValueError:
        out_label = out_root
    print(f"out={out_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
