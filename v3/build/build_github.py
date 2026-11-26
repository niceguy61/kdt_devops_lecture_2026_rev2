"""원고 → GitHub용 Markdown (저장소 최상위에 출력).

사용법: python3 build/build_github.py week1      (주차 하나 + 목차 갱신)
        python3 build/build_github.py appendix   (부록 + 목차 갱신)
        python3 build/build_github.py index      (최상위 README만)
출력: <저장소>/README.md, weekN/README.md, weekN/dayM/*.md, appendix/*.md
그림은 v3/assets, 내려받기 파일은 downloads/{pdf,pptx}를 가리킨다.
"""
from __future__ import annotations
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # v3/
REPO = ROOT.parent                                   # 저장소 최상위
SRC = ROOT / "src"
RAW = "https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main"

ALERT = {"goal": "NOTE", "key": "IMPORTANT", "tip": "TIP", "warn": "WARNING", "diary": "NOTE"}
LABEL = {"lab": "🧪 실습:", "check": "🟢 확인:", "trouble": "🛠️ 막혔다면:", "cleanup": "🧹 정리:", "example": "📘", "analogy": "🧩", "myth": "❓", "term": "📖", "quiz": "✅", "academic": "🎓", "trend": "📈"}
WEEK_TITLES = {1: "클라우드·컴퓨팅 기초 이론", 2: "Docker + Git 첫 실습", 3: "MSA + Kubernetes 입문", 4: "Kubernetes 운영", 5: "AWS + Terraform + EKS"}
SEP = " &nbsp;|&nbsp; "


