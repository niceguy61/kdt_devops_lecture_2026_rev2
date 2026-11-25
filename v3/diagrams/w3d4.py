"""3주차 4일차 다이어그램. 실행: python3 diagrams/w3d4.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week3" / "day4"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def box(t, c, mono=True, size=15):
    f = MONO if mono else ""
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:{size}px;{f};border:1.5px solid var(--{c})">{t}</div>'


def flow(items, size=20):
    out = []
    for k, x in enumerate(items):
        out.append(x)
        if k < len(items) - 1:
            out.append(arrow(size=size))
    return f'<div class="row flow" style="gap:4px;align-items:center">{"".join(out)}</div>'


def step(n, t, d, c, i):
    return f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div>{ic(i,c,46)}<b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:15px;{MONO};color:var(--slate);white-space:pre-line;text-align:center">{d}</span></div>'


# 1. kubectl 루프
R("w3d4-kubectl-loop", f'''{flow([step("1", "쓰기", "kubectl apply -f\n원하는 상태 보내기", "violet", "FileText"),
 step("2", "보기", "kubectl get\n-o wide · -w", "teal", "Eye"),
 step("3", "읽기", "kubectl describe\nEvents 맨 아래", "orange", "Search"),
 step("4", "듣기", "kubectl logs\n--previous", "orange", "ScrollText"),
 step("5", "고치기", "YAML 수정\n→ 다시 1로", "green", "Wrench")])}
<div class="row" style="gap:14px">{note("teal", "명령 하나 뒤에는 <b style='color:var(--navy)'>항상 get</b> — apply 성공은 '저장됐다'일 뿐")}{note("orange", "<b style='color:var(--navy)'>describe는 클러스터 쪽</b>, <b style='color:var(--navy)'>logs는 앱 쪽</b> 이야기")}</div>''', w=1600)

# 2. Pod 장애 지도
rows = [("Pending", "violet", "스케줄러가 못 놓음", "describe → FailedScheduling", "메모리 · CPU 부족, 테인트, 조건"),
        ("ErrImagePull / ImagePullBackOff", "orange", "이미지를 못 받음", "describe → Failed ... pull", "태그 · 이름 오타, 비공개 레지스트리"),
        ("CrashLoopBackOff", "red", "시작하자마자 죽음 → 재시작 반복", "logs --previous", "설정 · 환경 변수 오류, 앱 버그"),
        ("Running · 0/1 READY", "slate", "떴지만 준비 안 됨", "describe → Readiness probe failed", "의존 대상(DB) 없음 — 5일차"),
        ("Running · 1/1", "green", "떴다 — 그래도 기능은?", "logs · curl", "앱 안의 오류 (503 등)")]
tr = "".join(f'''<div class="row" style="gap:10px;align-items:stretch">
<div class="box" style="width:380px;background:var(--{c}-l);border:1.5px solid var(--{c});color:var(--navy);font-size:17px;{MONO};text-align:left"><b>{s}</b></div>
<div class="box grow" style="background:#fff;border:1.5px solid var(--line);color:var(--navy);font-size:17px;text-align:left">{m}</div>
<div class="box" style="width:380px;background:#0F1E2E;color:#E2E8F0;font-size:16px;{MONO};text-align:left">{w}</div>
<div class="box" style="width:330px;background:var(--slate-l);color:var(--navy);font-size:16px;text-align:left">{why}</div></div>''' for s, c, m, w, why in rows)
R("w3d4-pod-troubleshoot", f'''<div class="row" style="gap:10px;font-size:16px;color:var(--slate);font-weight:800"><div style="width:380px">STATUS</div><div class="grow">뜻</div><div style="width:380px">어디를 보나</div><div style="width:330px">흔한 원인</div></div>
<div class="col" style="gap:8px">{tr}</div>
<div class="row" style="gap:14px">{note("violet", "어제 6단계 중 <b style='color:var(--navy)'>몇 단계에서 멈췄나</b>부터 — 3 Pending · 5 Image · 6 이후 Crash")}{note("red", "죽은 컨테이너의 로그는 <b style='color:var(--navy)'>--previous</b> — 지금 것은 막 다시 뜬 새 컨테이너")}</div>''', w=1650)

# 3. 소유 사슬
def podc(n, c="teal"):
    return f'<div class="card center" style="gap:4px;padding:10px 8px;border-color:var(--{c})">{icon("Box",24,c,2)}<span style="font-size:14px;{MONO};color:var(--navy)">{n}</span><span class="chip" style="font-size:12px;background:var(--{c}-l);color:var(--navy);{MONO}">app=catalog-api</span></div>'


R("w3d4-ownership", f'''<div class="row" style="gap:16px;align-items:center">
<div class="card center" style="width:300px;gap:8px;padding:16px;border-color:var(--violet)">{ic("FileText","violet",54)}<b style="font-size:21px;{MONO};color:var(--navy)">Deployment</b><span style="font-size:16px;{MONO};color:var(--slate)">catalog-api</span><span style="font-size:15px;color:var(--slate);text-align:center">버전 교체 담당<br>replicas: 3 · template</span></div>
<div class="col center" style="gap:2px">{arrow(size=30)}<span style="font-size:14px;color:var(--slate)">만든다</span></div>
<div class="card center" style="width:320px;gap:8px;padding:16px;border-color:var(--orange)">{ic("Layers","orange",54)}<b style="font-size:21px;{MONO};color:var(--navy)">ReplicaSet</b><span style="font-size:16px;{MONO};color:var(--slate)">catalog-api-6b8f7c9d5c</span><span style="font-size:15px;color:var(--slate);text-align:center">개수 담당 · 템플릿 해시가 이름에</span></div>
<div class="col center" style="gap:2px">{arrow(size=30)}<span style="font-size:14px;color:var(--slate)">셀렉터로 센다</span></div>
<div class="row" style="gap:8px;flex:1">{podc("…-4xk2m")}{podc("…-9tq7w")}{podc("…-hz5rp")}</div></div>
<div class="row" style="gap:14px">{note("orange", "이름이 아니라 <b style='color:var(--navy)'>라벨</b>로 센다 — 라벨을 떼면 '내 것'이 아니게 된다")}{note("violet", "사람은 <b style='color:var(--navy)'>Deployment만</b> 만진다 — ReplicaSet · Pod는 컨트롤러가 만들고 지운다")}</div>''', w=1650)

# 4. Service
def wpod(n, ip, node):
    return f'<div class="card center grow" style="gap:4px;padding:10px 6px;border-color:var(--teal)">{icon("Box",24,"teal",2)}<span style="font-size:14px;{MONO};color:var(--navy)">{n}</span><span style="font-size:14px;{MONO};color:var(--slate)">{ip}</span><span style="font-size:13px;color:var(--slate)">{node}</span></div>'


R("w3d4-service", f'''<div class="row" style="gap:14px;align-items:center">
<div class="col" style="gap:10px;width:300px">
<div class="card center" style="gap:4px;padding:12px;border-color:var(--navy)">{ic("Box","navy",44)}<b style="font-size:18px;{MONO};color:var(--navy)">클러스터 안 Pod</b><span style="font-size:15px;{MONO};color:var(--slate)">http://catalog-api/api/info</span></div>
<div class="card center" style="gap:4px;padding:12px;border-color:var(--navy)">{ic("Laptop","navy",44)}<b style="font-size:18px;color:var(--navy)">내 브라우저</b><span style="font-size:15px;{MONO};color:var(--slate)">localhost:30080</span></div></div>
<div class="col center" style="gap:10px">{arrow(size=26)}{arrow(size=26)}</div>
<div class="col" style="gap:10px;width:330px">
<div class="card center" style="gap:4px;padding:12px;border-color:var(--violet)">{ic("BookOpen","violet",44)}<b style="font-size:18px;color:var(--navy)">CoreDNS</b><span style="font-size:15px;{MONO};color:var(--slate)">catalog-api → 10.96.142.87</span></div>
<div class="card center" style="gap:4px;padding:12px;border-color:var(--violet)">{ic("DoorOpen","violet",44)}<b style="font-size:18px;color:var(--navy)">NodePort 30080</b><span style="font-size:15px;color:var(--slate)">kind 포트 통로 → 노드</span></div></div>
<div class="col center">{arrow(size=30)}</div>
<div class="card center" style="width:300px;gap:6px;padding:14px;border-color:var(--orange)">{ic("Split","orange",54)}<b style="font-size:20px;{MONO};color:var(--navy)">Service</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">catalog-api<br>ClusterIP 10.96.142.87:80<br>selector app=catalog-api</span><span style="font-size:14px;color:var(--slate)">kube-proxy 규칙이 나눠 보냄</span></div>
<div class="col center">{arrow(size=30)}</div>
<div class="col" style="gap:8px;flex:1">{box("EndpointSlice — 준비된 Pod IP 목록", "orange")}
<div class="row" style="gap:8px">{wpod("…-4xk2m", "10.244.1.5:8000", "worker")}{wpod("…-9tq7w", "10.244.2.4:8000", "worker2")}{wpod("…-hz5rp", "10.244.1.6:8000", "worker")}</div></div></div>
<div class="row" style="gap:14px">{note("orange", "Pod IP는 바뀌어도 <b style='color:var(--navy)'>Service 이름 · IP는 그대로</b> — 2주차 Compose DNS의 Kubernetes판")}{note("violet", "Service가 Pod를 찾는 방법도 <b style='color:var(--navy)'>라벨 셀렉터</b> — 오타 하나면 목록이 텅 빈다")}</div>''', w=1700)

# 5. 롤링 업데이트
def rsrow(label, old, new, note_):
    cells = "".join(f'<div style="width:46px;height:46px;border-radius:10px;background:var(--slate-l);border:2px solid var(--slate)"></div>' for _ in range(old))
    cells += "".join(f'<div style="width:46px;height:46px;border-radius:10px;background:var(--teal-l);border:2px solid var(--teal)"></div>' for _ in range(new))
    return f'<div class="row c" style="gap:14px"><div style="width:120px;font-size:17px;font-weight:900;color:var(--navy)">{label}</div><div class="row" style="gap:8px;width:250px">{cells}</div><span style="font-size:16px;color:var(--slate)">{note_}</span></div>'


R("w3d4-rolling", f'''<div class="row" style="gap:20px;align-items:stretch">
<div class="card" style="gap:10px;padding:16px;flex:1;border-color:var(--teal)"><div class="row c" style="gap:8px">{icon("RefreshCw",28,"teal",2)}<b style="font-size:21px;color:var(--navy)">성공한 교체 — APP_VERSION 2.0.0 → 2.1.0</b></div>
{rsrow("시작", 3, 0, "옛 ReplicaSet 3")}{rsrow("1", 3, 1, "새 것 하나 더 (maxSurge 1)")}{rsrow("2", 2, 1, "새 것이 준비되면 옛 것 하나 내림")}{rsrow("3", 2, 2, "")}{rsrow("…", 0, 3, "옛 ReplicaSet 0 — 지우지 않고 남겨 둔다")}
<div class="row c" style="gap:10px"><div style="width:22px;height:22px;border-radius:6px;background:var(--slate-l);border:2px solid var(--slate)"></div><span style="font-size:15px;color:var(--slate)">옛 버전</span><div style="width:22px;height:22px;border-radius:6px;background:var(--teal-l);border:2px solid var(--teal)"></div><span style="font-size:15px;color:var(--slate)">새 버전</span></div></div>
<div class="card" style="gap:10px;padding:16px;width:560px;border-color:var(--red);background:#FFF8F7"><div class="row c" style="gap:8px">{icon("ShieldAlert",28,"red",2)}<b style="font-size:21px;color:var(--red)">실패한 교체 — 태그 오타</b></div>
<div class="row" style="gap:8px">{"".join('<div style="width:46px;height:46px;border-radius:10px;background:var(--slate-l);border:2px solid var(--slate)"></div>' for _ in range(3))}<div style="width:46px;height:46px;border-radius:10px;background:var(--red-l);border:2px dashed var(--red)"></div></div>
<span style="font-size:17px;color:var(--navy)">새 Pod 하나가 <b style="{MONO}">ImagePullBackOff</b> — 준비되지 않으니 <b>옛 Pod를 내리지 않는다</b></span>
<span style="font-size:17px;color:var(--navy)">사용자는 계속 2.1.0을 받는다 — <b>장애가 아니라 '멈춘 배포'</b></span>
<div class="box" style="background:#0F1E2E;color:#E2E8F0;font-size:16px;{MONO};text-align:left">kubectl rollout undo deployment/catalog-api</div></div></div>
<div class="row" style="gap:14px">{note("teal", "Deployment가 <b style='color:var(--navy)'>새 ReplicaSet을 만들고</b> 두 ReplicaSet의 개수를 조금씩 옮긴다")}{note("orange", "되돌리기 = 옛 ReplicaSet을 다시 키우기 — <b style='color:var(--navy)'>그래서 몇 초면 끝난다</b>")}</div>''', w=1650)
