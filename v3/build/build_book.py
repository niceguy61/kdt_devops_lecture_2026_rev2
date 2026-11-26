"""Markdown 원고 → PDF 이북.

사용법: python3 build/build_book.py week1 [--days day1 day2] [--out ../downloads/pdf/...pdf]  (기본: 저장소/downloads/pdf/)
"""
from __future__ import annotations
import argparse, re, html
from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXT = ["tables", "fenced_code", "admonition", "attr_list", "md_in_html", "pymdownx.details", "pymdownx.highlight", "pymdownx.superfences", "sane_lists"]

WEEK_TITLES = {1: ("클라우드·컴퓨팅 기초 이론", "서버, 네트워크, 클라우드, 그리고 DevOps — 앞으로 5주를 읽기 위한 지도"),
               2: ("Docker + Git 첫 실습", "내 노트북에 개발 환경을 만들고, 앱 하나를 컨테이너로 포장해 실행하기까지"), 3: ("MSA + Kubernetes 입문", "여러 서비스로 나뉜 앱을 실행하고, 자동으로 검증하고, Kubernetes 위에 올리기까지"),
               4: ("Kubernetes 운영", "Helm으로 설치하고, 표준 입구로 들이고, 지켜보고, Git으로 맞추고, 그물로 잇고, 지키기까지"), 5: ("AWS + Terraform + EKS", "내 계정을 지키고, 네트워크를 그리고, 클릭을 코드로 바꾸고, 클라우드에 클러스터를 세웠다가 깨끗이 지우기까지")}


def front(text: str):
    meta = {}
    if text.startswith("---"):
        _, fm, text = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text


def md(text: str) -> str:
    html = markdown.markdown(text, extensions=EXT, extension_configs={"pymdownx.highlight": {"use_pygments": False}})
    # 22줄이 넘는 긴 코드 블록은 쪽을 넘어가도 되게 한다 (빈 쪽 방지)
    def _long(m):
        return m.group(0).replace("<pre", '<pre class="long"', 1) if m.group(0).count("\n") > 22 else m.group(0)
    return re.sub(r"<pre[\s>].*?</pre>", _long, html, flags=re.S)


def figures(h: str, base: Path, prefix: str, counter: list) -> str:
    def rep(m):
        alt, src = html.unescape(m.group(1)), m.group(2)
        counter[0] += 1
        p = (base / src).resolve()
        title = alt.split(" — ")[0]
        cap = f"<b>그림 {prefix}-{counter[0]}</b> &nbsp;{html.escape(title)}"
        return f'<figure><img src="{p.as_uri()}" alt="{html.escape(alt)}"><figcaption>{cap}</figcaption></figure>'
    return re.sub(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>', rep, h)


def lesson_html(path: Path, prefix: str, idx: int, counter: list) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    _, text = front(text)
    h = md(text)
    h = figures(h, path.parent, prefix, counter)
    # "# 1교시 · 제목" → 번호 분리
    m = re.search(r"<h1>(.*?)</h1>", h)
    title = m.group(1) if m else path.stem
    num, sep, name = title.partition(" · ")
    if sep:
        h = h.replace(m.group(0), f'<div class="runhead">{num} · {name}</div><h1 id="L{prefix}-{idx}"><span class="num">{num}</span>{name}</h1>', 1)
        title = f"{num} · {name}"
    h = h.replace('<details class="answer">', '<details class="answer" open>')
    return f'<section class="lesson">{h}</section>', title


def day_opener(path: Path, week: int, day: int) -> tuple[str, dict]:
    meta, text = front(path.read_text(encoding="utf-8"))
    text = re.sub(r"^# .*\n", "", text.strip() + "\n", count=1)
    text = re.sub(r"## 교시별 자료[\s\S]*$", "", text)   # 목차는 별도 페이지에서
    h = md(text)
    return (f'<section class="opener"><span class="daytag">WEEK {week} · DAY {day}</span>'
            f'<h1>{html.escape(meta.get("title", ""))}</h1><div class="subtitle">{html.escape(meta.get("subtitle", ""))}</div>{h}</section>'), meta


def build_appendix(out: Path):
    body, toc = [], []
    for i, f in enumerate(sorted((SRC / "appendix").glob("*.md")), 1):
        sec, title = lesson_html(f, "A", i, [0])
        body.append(sec.replace('<span class="num">', '<span class="num">', 1))
        toc.append(f'<a href="#LA-{i}">{html.escape(title)}</a>')
    cover = """<section class="cover"><div class="series">CLOUD NATIVE DEVOPS · 기초 이론 과정</div>
      <h1>부록<br>도구 설치 가이드</h1><div class="lead">Windows(PowerShell · WSL) · macOS · 직접 다운로드 — 5주 동안 쓰는 도구를 한곳에</div>
      <div class="band"><span>5주 · 200시간 과정 교재</span><span>v3 · appendix</span></div></section>"""
    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>부록 · 도구 설치 가이드</title></head><body>
      {cover}<section class="toc"><h2>차례</h2>{''.join(toc)}</section>{''.join(body)}</body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=doc, base_url=str(ROOT)).write_pdf(out, stylesheets=[str(ROOT / "build" / "book.css")])
    print("PDF:", out)


def build(week: str, days: list[str] | None, out: Path):
    if week == "appendix":
        return build_appendix(out)
    wdir = SRC / week
    wn = int(week.replace("week", ""))
    day_dirs = sorted(d for d in wdir.iterdir() if d.is_dir() and (not days or d.name in days))
    body, toc = [], []
    for d in day_dirs:
        dn = int(d.name.replace("day", ""))
        op, meta = day_opener(d / "README.md", wn, dn)
        body.append(op)
        toc.append(f'<div class="day">{dn}일차 · {html.escape(meta.get("title", ""))}</div>')
        counter = [0]
        for i, lf in enumerate(sorted(d.glob("lesson-*.md")), 1):
            sec, title = lesson_html(lf, f"{wn}-{dn}", i, counter)
            body.append(sec)
            toc.append(f'<a href="#L{wn}-{dn}-{i}">{html.escape(title)}</a>')
    wt, wl = WEEK_TITLES.get(wn, ("", ""))
    dots = "".join(f'<span class="{"on" if i < wn*5 and i >= (wn-1)*5 else ("or" if i == 24 else "")}"></span>' for i in range(25))
    cover = f'''<section class="cover"><div class="dots">{dots}</div>
      <div class="series">CLOUD NATIVE DEVOPS · 기초 이론 과정</div>
      <h1>{wn}주차<br>{html.escape(wt)}</h1><div class="lead">{html.escape(wl)}</div>
      <div class="band"><span>5주 · 200시간 과정 교재</span><span>v3 · {html.escape(", ".join(x.name for x in day_dirs))}</span></div></section>'''
    doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{wn}주차 {wt}</title></head><body>
      {cover}<section class="toc"><h2>차례</h2>{''.join(toc)}</section>{''.join(body)}</body></html>'''
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=doc, base_url=str(ROOT)).write_pdf(out, stylesheets=[str(ROOT / "build" / "book.css")])
    print("PDF:", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("week")
    ap.add_argument("--days", nargs="*")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = Path(a.out) if a.out else ROOT.parent / "downloads" / "pdf" / (f"{a.week}.pdf" if a.week != "appendix" else "appendix-install.pdf")
    build(a.week, a.days, out)
