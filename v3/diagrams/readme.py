"""GitHub README 배너 — '앱 하나의 여행' 노선도. 실행: python3 diagrams/readme.py
출력: assets/readme/hero.png, assets/readme/week1.png … week5.png
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, icon  # noqa: E402

OUT = ROOT / "assets" / "readme"
NAVY, TEAL, ORANGE, MUTED, LINE = "#0F2A44", "#0089A0", "#C8651B", "#A9B6C3", "#D5DEE6"
STOPS = [("BookOpen", "기초 이론", "서버 · 네트워크 · 클라우드"),
         ("Container", "Docker + Git", "내 노트북의 컨테이너"),
         ("Network", "MSA + Kubernetes", "여러 서비스를 클러스터로"),
         ("Activity", "Kubernetes 운영", "Helm · 관측 · GitOps · 메시"),
         ("Cloud", "AWS + Terraform + EKS", "코드로 세우고 지우는 클라우드")]
TITLES = {1: "클라우드·컴퓨팅 기초 이론", 2: "Docker + Git 첫 실습", 3: "MSA + Kubernetes 입문", 4: "Kubernetes 운영", 5: "AWS + Terraform + EKS"}
LEADS = {1: "서버, 네트워크, 클라우드, 그리고 DevOps — 앞으로 5주를 읽기 위한 지도",
         2: "내 노트북에 개발 환경을 만들고, 앱 하나를 컨테이너로 포장해 실행하기까지",
         3: "여러 서비스로 나뉜 앱을 실행하고, 자동으로 검증하고, Kubernetes 위에 올리기까지",
         4: "Helm으로 설치하고, 표준 입구로 들이고, 지켜보고, Git으로 맞추고, 그물로 잇고, 지키기까지",
         5: "내 계정을 지키고, 네트워크를 그리고, 클릭을 코드로 바꾸고, 클러스터를 세웠다가 깨끗이 지우기까지"}
FONT = "font-family:Pretendard,sans-serif"
RESET = "<style>.canvas{padding:0!important;display:block!important}</style>"


def route(cur: int | None, w: int, compact: bool) -> str:
    """다섯 정거장과 25개의 일차 눈금. cur=None이면 전체가 켜진 노선."""
    n = 5
    pad = 160
    seg = (w - 2 * pad) / (n - 1)
    y = 46
    parts = [f'<div style="position:relative;height:{150 if not compact else 128}px;width:{w}px">']
    # 바탕 선 + 지나온 구간
    parts.append(f'<div style="position:absolute;left:{pad}px;top:{y-3}px;width:{w-2*pad}px;height:6px;border-radius:3px;background:{LINE}"></div>')
    lit_end = (w - 2 * pad) if cur is None else seg * (cur - 1)
    if lit_end > 0:
        parts.append(f'<div style="position:absolute;left:{pad}px;top:{y-3}px;width:{lit_end}px;height:6px;border-radius:3px;background:{TEAL}"></div>')
    for i, (ic_name, name, sub) in enumerate(STOPS, 1):
        x = pad + seg * (i - 1)
        on = cur is None or i <= cur
        here = cur == i
        last = i == n
        col = (ORANGE if last and cur in (None, 5) else TEAL) if on else MUTED
        # 일차 눈금 (정거장 사이 5칸 중 이 주의 5일)
        if i < n or True:
            for d in range(5):
                tx = x + (d + 1) * (seg / 6) if i < n else None
                if tx is None:
                    break
                tick_on = cur is None or i < cur
                parts.append(f'<div style="position:absolute;left:{tx-4}px;top:{y-4}px;width:8px;height:8px;border-radius:4px;background:{"#FFFFFF" if tick_on else "#F4F7FA"};border:2px solid {TEAL if tick_on else LINE}"></div>')
        size = 74 if here else 60
        parts.append(f'<div style="position:absolute;left:{x-size/2}px;top:{y-size/2}px;width:{size}px;height:{size}px;border-radius:50%;'
                     f'background:{"#FFFFFF" if not here else col};border:{4 if on else 3}px solid {col};display:flex;align-items:center;justify-content:center">'
                     f'{icon(ic_name, int(size*0.46), "#FFFFFF" if here else col, 2.2)}</div>')
        lc = NAVY if on else MUTED
        parts.append(f'<div style="position:absolute;left:{x-120}px;top:{y+46}px;width:240px;text-align:center;{FONT}">'
                     f'<div style="font-size:15px;font-weight:700;color:{col if on else MUTED}">{i}주차</div>'
                     f'<div style="font-size:{21 if here else 19}px;font-weight:{800 if here else 700};color:{lc};margin-top:2px">{name}</div>'
                     + ("" if compact else f'<div style="font-size:14px;color:{"#5B6B7C" if on else MUTED};margin-top:3px">{sub}</div>') + '</div>')
    parts.append("</div>")
    return "".join(parts)


def hero():
    w, h = 1600, 480
    body = RESET + f'''<div style="width:{w}px;height:{h}px;background:#FFFFFF;{FONT};position:relative;overflow:hidden">
      <div style="position:absolute;left:0;top:0;width:{w}px;height:10px;display:flex">
        {''.join(f'<div style="flex:1;background:{c}"></div>' for c in (TEAL,)*4 + (ORANGE,))}</div>
      <div style="padding:58px 70px 0 70px">
        <div style="font-size:24px;font-weight:600;color:{TEAL}">Cloud Native DevOps 기초 과정</div>
        <div style="font-size:64px;font-weight:800;color:{NAVY};letter-spacing:-1.5px;line-height:1.12;margin-top:10px">앱 하나를 노트북에서 클라우드까지</div>
        <div style="font-size:24px;color:#475569;margin-top:16px;max-width:1150px;line-height:1.5">작은 쇼핑몰 DevMart를 5주 동안 컨테이너에 담고, 클러스터에 올리고, AWS에 세웠다가 깨끗이 지웁니다.</div>
      </div>
      <div style="position:absolute;left:0;top:{h-185}px">{route(None, w, False)}</div>
    </div>'''
    render(OUT / "hero.png", body, w=w, h=h, scale=1)


def week(n: int):
    w, h = 1600, 330
    body = RESET + f'''<div style="width:{w}px;height:{h}px;background:#FFFFFF;{FONT};position:relative;overflow:hidden">
      <div style="padding:36px 70px 0 70px;display:flex;align-items:baseline;gap:22px">
        <div style="font-size:52px;font-weight:800;color:{ORANGE if n == 5 else TEAL};letter-spacing:-1px">{n}주차</div>
        <div style="font-size:42px;font-weight:800;color:{NAVY};letter-spacing:-0.8px">{TITLES[n]}</div>
      </div>
      <div style="padding:8px 70px 0 70px;font-size:22px;color:#475569">{LEADS[n]}</div>
      <div style="position:absolute;left:0;top:{h-150}px">{route(n, w, True)}</div>
    </div>'''
    render(OUT / f"week{n}.png", body, w=w, h=h, scale=1)


if __name__ == "__main__":
    hero()
    for i in range(1, 6):
        week(i)
    print("ok", OUT)
