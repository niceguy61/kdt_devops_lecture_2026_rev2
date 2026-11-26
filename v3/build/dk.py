"""Diagram Kit — HTML/CSS 다이어그램을 헤드리스 Chrome으로 PNG 렌더링한다.

화살표는 flex 레이아웃 안의 요소(.arr)로 배치하므로 박스와 어긋나지 않는다.
노드-엣지 그래프가 필요할 때는 gv()로 Graphviz 자동 레이아웃을 쓴다.
"""
from __future__ import annotations
import glob, os, re, subprocess, tempfile, shutil
from pathlib import Path

BUILD = Path(__file__).resolve().parent
ICONS = BUILD / "icons"
_REPO_ICONS = BUILD.parents[1] / "reference" / "icons"
AWS_DIR = Path(os.environ.get("AWS_ICONS", str(_REPO_ICONS if _REPO_ICONS.exists() else Path.home() / "awsicons")))
CSS = (BUILD / "diagram.css").read_text(encoding="utf-8")
CHROME = shutil.which("google-chrome") or shutil.which("chromium")

COLORS = {"teal": "#0089A0", "orange": "#C8651B", "navy": "#0F2A44", "slate": "#475569",
          "red": "#B83227", "green": "#2E7D4F", "violet": "#5B4BB7", "white": "#FFFFFF",
          "muted": "#94A3B8"}
LIGHT = {"teal": "#E0F3F6", "orange": "#FBEBDD", "navy": "#DCE5EE", "slate": "#EEF2F6",
         "red": "#FBE7E5", "green": "#E3F3E9", "violet": "#ECEAFB", "white": "#FFFFFF"}


def icon(name: str, size: int = 40, color: str = "navy", stroke: float = 2.0) -> str:
    """lucide 아이콘을 인라인 SVG로 반환 (name 예: 'Server' 또는 'LuServer')."""
    n = name if name.startswith("Lu") else "Lu" + name
    p = ICONS / f"{n}.svg"
    if not p.exists():
        raise FileNotFoundError(f"아이콘 없음: {n}")
    svg = p.read_text()
    c = COLORS.get(color, color)
    svg = svg.replace('height="24" width="24"', f'height="{size}" width="{size}"', 1)
    svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
    return svg.replace("<svg ", f'<svg style="color:{c}" ', 1)


def ic(name: str, color: str = "teal", size: int = 76, bg: str | None = None) -> str:
    """원형 배경 위의 아이콘."""
    b = bg or LIGHT.get(color, "#EEF2F6")
    return (f'<span class="ic" style="width:{size}px;height:{size}px;background:{b}">'
            f'{icon(name, int(size*0.52), color)}</span>')


def aws(name: str, size: int = 64) -> str:
    """AWS 공식 아이콘(SVG)을 data URI로 인라인."""
    hits = [h for h in glob.glob(str(AWS_DIR / "**" / f"*{name}*.svg"), recursive=True)]
    if not hits:
        raise FileNotFoundError(f"AWS 아이콘 없음: {name}")
    hits.sort(key=len)
    import base64
    data = base64.b64encode(Path(hits[0]).read_bytes()).decode()
    return f'<img src="data:image/svg+xml;base64,{data}" style="width:{size}px;height:{size}px;display:block">'


def arrow(direction: str = "right", size: int = 44, color: str = "#9AAAB8") -> str:
    d = {"right": "ArrowRight", "down": "ArrowDown", "left": "ArrowLeft", "up": "ArrowUp",
         "both": "ArrowLeftRight"}[direction]
    return f'<div class="arr">{icon(d, size, color, 2.5)}</div>'


def render(out: str | Path, body: str, w: int = 1320, h: int = 1100, scale: int = 2) -> Path:
    """body(HTML)를 w x h 캔버스로 렌더링해 PNG 저장."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
    .canvas{{width:{w}px;height:{h}px}}</style></head><body><div class="canvas">{body}</div></body></html>"""
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "d.html"; f.write_text(html, encoding="utf-8")
        # 소스 HTML도 남겨둔다 (수정용)
        src = out.parent / "_src"; src.mkdir(exist_ok=True)
        (src / (out.stem + ".html")).write_text(html, encoding="utf-8")
        cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
               f"--window-size={w},{h}", f"--force-device-scale-factor={scale}",
               "--default-background-color=FFFFFFFF", f"--screenshot={out}", f.as_uri()]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if not out.exists():
            raise RuntimeError(r.stderr[-800:])
    trim(out, pad=28 * scale)
    return out


def trim(path, pad=56):
    """흰 여백을 잘라 내용에 딱 맞게 만든다 (페이지/슬라이드가 비어 보이지 않게)."""
    from PIL import Image, ImageChops
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        l, t, r, b = bbox
        im = im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))
        im.save(path, optimize=True)


def gv(out: str | Path, dot: str, dpi: int = 220) -> Path:
    """Graphviz dot 소스를 PNG로 렌더링 (자동 레이아웃)."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    (out.with_suffix(".dot")).write_text(dot, encoding="utf-8")
    subprocess.run(["dot", "-Tpng", f"-Gdpi={dpi}", "-o", str(out)], input=dot, text=True, check=True)
    return out
