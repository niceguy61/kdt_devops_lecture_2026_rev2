"""2주차 3일차 다이어그램. 실행: python3 diagrams/w2d3.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week2" / "day3"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def layer(text, sub, bg, fg="var(--navy)", w="100%", ro=True):
    lock = icon("Lock", 22, "slate", 2) if ro else icon("PenLine", 22, "orange", 2)
    return f'''<div style="width:{w};background:{bg};border-radius:10px;padding:12px 18px;display:flex;align-items:center;gap:12px;color:{fg}">
{lock}<div style="font-size:20px;font-weight:800;{MONO}">{text}</div><div class="grow"></div><div style="font-size:17px;color:var(--slate)">{sub}</div></div>'''


# 1. 레이어
img_layers = [("CMD / EXPOSE / ENV", "설정만 · 0B", "#E8EEF4"), ("COPY 설정 파일", "수 kB", "#D8F0F3"), ("RUN nginx 설치", "수십 MB", "#BFE6EC"), ("ADD alpine-minirootfs", "Alpine 기본 파일", "#A3DAE3")]
il = "".join(layer(t, s, b) for t, s, b in img_layers)
cont = "".join(f'<div class="col" style="gap:8px;flex:1">{layer("쓰기 가능한 층", n, "var(--orange-l)", ro=False)}</div>' for n in ["web", "web2", "web3"])
R("w2d3-layers", f'''<div class="row" style="gap:24px;align-items:stretch">
<div class="col grow" style="gap:10px">
 <div class="tag">컨테이너마다 — 얇은 쓰기 가능한 층 (Copy-on-Write, 지우면 사라짐)</div>
 <div class="row" style="gap:10px">{cont}</div>
 <div class="row c" style="gap:10px;justify-content:center">{icon("ArrowDown",28,"slate",2.5)}<span style="font-size:18px;color:var(--slate)">세 컨테이너가 아래 이미지 층을 함께 쓴다</span>{icon("ArrowDown",28,"slate",2.5)}</div>
 <div style="border:3px solid var(--teal);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:8px">
  <div class="row c" style="gap:10px">{icon("Layers",30,"teal",2)}<div style="font-size:21px;font-weight:900;color:var(--teal-d)">이미지 nginx:1.30-alpine — 읽기 전용 층</div></div>{il}
 </div></div>
<div class="col" style="width:330px;gap:14px;justify-content:center">
 <div class="card fill-teal" style="padding:18px"><h3 style="font-size:23px">공간 공유</h3><p style="font-size:18px">같은 층은 한 번만 저장</p></div>
 <div class="card fill-violet" style="padding:18px"><h3 style="font-size:23px">빠른 다운로드</h3><p style="font-size:18px">있는 층은 Already exists</p></div>
 <div class="card fill-orange" style="padding:18px"><h3 style="font-size:23px">빠른 빌드</h3><p style="font-size:18px">안 바뀐 층은 CACHED (5교시)</p></div>
</div></div>''')

# 2. Dockerfile 해부
lines = [("FROM python:3.14-slim", "베이스 층들", "teal", "Layers"), ("WORKDIR /app", "폴더 하나", "slate", "Folder"),
         ("RUN useradd … appuser", "사용자 생성", "slate", "UserPlus"), ("COPY requirements.txt .", "의존성 목록", "violet", "FileText"),
         ("RUN pip install …", "라이브러리 (가장 큼)", "violet", "Package"), ("COPY app.py .", "내 코드 (몇 kB)", "orange", "FileCode"),
         ("USER · ENV · EXPOSE · CMD", "설정 (0B)", "green", "Settings")]
lr = "".join(f'''<div class="row c" style="gap:14px"><div style="width:520px;background:#0F1E2E;color:#E2E8F0;border-radius:8px;padding:10px 16px;font-size:20px;{MONO}">{t}</div>
{icon("ArrowRight",28,"slate",2.5)}<div class="grow" style="background:var(--{c}-l);border-left:6px solid var(--{c});border-radius:8px;padding:10px 16px;display:flex;align-items:center;gap:10px">{icon(i,26,c,2)}<span style="font-size:20px;font-weight:700;color:var(--navy)">{d}</span></div></div>''' for t, d, c, i in lines)
R("w2d3-dockerfile-anatomy", f'''<div class="row c" style="gap:14px"><div class="tag" style="width:520px">DOCKERFILE (위에서 아래로)</div><div style="width:28px"></div><div class="tag grow">이미지의 층 (아래에서 위로 쌓인다)</div></div>
<div class="col" style="gap:8px">{lr}</div>
<div class="row" style="gap:14px"><div class="card fill-violet grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">RUN</b> = 빌드할 때 (밀키트 포장)</p></div>
<div class="card fill-green grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">CMD</b> = 실행할 때 (조리 방법) · PID 1</p></div>
<div class="card fill-slate grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">EXPOSE</b> = 안내문 · 포트를 열지 않는다</p></div></div>''')

# 3. 빌드 컨텍스트
files = [("app.py", "teal", True), ("requirements.txt", "teal", True), ("Dockerfile", "slate", True), (".env (비밀번호!)", "red", False), ("debug.log 100MB", "red", False), (".git/", "red", False)]
fl = "".join(f'<div class="row c" style="gap:10px;background:#fff;border:2px solid var(--{c});border-radius:10px;padding:8px 12px">{icon("File",24,c,2)}<span style="font-size:19px;{MONO};color:var(--navy)">{n}</span><div class="grow"></div>{icon("Check" if ok else "X",24,"green" if ok else "red",2.5)}</div>' for n, c, ok in files)
R("w2d3-build-context", f'''<div class="row" style="gap:18px;align-items:center">
<div class="card" style="width:400px;gap:8px"><div class="row c" style="gap:10px">{icon("FolderOpen",34,"navy",2)}<h3 style="font-size:23px">빌드 컨텍스트 ( . )</h3></div>{fl}</div>
<div class="col center" style="gap:8px">{arrow(size=40)}<div class="box" style="background:var(--orange);color:#fff;font-size:19px">.dockerignore<br>필터</div>{arrow(size=40)}</div>
<div class="card fill-teal center" style="width:300px;gap:10px">{ic("ChefHat","teal",80)}<h3 style="font-size:23px">Docker 엔진</h3><p style="font-size:18px">상자 안의 것만<br>COPY할 수 있다</p></div>
{arrow(size=40)}
<div class="card center grow" style="gap:10px;border-color:var(--green)">{ic("Layers","green",80)}<h3 style="font-size:23px">이미지</h3><p style="font-size:18px">app.py · requirements.txt만</p></div></div>
<div class="row" style="gap:14px"><div class="card fill-red grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">COPY . . + 필터 없음</b> → .env가 이미지에 → 받는 사람 누구나 읽는다</p></div>
<div class="card fill-orange grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">RUN rm .env</b>로는 안 지워진다 — 아래층에 남는다</p></div></div>''')

# 4. 캐시와 순서
def stack(title, items, col, note):
    out = []
    for t, state in items:
        bg = {"cached": "var(--green-l)", "rebuild": "var(--red-l)", "changed": "var(--orange-l)"}[state]
        tag = {"cached": "CACHED", "rebuild": "다시 실행", "changed": "바뀜"}[state]
        tc = {"cached": "green", "rebuild": "red", "changed": "orange"}[state]
        out.append(f'<div style="background:{bg};border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:10px"><span style="font-size:18px;{MONO};color:var(--navy)">{t}</span><div class="grow"></div><span class="chip" style="font-size:15px;background:var(--{tc});color:#fff">{tag}</span></div>')
    return f'''<div class="card grow" style="gap:8px;border-color:var(--{col})"><h3 style="font-size:23px;color:var(--{col})">{title}</h3><div class="col" style="gap:6px;flex-direction:column-reverse">{"".join(out)}</div><div class="note" style="font-size:18px">{note}</div></div>'''


good = [("FROM python:3.14-slim", "cached"), ("RUN useradd", "cached"), ("COPY requirements.txt", "cached"), ("RUN pip install (20초+)", "cached"), ("COPY app.py", "changed")]
bad = [("FROM python:3.14-slim", "cached"), ("RUN useradd", "cached"), ("COPY app.py requirements.txt", "changed"), ("RUN pip install (20초+)", "rebuild")]
R("w2d3-cache-order", f'''<div class="row c" style="gap:12px;justify-content:center">{icon("FilePen",30,"orange",2)}<div style="font-size:22px;font-weight:800;color:var(--navy)">app.py 한 글자를 고치고 다시 빌드하면</div></div>
<div class="row" style="gap:20px">{stack("좋은 순서 — 1~2초", good, "green", "코드를 맨 위(마지막)에 — 설치는 재사용")}{stack("나쁜 순서 — 20초 이상", bad, "red", "코드가 설치보다 아래 — 위층인 설치를 매번 다시")}</div>
<div class="card fill-slate" style="padding:12px 20px"><p style="font-size:19px">규칙: <b style="color:var(--navy)">거의 안 바뀌는 것 → 의존성 목록 → 설치 → 코드</b> · 한 층이 바뀌면 그 위는 모두 다시</p></div>''')

# 5. 레지스트리 흐름
st = [("Laptop", "teal", "내 노트북", "docker build\ndocker tag"), ("CloudUpload", "violet", "docker push", "내아이디/devmart-catalog-api:1.0.1"),
      ("Warehouse", "violet", "Docker Hub", "태그 + digest sha256:…"), ("Download", "orange", "docker pull", "동료 · CI · K8s · AWS"), ("Box", "green", "어디서든", "같은 이미지 → 같은 실행")]
sc = []
for k, (i, c, t, d) in enumerate(st):
    sc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:18px 10px">{ic(i,c,74)}<h3 style="font-size:22px">{t}</h3><div style="font-size:16px;{MONO};color:var(--slate);white-space:pre-line">{d}</div></div>')
    if k < 4:
        sc.append(arrow(size=28))
R("w2d3-registry-flow", f'''<div class="row flow" style="gap:6px">{"".join(sc)}</div>
<div class="row" style="gap:14px"><div class="card fill-orange grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">태그</b> = 이름표 — 다른 이미지로 옮겨 붙을 수 있다</p></div>
<div class="card fill-teal grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">다이제스트</b> = 내용 지문 — 절대 바뀌지 않는다</p></div>
<div class="card fill-red grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">처음 push = 공개</b> — 비밀값 점검 필수</p></div></div>''')

# 6. 멀티 스테이지
R("w2d3-multistage", f'''<div class="row" style="gap:18px;align-items:stretch">
<div class="card grow" style="gap:10px;border-color:var(--slate);background:var(--slate-l)"><div class="tag">1단계 · FROM golang:1.27 AS build — 주방</div>
 <div class="row" style="gap:10px;flex-wrap:wrap">{"".join(f'<div class="box" style="background:#fff;color:var(--slate);font-size:18px">{x}</div>' for x in ["Go 컴파일러","Debian 전체","빌드 캐시","소스 코드"])}</div>
 <div class="box" style="background:var(--teal);color:#fff;font-size:20px;{MONO}">/hello (실행 파일 하나)</div>
 <div style="font-size:30px;font-weight:900;color:var(--slate);text-align:center">약 1GB</div></div>
<div class="col center" style="gap:6px;justify-content:center">{arrow(size=44)}<div style="font-size:18px;font-weight:800;{MONO};color:var(--teal-d);text-align:center">COPY --from=build<br>/hello만</div></div>
<div class="card grow" style="gap:10px;border-color:var(--green);background:var(--green-l)"><div class="tag">2단계 · FROM scratch — 식탁</div>
 <div class="box" style="background:var(--teal);color:#fff;font-size:20px;{MONO}">/hello</div>
 <div class="row" style="gap:10px"><div class="box grow" style="background:#fff;color:var(--green);font-size:18px">셸 없음 · 공격 표면 최소</div><div class="box grow" style="background:#fff;color:var(--red);font-size:18px">디버깅은 어렵다</div></div>
 <div style="font-size:30px;font-weight:900;color:var(--green);text-align:center">약 10MB</div></div></div>
<div class="card fill-orange" style="padding:12px 20px"><p style="font-size:19px">Python은 인터프리터가 필요해 scratch까지는 안 된다 — <b style="color:var(--navy)">slim</b>으로 충분, C 라이브러리를 컴파일할 때 멀티 스테이지</p></div>''')
