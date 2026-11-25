"""4주차 2일차 다이어그램. 실행: python3 diagrams/w4d2.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week4" / "day2"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def box(t, c, size=15):
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:{size}px;{MONO};border:1.5px solid var(--{c});text-align:left">{t}</div>'


def card(t, sub, c, i, mono=False):
    f = MONO if mono else ""
    return f'<div class="card center grow" style="gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,46)}<b style="font-size:18px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


# 1. 세 기둥
def pillar(t, q, ex, tool, c, i):
    return f'''<div class="card grow" style="gap:8px;padding:14px;border-color:var(--{c})"><div class="row c" style="gap:8px">{ic(i,c,44)}<b style="font-size:22px;color:var(--navy)">{t}</b></div>
<span style="font-size:17px;color:var(--navy)"><b>묻는 것</b> — {q}</span>{box(ex, c, 14)}<span style="font-size:15px;color:var(--slate)">{tool}</span></div>'''


R("w4d2-pillars", f'''<div class="row" style="gap:14px;align-items:stretch">
{pillar("로그 (logs)", "<b>무슨 일이</b> 있었나 — 사건 한 건의 이야기", '{"event": "order_saved",<br> "request_id": "5b2e…", "order_id": 61}', "3주차: kubectl logs · 오늘: 소개만 (Loki)", "orange", "ScrollText")}
{pillar("메트릭 (metrics)", "<b>얼마나</b> — 시간에 따른 숫자", "envoy_cluster_upstream_rq_total<br>{envoy_cluster_name=&quot;…/orders/…&quot;} 1532", "오늘의 주인공: Prometheus · Grafana", "teal", "ChartLine")}
{pillar("트레이스 (traces)", "<b>어디서</b> 시간이 걸렸나 — 요청 하나의 여정", "web 2ms → order-api 41ms<br>  └ catalog-api 12ms", "3주차 요청 ID의 진화형 · OpenTelemetry", "violet", "Waypoints")}</div>
<div class="row" style="gap:14px">{note("teal", "메트릭으로 <b style='color:var(--navy)'>이상을 알아채고</b>, 트레이스로 <b style='color:var(--navy)'>어디인지 좁히고</b>, 로그로 <b style='color:var(--navy)'>왜인지 읽는다</b>")}{note("violet", "세 기둥을 <b style='color:var(--navy)'>같은 요청 ID · 라벨</b>로 이어 붙일 수 있어야 관찰 가능하다")}</div>''', w=1650)

# 2. kube-prometheus-stack 구조
R("w4d2-kps", f'''<div class="row" style="gap:14px;align-items:stretch">
<div class="col" style="gap:8px;width:330px">
<div class="row c" style="gap:6px">{icon("Crosshair",22,"slate",2)}<b style="font-size:18px;color:var(--navy)">긁어 갈 곳 (targets)</b></div>
{box("kubelet · cAdvisor — 컨테이너 CPU · 메모리", "slate")}{box("node-exporter — 노드 디스크 · 네트워크", "slate")}{box("kube-state-metrics — Deployment · Pod 상태", "slate")}{box("Envoy (PodMonitor) — 요청 수 · 오류 · 시간", "orange")}</div>
<div class="col center" style="gap:4px">{arrow(size=26)}<span style="font-size:13px;color:var(--slate)">15초마다<br>pull</span></div>
<div class="col" style="gap:10px;flex:1">
<div class="row" style="gap:10px">{card("Prometheus", "시계열 DB · PromQL<br>규칙 평가", "red", "Database")}{card("Alertmanager", "묶기 · 잠재우기<br>→ Slack · 메일", "orange", "BellRing")}{card("Grafana", "대시보드<br>사이드카가 ConfigMap 읽음", "teal", "LayoutDashboard")}</div>
<div class="card" style="gap:6px;padding:12px;border-color:var(--violet);background:#FBFAFF"><div class="row c" style="gap:8px">{icon("Cog",24,"violet",2)}<b style="font-size:18px;color:var(--navy);{MONO}">prometheus-operator</b><span style="font-size:15px;color:var(--slate)">CRD를 읽어 Prometheus 설정을 만든다 (3주차 reconcile)</span></div>
<div class="row" style="gap:8px">{box("ServiceMonitor", "violet")}{box("PodMonitor", "violet")}{box("PrometheusRule", "violet")}{box("Prometheus · Alertmanager", "violet")}</div></div></div></div>
<div class="row" style="gap:14px">{note("red", "Prometheus는 <b style='color:var(--navy)'>가서 긁어 온다</b>(pull) — 앱은 /metrics만 열어 두면 된다")}{note("violet", "설정 파일을 고치지 않고 <b style='color:var(--navy)'>CRD를 apply</b> — 팀마다 자기 ServiceMonitor · 규칙을 둔다")}</div>''', w=1700)

# 3. RED / USE
def sig(l, t, q, c):
    return f'<div class="row" style="gap:8px;align-items:stretch"><div class="box" style="width:70px;background:var(--{c});color:#fff;font-size:24px;font-weight:900">{l}</div><div class="box" style="width:200px;background:var(--{c}-l);color:var(--navy);font-size:17px;text-align:left"><b>{t}</b></div><div class="box grow" style="background:#0F1E2E;color:#E2E8F0;font-size:14px;{MONO};text-align:left">{q}</div></div>'


R("w4d2-red-use", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1.3;gap:8px;padding:14px;border-color:var(--teal)"><b style="font-size:21px;color:var(--navy)">RED — 요청을 받는 서비스 (Gateway에서 본다)</b>
{sig("R", "Rate 초당 요청", "sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_total[1m]))", "teal")}
{sig("E", "Errors 실패 비율", "… rq_xx{envoy_response_code_class=&quot;5&quot;} / … rq_total", "red")}
{sig("D", "Duration 응답 시간", "histogram_quantile(0.95, sum by (le, …) (rate(…_rq_time_bucket[1m])))", "violet")}</div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--orange)"><b style="font-size:21px;color:var(--navy)">USE — 자원 (Pod · 노드)</b>
{sig("U", "Utilization 사용률", "rate(container_cpu_usage_seconds_total[1m])", "orange")}
{sig("S", "Saturation 포화", "throttling · 큐 길이 · OOMKilled 재시작", "orange")}
{sig("E", "Errors 오류", "kube_pod_container_status_restarts_total", "red")}</div></div>
<div class="row" style="gap:14px">{note("teal", "구글 SRE의 <b style='color:var(--navy)'>네 가지 황금 신호</b> = 지연 · 트래픽 · 오류 · 포화")}{note("orange", "DevMart 앱은 /metrics가 없다 — 그래도 <b style='color:var(--navy)'>입구(Envoy)에서</b> RED를 다 볼 수 있다")}</div>''', w=1700)

# 4. 알림 흐름
st = [("1", "규칙 평가", "expr > 0.05\n15초마다", "red", "Calculator"), ("2", "Pending", "조건 참\nfor: 1m 기다림", "orange", "Hourglass"), ("3", "Firing", "1분 넘게 참\n→ Alertmanager로", "red", "Flame"),
      ("4", "Alertmanager", "묶기 · 잠재우기\n· 억제", "orange", "Filter"), ("5", "받는 곳", "Slack · 메일\n· 호출 (PagerDuty)", "teal", "BellRing"), ("6", "사람", "런북을 연다\nrunbook_url", "violet", "BookOpen")]
sc = []
for k, (n, t, d, c, i) in enumerate(st):
    sc.append(f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div>{ic(i,c,44)}<b style="font-size:18px;color:var(--navy)">{t}</b><span style="font-size:14px;{MONO};color:var(--slate);white-space:pre-line;text-align:center">{d}</span></div>')
    if k < len(st) - 1:
        sc.append(arrow(size=18))
R("w4d2-alert-flow", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(sc)}</div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>for:</b>는 순간의 흔들림을 거른다 — 3주차 노드 장애의 '하트비트 기다림'과 같은 이유")}{note("violet", "알림은 <b style='color:var(--navy)'>사람이 행동할 일</b>에만 — 행동할 게 없는 알림은 소음이 된다")}</div>''', w=1650)
