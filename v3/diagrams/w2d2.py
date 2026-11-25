"""2주차 2일차 다이어그램. 실행: python3 diagrams/w2d2.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week2" / "day2"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


# 1. 이미지와 컨테이너
cont = "".join(f'''<div class="card center" style="gap:6px;padding:14px;border-color:var(--orange)">{icon("Box",44,"orange",2)}<div style="font-size:20px;font-weight:800;color:var(--navy)">{n}</div>
<div class="chip" style="font-size:16px;background:var(--{c}-l);color:var(--{c})">{s}</div><div style="font-size:15px;{MONO};color:var(--slate)">{p}</div></div>''' for n, s, c, p in [("web", "Up", "green", ":8080"), ("web2", "Up", "green", ":8081"), ("old", "Exited (0)", "slate", "—")])
R("w2d2-image-container", f'''<div class="row" style="gap:22px;align-items:center">
<div class="card fill-teal center" style="width:330px;gap:10px">{ic("Layers","teal",96)}<h3 style="font-size:27px">이미지</h3><div style="font-size:19px;{MONO};color:var(--teal-d)">nginx:1.30-alpine</div>
 <div class="box" style="background:#fff;color:var(--navy);font-size:18px;width:100%">읽기 전용 · 바뀌지 않는다</div><div class="note" style="font-size:17px">붕어빵 틀 · 밀키트</div></div>
<div class="col center" style="gap:6px">{arrow(size=44)}<div style="font-size:18px;font-weight:800;color:var(--slate);{MONO}">docker run</div></div>
<div class="col grow" style="gap:12px"><div class="tag">컨테이너 — 실행 중이거나 멈춘 프로세스, 각자 쓰기 가능한 층</div><div class="grid" style="grid-template-columns:repeat(3,1fr);gap:12px">{cont}</div>
<div class="row" style="gap:12px"><div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:18px">docker images — 틀 목록</div><div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:18px">docker ps -a — 붕어빵 목록</div></div></div></div>
<div class="card fill-orange" style="padding:14px 22px"><p style="font-size:20px">컨테이너 안에서 바꾼 것은 <b style="color:var(--navy)">컨테이너를 지우면 사라진다</b> — 이미지는 그대로 (→ 3일차 이미지 빌드, 4일차 볼륨)</p></div>''')

# 2. 안과 밖
rows = [("FolderTree", "OS 파일", "Alpine Linux", "Ubuntu / macOS", "다르다", "teal"), ("ListTree", "프로세스", "2개 · 내가 PID 1", "수백 개", "다르다", "teal"),
        ("Tag", "호스트 이름", "컨테이너 ID", "노트북 이름", "다르다", "teal"), ("Cpu", "커널", "6.6.x-…-WSL2", "6.6.x-…-WSL2", "같다!", "orange")]
rr = "".join(f'''<div class="row c" style="gap:12px"><div class="row c" style="width:230px;gap:10px">{icon(i,36,c,2)}<span style="font-size:21px;font-weight:800;color:var(--navy)">{t}</span></div>
<div class="box grow" style="background:var(--teal-l);color:var(--navy);font-size:19px">{a}</div><div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:19px">{b}</div>
<div class="chip" style="width:110px;text-align:center;font-size:18px;background:var(--{c});color:#fff">{v}</div></div>''' for i, t, a, b, v, c in rows)
R("w2d2-inside-outside", f'''<div class="row c" style="gap:12px"><div style="width:230px"></div><div class="tag grow" style="text-align:center">컨테이너 안 (docker run -it alpine sh)</div><div class="tag grow" style="text-align:center">바깥 (호스트)</div><div style="width:110px"></div></div>
<div class="col" style="gap:10px">{rr}</div>
<div class="card fill-orange" style="padding:14px 22px"><p style="font-size:20px">VM은 커널까지 따로, <b style="color:var(--navy)">컨테이너는 커널을 공유</b> — 그래서 가볍고 빠르다 (1주차 2일차)</p></div>''')

# 3. 포트 연결
R("w2d2-port-mapping", f'''<div class="row" style="gap:18px;align-items:center">
<div class="col center" style="width:220px;gap:10px">{ic("Globe","navy",90)}<h3 style="font-size:23px;color:var(--navy)">브라우저</h3><div class="box" style="background:var(--slate-l);color:var(--navy);font-size:18px;{MONO}">localhost:8080</div></div>
{arrow(size=40)}
<div class="grow" style="border:4px solid var(--navy);border-radius:22px;padding:18px;display:flex;flex-direction:column;gap:14px;background:var(--slate-l)">
 <div class="row c" style="gap:10px">{icon("Laptop",36,"navy",2)}<div style="font-size:23px;font-weight:900;color:var(--navy)">내 노트북 (호스트)</div><div class="grow"></div><div class="chip orange" style="font-size:20px;{MONO}">:8080 문</div></div>
 <div class="row c" style="gap:12px;justify-content:center">{icon("ArrowDown",34,"orange",2.5)}<div class="box" style="background:var(--orange);color:#fff;font-size:22px;{MONO}">-p 8080:80</div><div style="font-size:19px;color:var(--slate)">바깥 : 안</div></div>
 <div style="border:3px dashed var(--teal);border-radius:16px;padding:14px;background:#fff;display:flex;align-items:center;gap:14px">{icon("Box",40,"teal",2)}<div style="font-size:21px;font-weight:800;color:var(--navy)">컨테이너 web</div><div class="grow"></div><div class="chip teal" style="font-size:19px;{MONO}">nginx :80</div></div>
</div></div>
<div class="row" style="gap:14px"><div class="card fill-red grow" style="padding:14px 20px"><p style="font-size:19px"><b style="color:var(--navy)">-p 없이</b> PORTS = 80/tcp → 바깥에서 못 들어간다</p></div>
<div class="card fill-green grow" style="padding:14px 20px"><p style="font-size:19px"><b style="color:var(--navy)">-p 8080:80</b> PORTS = 0.0.0.0:8080->80/tcp</p></div>
<div class="card fill-violet grow" style="padding:14px 20px"><p style="font-size:19px"><b style="color:var(--navy)">-p 127.0.0.1:8080:80</b> 내 컴퓨터만</p></div></div>''')

# 4. 관찰 도구
ob = [("ScrollText", "teal", "docker logs", "무슨 일이 있었나", "블랙박스 영상", "logs -f · --tail 3"),
      ("DoorOpen", "orange", "docker exec", "안에서 확인", "차 문 열고 들어가기", "exec -it web sh"),
      ("FileSearch", "violet", "docker inspect", "설정과 상태", "등록증 · 정비 기록", "--format '{{.State.Status}}'"),
      ("Gauge", "green", "docker stats · top", "자원과 프로세스", "계기판", "stats --no-stream")]
oc = "".join(f'''<div class="card center grow" style="gap:8px;border-color:var(--{c})">{ic(i,c,80)}<h3 style="font-size:23px;{MONO}">{t}</h3><p style="font-size:19px;font-weight:700;color:var(--navy)">{q}</p>
<div class="box" style="background:var(--{c}-l);color:var(--slate);font-size:17px;width:100%">비유: {a}</div><div style="font-size:16px;{MONO};color:var(--{c})">{e}</div></div>''' for i, c, t, q, a, e in ob)
R("w2d2-observe", f'''<div class="row" style="gap:14px">{oc}</div>
<div class="card fill-slate" style="padding:14px 22px"><p style="font-size:20px">exec · cp로 고친 것은 <b style="color:var(--navy)">임시</b> — 확인과 디버깅에만 쓰고, 진짜 변경은 이미지(3일차)나 볼륨(4일차)으로</p></div>''')

# 5. 생명주기
def st(name, col, sub):
    return f'<div class="card center" style="width:220px;gap:6px;border-color:var(--{col});border-width:3px;padding:18px"><div style="font-size:26px;font-weight:900;color:var(--{col})">{name}</div><div style="font-size:17px;color:var(--slate)">{sub}</div></div>'


def edge(label, d="right"):
    return f'<div class="col center" style="gap:4px">{arrow(d,34)}<div style="font-size:17px;font-weight:700;{MONO};color:var(--slate);white-space:nowrap">{label}</div></div>'


R("w2d2-lifecycle", f'''<div class="row c" style="gap:10px;justify-content:center">
{ic("Layers","teal",80)}{edge("create")}{st("Created","slate","만들기만 함")}{edge("start")}{st("Up","green","실행 중")}{edge("stop · kill · 스스로 끝")}{st("Exited (코드)","orange","멈춤 · 0 / 137 / …")}{edge("rm")}
<div class="col center" style="gap:4px">{icon("Trash2",54,"red",2)}<div style="font-size:18px;font-weight:700;color:var(--red)">지워짐</div></div></div>
<div class="row c" style="gap:12px;justify-content:center">{icon("Undo2",30,"green",2.2)}<div class="box" style="background:var(--green-l);color:var(--green);font-size:20px">Exited → <span style="{MONO}">docker start</span> → Up (같은 컨테이너, 변경 유지)</div>
<div class="box" style="background:var(--teal-l);color:var(--teal-d);font-size:20px;{MONO}">docker run = create + start</div></div>
<div class="row" style="gap:14px"><div class="card fill-green grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">stop</b> 종료 요청 신호 → 정중히, 보통 <b>0</b></p></div>
<div class="card fill-red grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">kill</b> SIGKILL → 강제, <b>137 = 128 + 9</b></p></div>
<div class="card fill-violet grow" style="padding:12px 18px"><p style="font-size:19px"><b style="color:var(--navy)">--restart on-failure:3</b> 실패하면 다시</p></div></div>''')

# 6. 디버깅 순서
dbg = [("Tag", "slate", "1 이미지", "이름·태그가 맞나", "docker images"), ("Activity", "teal", "2 상태", "살아 있나 · 종료 코드", "docker ps -a"),
       ("ScrollText", "teal", "3 로그", "무슨 말을 남겼나", "docker logs"), ("Plug", "orange", "4 포트", "바깥:안 순서", "docker port"),
       ("DoorOpen", "violet", "5 안쪽", "안에서는 되나", "docker exec")]
sc = []
for k, (i, c, t, d, cmd) in enumerate(dbg):
    sc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:18px 10px">{ic(i,c,70)}<h3 style="font-size:23px">{t}</h3><p style="font-size:18px">{d}</p><div style="font-size:17px;{MONO};color:var(--{c})">{cmd}</div></div>')
    if k < 4:
        sc.append(arrow(size=28))
R("w2d2-debug-order", f'''<div class="row flow" style="gap:6px">{"".join(sc)}</div>
<div class="card fill-slate" style="padding:14px 22px"><p style="font-size:20px"><b style="color:var(--navy)">안에서는 되고 밖에서는 안 된다</b> → 앱이 127.0.0.1에서만 기다리는지 · 포트 순서를 의심 (1주차 3일차)</p></div>''')