def convert(text: str) -> str:
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        q = re.match(r'^\?\?\? \w+(?: "(.*)")?\s*$', lines[i])
        if q:  # 맨 바깥의 접기 블록 → <details>
            body = []
            i += 1
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                body.append(lines[i][4:] if lines[i].startswith("    ") else "")
                i += 1
            while body and not body[-1].strip():
                body.pop()
            out += [f"<details><summary>{q.group(1) or '펼치기'}</summary>", ""] + body + ["", "</details>", ""]
            continue
        m = re.match(r'^!!! (\w+)(?: "(.*)")?\s*$', lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        kind, title = m.group(1), m.group(2) or ""
        body = []
        i += 1
        while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
            body.append(lines[i][4:] if lines[i].startswith("    ") else "")
            i += 1
        while body and not body[-1].strip():
            body.pop()
        btxt = "\n".join(body)
        btxt = re.sub(r'\?\?\? answer "(.*?)"\n((?:    .*\n?|\s*\n)+)',
                      lambda mm: f"<details><summary>{mm.group(1)}</summary>\n\n" + re.sub(r"^    ", "", mm.group(2), flags=re.M).rstrip() + "\n\n</details>\n", btxt + "\n")
        head = [f"> [!{ALERT[kind]}]", f"> **{title}**", ">"] if kind in ALERT else [f"> **{LABEL.get(kind, '')} {title}**", ">"]
        out += head + [("> " + l) if l.strip() else ">" for l in btxt.rstrip().splitlines()] + [""]
    return "\n".join(out) + "\n"


def front(text: str):
    meta = {}
    if text.startswith("---"):
        _, fm, text = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text.lstrip()


def h1(text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def weeks():
    return sorted(SRC.glob("week*"), key=lambda p: int(p.name[4:]))


def days(w: Path):
    return sorted(w.glob("day*"), key=lambda p: int(p.name[3:]))


def day_meta(d: Path):
    meta, _ = front((d / "README.md").read_text(encoding="utf-8"))
    lessons = [(f.name, h1(f.read_text(encoding="utf-8"))) for f in sorted(d.glob("lesson-*.md"))]
    return meta, lessons


def all_pages():
    """과정 전체를 읽는 순서대로: [(week, day, 원고 Path, 제목)]"""
    pages = []
    for w in weeks():
        for d in days(w):
            meta, lessons = day_meta(d)
            pages.append((w.name, d.name, d / "README.md", f"{w.name[4:]}주차 {d.name[3:]}일차 목차"))
            pages += [(w.name, d.name, d / n, t) for n, t in lessons]
    return pages


def rel(frm: Path, to: Path) -> str:
    return os.path.relpath(to, frm.parent).replace("\\", "/")


def out_path(week: str, day: str, f: Path) -> Path:
    return REPO / week / day / f.name


def downloads(week: str, day: str | None, me: Path) -> str:
    pdf = f"downloads/pdf/{week}.pdf"
    s = f"📕 {week[4:]}주차 이북 PDF: [보기]({rel(me, REPO / pdf)}) · [내려받기]({RAW}/{pdf})"
    if day:
        s += f"{SEP}📊 {day[3:]}일차 슬라이드: [PPTX 내려받기]({RAW}/downloads/pptx/{week}-{day}.pptx)"
    return s


def nav(pages, idx):
    week, day, f, _ = pages[idx]
    me = out_path(week, day, f)
    same = [p for p in pages if p[0] == week and p[1] == day and p[2].name != "README.md"]
    pos = next((i for i, p in enumerate(same, 1) if p[2] == f), 0)
    here = f" › {pos}/{len(same)}교시" if pos else ""
    crumbs = (f"<sub>[🏠 과정 목차]({rel(me, REPO / 'README.md')}) › [{week[4:]}주차]({rel(me, REPO / week / 'README.md')})"
              f" › [{day[3:]}일차]({rel(me, REPO / week / day / 'README.md')}){here}</sub>")
    prev = nxt = ""
    if idx > 0:
        pw, pd, pf, pt = pages[idx - 1]
        prev = f"⬅️ [{pt}]({rel(me, out_path(pw, pd, pf))})"
    if idx + 1 < len(pages):
        nw, nd, nf, nt = pages[idx + 1]
        nxt = f"[{nt}]({rel(me, out_path(nw, nd, nf))}) ➡️"
    mid = f"[⬆️ {day[3:]}일차 목차]({rel(me, REPO / week / day / 'README.md')})" if f.name != "README.md" else f"[⬆️ {week[4:]}주차 목차]({rel(me, REPO / week / 'README.md')})"
    bar = f"| 이전 | 목차 | 다음 |\n|:--|:--:|--:|\n| {prev} | {mid} | {nxt} |"
    return crumbs, bar


def build_week(week: str):
    pages = all_pages()
    for idx, (w, d, f, _) in enumerate(pages):
        if w != week:
            continue
        _, t = front(f.read_text(encoding="utf-8"))
        t = t.replace("../../../assets/", "../../v3/assets/")      # 그림은 v3/assets
        me = out_path(w, d, f)
        crumbs, bar = nav(pages, idx)
        if f.name == "README.md":
            t = re.sub(r"^(# .+\n)", lambda m: f'<img src="../../v3/assets/readme/{w}.png" alt="{w[4:]}주차 노선도" width="100%">\n\n' + m.group(1) + f"\n{downloads(w, d, me)}\n", t, count=1)
        me.parent.mkdir(parents=True, exist_ok=True)
        me.write_text(f"{crumbs}\n\n{convert(t).rstrip()}\n\n---\n\n{bar}\n", encoding="utf-8")
    build_week_index(week)
    print("GitHub md:", REPO / week)


def build_week_index(week: str):
    wn = int(week[4:])
    me = REPO / week / "README.md"
    L = ["[🏠 과정 목차](../README.md)", "", f'<img src="../v3/assets/readme/{week}.png" alt="{wn}주차 · {WEEK_TITLES.get(wn, "")}" width="100%">', "",
         f"# {wn}주차 · {WEEK_TITLES.get(wn, '')}", "", downloads(week, None, me), "", " ".join(shield(*b) for b in STACK.get(wn, [])), "",
         "| 일차 | 주제 | 교시 | 슬라이드 |", "|:--|:--|:--|:--|"]
    for d in days(SRC / week):
        meta, lessons = day_meta(d)
        ls = " ".join(f"[{h.split(' · ')[0].replace('교시', '')}]({d.name}/{n})" for n, h in lessons)
        L.append(f"| [**{d.name[3:]}일차**]({d.name}/README.md) | {meta.get('title', '')}<br><sub>{meta.get('subtitle', '')}</sub> | {ls} | [📊 PPTX]({RAW}/downloads/pptx/{week}-{d.name}.pptx) |")
    L += ["", "<sub>교시 칸의 숫자는 교시 번호입니다. 처음이라면 1일차 목차부터 열고, 각 페이지 맨 아래의 <b>다음 ➡️</b>를 따라가세요.</sub>", ""]
    me.parent.mkdir(exist_ok=True)
    me.write_text("\n".join(L), encoding="utf-8")


def build_appendix():
    dst = REPO / "appendix"
    dst.mkdir(exist_ok=True)
    pdf = "downloads/pdf/appendix-install.pdf"
    for f in sorted((SRC / "appendix").glob("*.md")):
        head = f"[🏠 과정 목차](../README.md)\n\n📕 PDF: [보기](../{pdf}) · [내려받기]({RAW}/{pdf})\n\n"
        (dst / f.name).write_text(head + convert(f.read_text(encoding="utf-8")), encoding="utf-8")
    print("GitHub md:", dst)


REPO_SLUG = "niceguy61/kdt_devops_lecture_2026_rev2"
STACK = {
    1: [("Linux", "FCC624", "linux", "000000"), ("Network", "475569", None, None), ("Cloud", "0089A0", None, None), ("Git", "F05032", "git", None)],
    2: [("Ubuntu_on_WSL2", "E95420", "ubuntu", None), ("Bash", "4EAA25", "gnubash", None), ("Git", "F05032", "git", None), ("GitHub", "181717", "github", None),
        ("Docker", "2496ED", "docker", None), ("Python", "3776AB", "python", None), ("Flask", "000000", "flask", None), ("PostgreSQL", "4169E1", "postgresql", None), ("Nginx", "009639", "nginx", None)],
    3: [("Docker_Compose", "2496ED", "docker", None), ("Redis", "DC382D", "redis", None), ("GitHub_Actions", "2088FF", "githubactions", None), ("GHCR", "181717", "github", None),
        ("Kubernetes", "326CE5", "kubernetes", None), ("kind", "326CE5", "kubernetes", None), ("Kustomize", "326CE5", None, None)],
    4: [("Helm", "0F1689", "helm", None), ("Envoy_Gateway", "AC6199", "envoyproxy", None), ("Prometheus", "E6522C", "prometheus", None), ("Grafana", "F46800", "grafana", None),
        ("OpenTelemetry", "425CC7", "opentelemetry", None), ("k6", "7D64FF", "k6", None), ("Argo_CD", "EF7B4D", "argo", None), ("Istio", "466BB0", "istio", None), ("Kyverno", "FF6F00", None, None)],
    5: [("AWS", "FF9900", None, None), ("IAM_·_VPC_·_EC2_·_S3", "232F3E", None, None), ("Terraform", "844FBA", "terraform", None), ("Amazon_EKS", "FF9900", None, None), ("GitHub_OIDC", "2088FF", "githubactions", None)],
}


def shield(label, color, logo=None, logo_color=None):
    from urllib.parse import quote
    lab = quote(label.replace("-", "--"))
    u = f"https://img.shields.io/badge/{lab}-{color}?style=flat-square"
    if logo:
        u += f"&logo={logo}&logoColor={logo_color or 'white'}"
    return f'<img src="{u}" alt="{label.replace("_", " ")}">'


def fact(label, msg, color):
    from urllib.parse import quote
    return f'<img src="https://img.shields.io/badge/{quote(label)}-{quote(msg)}-{color}?style=flat-square" alt="{label} {msg}">'


def build_index():
    ws = weeks()
    n_days = sum(len(days(w)) for w in ws)
    n_lessons = sum(len(day_meta(d)[1]) for w in ws for d in days(w))
    from urllib.parse import quote
    L = ['<p align="center"><img src="v3/assets/readme/hero.png" alt="앱 하나를 노트북에서 클라우드까지 — Cloud Native DevOps 기초 과정 5주 노선도" width="100%"></p>', "",
         '<p align="center">',
         "  " + fact("과정", "5주 · 200시간", "0F2A44"),
         "  " + fact("구성", f"{n_days}일 · {n_lessons}교시", "0089A0"),
         "  " + fact("이북", "PDF 6권", "C8651B"),
         "  " + fact("슬라이드", f"PPTX {n_days}개", "C8651B"),
         "  " + fact("실습 환경", "WSL2 · macOS", "475569"),
         f'  <img src="https://img.shields.io/github/last-commit/{REPO_SLUG}?style=flat-square&label={quote("업데이트")}&color=2E7D4F" alt="마지막 업데이트">',
         "</p>", "",
         '<p align="center">',
         '  <a href="week1/day1/README.md"><b>1주차 1일차부터 시작하기</b></a> &nbsp;·&nbsp;',
         '  <a href="appendix/install.md">도구 설치 가이드</a> &nbsp;·&nbsp;',
         '  <a href="#내려받기">PDF · PPTX 내려받기</a>',
         "</p>", "", "<br>", "",
         "## 이 과정에서 다루는 기술", "",
         "주차가 지날수록 DevMart가 올라가는 자리가 바뀌고, 쓰는 도구도 그 자리에 맞게 늘어납니다.", "",
         "| 주차 | 기술 |", "|:--|:--|"]
    for w in ws:
        wn = int(w.name[4:])
        L.append(f"| [**{wn}주차**]({w.name}/README.md)<br><sub>{WEEK_TITLES[wn]}</sub> | " + " ".join(shield(*b) for b in STACK.get(wn, [])) + " |")
    L += ["", "## 시작하기", "",
          "1. **[1주차 1일차](week1/day1/README.md)부터** 엽니다. 모든 페이지 맨 아래의 **다음 ➡️** 링크를 따라가면 교시 순서대로 이어집니다.",
          "2. 도구는 그 도구를 처음 쓰는 교시에서 설치합니다. Windows(PowerShell · WSL) · macOS별 방법을 모은 것은 [부록 A · 도구 설치 가이드](appendix/install.md)입니다.",
          "3. 3주차부터는 이 저장소의 실습 파일을 복사해 씁니다.", "",
          "```bash", "cd ~", f"git clone https://github.com/{REPO_SLUG}.git course", "ls ~/course/labs        # week2 … week5", "```", "",
          "## 내려받기", "",
          "| | 이북 PDF | 일차별 슬라이드 PPTX |", "|:--|:--|:--|"]
    for w in ws:
        wn = int(w.name[4:])
        pp = " ".join(f"[{d.name[3:]}일차]({RAW}/downloads/pptx/{w.name}-{d.name}.pptx)" for d in days(w))
        L.append(f"| **{wn}주차** {WEEK_TITLES[wn]} | 📕 [보기](downloads/pdf/{w.name}.pdf) · [받기]({RAW}/downloads/pdf/{w.name}.pdf) | 📊 {pp} |")
    L.append(f"| **부록 A** 도구 설치 가이드 | 📕 [보기](downloads/pdf/appendix-install.pdf) · [받기]({RAW}/downloads/pdf/appendix-install.pdf) | |")
    L += ["", "<sub>PDF의 <b>보기</b>는 GitHub에서 바로 열고, <b>받기</b>는 파일로 저장합니다. PPTX는 누르면 내려받습니다.</sub>", "", "## 과정 목차", ""]
    for w in ws:
        wn = int(w.name[4:])
        L += [f'<a href="{w.name}/README.md"><img src="v3/assets/readme/{w.name}.png" alt="{wn}주차 · {WEEK_TITLES[wn]}" width="100%"></a>', "",
              "| 일차 | 주제 | 교시 |", "|:--|:--|:--|"]
        for d in days(w):
            meta, lessons = day_meta(d)
            ls = " ".join(f"[{h.split(' · ')[0].replace('교시', '')}]({w.name}/{d.name}/{n})" for n, h in lessons)
            L.append(f"| [**{d.name[3:]}일차**]({w.name}/{d.name}/README.md) | {meta.get('title', '')} | {ls} |")
        L += ["", "<br>", ""]
    L += ["## 저장소 구성", "", "```",
          "README.md            지금 이 페이지 (과정 목차)",
          "week1/ … week5/      교재: 주차 목차 → 일차 목차 → 교시",
          "appendix/            부록 A · 도구 설치 가이드",
          "downloads/pdf/       주차별 이북 PDF",
          "downloads/pptx/      일차별 슬라이드",
          "labs/                실습 파일 (3주차부터 복사해서 사용)",
          "v3/                  원고와 빌드 도구 (강사용)",
          "archive/rev2/        이전 판 교재 (보관)",
          "```", ""]
    (REPO / "README.md").write_text("\n".join(L), encoding="utf-8")
    print("README:", REPO / "README.md")


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else "week1"
    if tgt == "appendix":
        build_appendix()
    elif tgt != "index":
        build_week(tgt)
    build_index()
