// slides.yaml(→json) → PPTX. 사용법: node build/build_slides.js <slides.json> <out.pptx>
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const React = require("react");
const RDS = require("react-dom/server");
const lu = require("react-icons/lu");

const ROOT = path.resolve(__dirname, "..");
const SKILL = process.env.PPTX_SKILL;
const [, , specPath, outPath] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));

const HEX = { navy: "0F2A44", navy2: "1E3A5F", teal: "0089A0", tealD: "006A7C", tealL: "E0F3F6", orange: "C8651B", orangeL: "FBEBDD",
  slate: "475569", slateL: "F1F5F9", line: "D5DEE6", red: "B83227", redL: "FBE7E5", green: "2E7D4F", greenL: "E3F3E9",
  violet: "5B4BB7", violetL: "ECEAFB", ink: "1E293B", muted: "64748B", white: "FFFFFF" };
const LIGHT = { teal: HEX.tealL, orange: HEX.orangeL, red: HEX.redL, green: HEX.greenL, violet: HEX.violetL, navy: "DCE5EE", slate: HEX.slateL };
const FONT = "맑은 고딕";
const THEME = { name: "Cloud Native DevOps", headFontFace: FONT, bodyFontFace: FONT,
  colors: { dk1: HEX.ink, lt1: HEX.white, dk2: HEX.navy, lt2: HEX.slateL, accent1: HEX.teal, accent2: HEX.orange, accent3: HEX.violet,
    accent4: HEX.green, accent5: HEX.red, accent6: HEX.slate, hlink: HEX.tealD, folHlink: HEX.violet } };

const W = 13.333, H = 7.5, MX = 0.6, CW = W - 2 * MX, TOP = 1.4, BOTTOM = 6.85;

const iconCache = {};
async function iconPng(name, color) {
  const key = name + color;
  if (iconCache[key]) return iconCache[key];
  const C = lu["Lu" + name];
  if (!C) throw new Error("icon missing: " + name);
  let svg = RDS.renderToStaticMarkup(React.createElement(C, { size: 256, color: "#" + color }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return (iconCache[key] = "image/png;base64," + buf.toString("base64"));
}

function imgSize(p) {
  const b = fs.readFileSync(p);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  pres.title = spec.meta.title;
  pres.author = "Cloud Native DevOps 기초 이론 과정";

  const footer = { text: spec.meta.footer, options: { x: MX, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: HEX.muted, fontFace: FONT } };
  pres.defineSlideMaster({ title: "CONTENT", background: { color: HEX.white },
    objects: [{ text: footer }, { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.32, w: CW, h: 0.85, fontSize: 28, bold: true, color: HEX.navy, fontFace: FONT, valign: "middle", align: "left", margin: 0 }, text: "" } }],
    slideNumber: { x: 12.3, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: HEX.muted, fontFace: FONT, align: "right" } });
  pres.defineSlideMaster({ title: "DARK", background: { color: HEX.navy }, objects: [],
    slideNumber: { x: 12.3, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: "7F95AA", fontFace: FONT, align: "right" } });

  const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, fontFace: FONT, margin: 0, color: HEX.ink, valign: "top" }, o));
  const card = (s, x, y, w, h, fill, line) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: line || fill, width: 1 } });
  const dots = (s, x0, y0, on) => { for (let r = 0; r < 5; r++) for (let c = 0; c < 5; c++) { const i = r * 5 + c;
      s.addShape(pres.shapes.OVAL, { x: x0 + c * 0.42, y: y0 + r * 0.42, w: 0.3, h: 0.3, fill: { color: on(i) }, line: { color: on(i) } }); } };
  const callout = (s, y, text, color = "orange") => {
    card(s, MX, y, CW, 0.62, LIGHT[color], LIGHT[color]);
    T(s, text, { x: MX + 0.3, y: y + 0.08, w: CW - 0.6, h: 0.46, fontSize: 15, color: { orange: HEX.orange, teal: HEX.tealD }[color] || HEX[color], bold: true, valign: "middle" });
  };
  const iconCircle = async (s, name, color, x, y, d) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: LIGHT[color] || HEX.slateL }, line: { color: LIGHT[color] || HEX.slateL } });
    s.addImage({ data: await iconPng(name, HEX[color] || color), x: x + d * 0.24, y: y + d * 0.24, w: d * 0.52, h: d * 0.52 });
  };

  let section = "시작";
  for (const sl of spec.slides) {
    if (sl.type === "section") { section = `${sl.num} ${sl.title}`; pres.addSection({ title: section }); }
    else if (sl.type === "cover") pres.addSection({ title: section });
    const dark = ["cover", "section"].includes(sl.type);
    const s = pres.addSlide({ masterName: dark ? "DARK" : "CONTENT", sectionTitle: section });
    if (!dark) s.addText(sl.title, { placeholder: "title" });

    switch (sl.type) {
      case "cover": {
        T(s, sl.kicker, { x: 0.9, y: 1.3, w: 8, h: 0.4, fontSize: 14, bold: true, color: "7FD3E0", charSpacing: 3 });
        T(s, sl.title, { x: 0.9, y: 2.0, w: 8.2, h: 1.9, fontSize: 46, bold: true, color: HEX.white, valign: "middle" });
        T(s, sl.subtitle, { x: 0.9, y: 4.1, w: 8, h: 1.0, fontSize: 17, color: "C9DCE8" });
        dots(s, 9.9, 2.0, (i) => (i < 5 ? HEX.teal : i === 24 ? HEX.orange : HEX.navy2));
        s.addShape(pres.shapes.LINE, { x: 0.9, y: 6.2, w: 11.5, h: 0, line: { color: "2D4C6D", width: 1 } });
        T(s, "5주 · 200시간 · Cloud Native DevOps 기초 이론", { x: 0.9, y: 6.35, w: 8, h: 0.4, fontSize: 12, color: "9FB7CB" });
        break;
      }
      case "agenda": {
        const n = sl.items.length, gap = 0.18, rh = Math.min(0.92, (BOTTOM - TOP - gap * (n - 1)) / n);
        for (let i = 0; i < n; i++) {
          const [time, num, title] = sl.items[i], y = TOP + 0.1 + i * (rh + gap);
          card(s, MX, y, CW, rh, i % 2 ? HEX.white : HEX.slateL, HEX.line);
          T(s, time, { x: MX + 0.35, y, w: 1.3, h: rh, fontSize: 18, color: HEX.muted, bold: true, valign: "middle" });
          s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX + 1.75, y: y + rh / 2 - 0.22, w: 1.1, h: 0.44, rectRadius: 0.22, fill: { color: HEX.teal }, line: { color: HEX.teal } });
          T(s, num, { x: MX + 1.75, y: y + rh / 2 - 0.22, w: 1.1, h: 0.44, fontSize: 14, bold: true, color: HEX.white, align: "center", valign: "middle" });
          T(s, title, { x: MX + 3.1, y, w: 8.6, h: rh, fontSize: 21, bold: true, color: HEX.navy, valign: "middle" });
        }
        break;
      }
      case "section": {
        T(s, sl.num, { x: 0.9, y: 1.1, w: 4, h: 0.6, fontSize: 22, bold: true, color: "7FD3E0", charSpacing: 2 });
        T(s, sl.title, { x: 0.9, y: 1.75, w: 11.5, h: 1.3, fontSize: 40, bold: true, color: HEX.white, valign: "middle" });
        T(s, "이번 시간에 할 일", { x: 0.9, y: 3.5, w: 6, h: 0.4, fontSize: 14, bold: true, color: "9FB7CB" });
        const g = sl.goals, cw = (11.5 - 0.3) / 2;
        for (let i = 0; i < g.length; i++) {
          const x = 0.9 + (i % 2) * (cw + 0.3), y = 4.05 + Math.floor(i / 2) * 1.05;
          card(s, x, y, cw, 0.85, HEX.navy2, HEX.navy2);
          s.addImage({ data: await iconPng("CircleCheck", "7FD3E0"), x: x + 0.28, y: y + 0.235, w: 0.38, h: 0.38 });
          T(s, g[i], { x: x + 0.85, y, w: cw - 1.0, h: 0.85, fontSize: 19, color: HEX.white, valign: "middle", bold: true });
        }
        break;
      }
      case "image": {
        const p = path.join(ROOT, "assets", sl.img), sz = imgSize(p);
        const maxW = CW, maxH = BOTTOM - TOP + 0.05 - (sl.callout ? 0.95 : 0);
        let w = maxW, h = (w * sz.h) / sz.w;
        if (h > maxH) { h = maxH; w = (h * sz.w) / sz.h; }
        const iy = sl.callout ? TOP + Math.max(0, (maxH - h) / 2 - 0.1) : TOP + (maxH - h) / 2;
        s.addImage({ path: p, x: (W - w) / 2, y: iy, w, h, altText: sl.title });
        if (sl.callout) callout(s, Math.min(iy + h + 0.35, BOTTOM - 0.62), sl.callout, sl.callout_color || "teal");
        break;
      }
      case "table": {
        const n = sl.rows.length, availT = BOTTOM - TOP - (sl.callout ? 1.0 : 0.1), rh = Math.min(n > 6 ? 0.55 : 0.85, availT / (n + 1)), fs_ = n > 6 ? 15 : n > 4 ? 16 : 18;
        const mono = sl.mono_col;
        const rows = [sl.head.map((t) => ({ text: t, options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: n > 4 ? 15 : 17 } }))];
        sl.rows.forEach((r, i) => rows.push(r.map((t, j) => ({ text: t, options: {
          fill: { color: i % 2 ? HEX.slateL : HEX.white }, fontSize: fs_, color: j === 0 ? HEX.navy : HEX.ink, bold: j === 0,
          fontFace: mono === j ? "Consolas" : FONT } }))));
        s.addTable(rows, { x: MX, y: TOP, w: CW, colW: sl.colw, rowH: rh, fontFace: FONT, valign: "middle", margin: [0.06, 0.15, 0.06, 0.15],
          border: { type: "solid", pt: 0.75, color: HEX.line } });
        if (sl.callout) callout(s, Math.min(TOP + rh * (n + 1) + 0.3, BOTTOM - 0.62), sl.callout);
        break;
      }
      case "cards": {
        const n = sl.cards.length, gap = 0.25, cw = (CW - gap * (n - 1)) / n, ch = n > 4 ? 3.7 : 3.5, blockH = ch + (sl.callout ? 0.97 : 0), y = TOP + Math.max(0.1, (BOTTOM - TOP - blockH) / 2);
        for (let i = 0; i < n; i++) {
          const [ic, col, head, text] = sl.cards[i], x = MX + i * (cw + gap);
          card(s, x, y, cw, ch, HEX.white, HEX.line);
          await iconCircle(s, ic, col, x + cw / 2 - 0.55, y + 0.4, 1.1);
          T(s, head, { x: x + 0.15, y: y + 1.75, w: cw - 0.3, h: 0.6, fontSize: n > 4 ? 19 : 22, bold: true, color: HEX.navy, align: "center", valign: "middle" });
          T(s, text, { x: x + 0.2, y: y + 2.45, w: cw - 0.4, h: ch - 2.6, fontSize: n > 4 ? 15 : 17, color: HEX.slate, align: "center" });
        }
        if (sl.callout) callout(s, y + ch + 0.35, sl.callout);
        break;
      }
      case "statement": {
        card(s, MX, TOP + 0.2, CW, 3.6, HEX.tealL, HEX.tealL);
        s.addShape(pres.shapes.OVAL, { x: MX + 0.6, y: TOP + 1.2, w: 1.6, h: 1.6, fill: { color: HEX.white }, line: { color: HEX.white } });
        s.addImage({ data: await iconPng(sl.icon, HEX.teal), x: MX + 0.98, y: TOP + 1.58, w: 0.84, h: 0.84 });
        T(s, sl.text, { x: MX + 2.7, y: TOP + 0.4, w: CW - 3.1, h: 3.2, fontSize: 25, bold: true, color: HEX.navy, valign: "middle", paraSpaceAfter: 6 });
        if (sl.sub) T(s, sl.sub, { x: MX, y: TOP + 4.15, w: CW, h: 1.0, fontSize: 18, color: HEX.slate, valign: "top" });
        break;
      }
      case "compare": {
        const cw = (CW - 0.4) / 2, mx = Math.max(sl.left[1].length, sl.right[1].length), ch = Math.min(5.1, 1.5 + mx * 0.78), y0 = TOP + Math.max(0.1, (BOTTOM - TOP - ch) / 2) - 0.1;
        [[sl.left, HEX.slateL, HEX.slate], [sl.right, HEX.tealL, HEX.tealD]].forEach(([[head, items], fill, hc], k) => {
          const x = MX + k * (cw + 0.4);
          card(s, x, y0, cw, ch, fill, fill);
          T(s, head, { x: x + 0.4, y: y0 + 0.3, w: cw - 0.8, h: 0.55, fontSize: 21, bold: true, color: hc });
          T(s, items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })),
            { x: x + 0.4, y: y0 + 1.0, w: cw - 0.8, h: ch - 1.15, fontSize: 19, color: HEX.ink, paraSpaceAfter: 12 });
        });
        break;
      }
      case "steps": {
        const n = sl.steps.length, cw = CW / n, cy = TOP + 1.2, d = 1.1;
        s.addShape(pres.shapes.LINE, { x: MX + cw / 2, y: cy + d / 2, w: CW - cw, h: 0, line: { color: HEX.line, width: 3 } });
        for (let i = 0; i < n; i++) {
          const [head, text] = sl.steps[i], cx = MX + cw * i + cw / 2, last = i === n - 1;
          const col = last ? HEX.orange : HEX.teal;
          s.addShape(pres.shapes.OVAL, { x: cx - d / 2, y: cy, w: d, h: d, fill: { color: col }, line: { color: HEX.white, width: 3 } });
          T(s, String(i + 1), { x: cx - d / 2, y: cy, w: d, h: d, fontSize: 30, bold: true, color: HEX.white, align: "center", valign: "middle" });
          T(s, head, { x: cx - cw / 2 + 0.1, y: cy + d + 0.3, w: cw - 0.2, h: 0.55, fontSize: 21, bold: true, color: last ? HEX.orange : HEX.navy, align: "center" });
          T(s, text, { x: cx - cw / 2 + 0.15, y: cy + d + 0.9, w: cw - 0.3, h: 1.3, fontSize: 16, color: HEX.slate, align: "center" });
        }
        break;
      }
      case "quiz": {
        const q = sl.questions, rh = Math.min(1.45, (4.9 - 0.15 * (q.length - 1)) / q.length);
        for (let i = 0; i < q.length; i++) {
          const y = TOP + 0.15 + i * (rh + 0.15);
          card(s, MX, y, CW, rh, i % 2 ? HEX.white : HEX.slateL, HEX.line);
          s.addShape(pres.shapes.OVAL, { x: MX + 0.3, y: y + rh / 2 - 0.3, w: 0.6, h: 0.6, fill: { color: HEX.navy }, line: { color: HEX.navy } });
          T(s, "Q" + (i + 1), { x: MX + 0.3, y: y + rh / 2 - 0.3, w: 0.6, h: 0.6, fontSize: 14, bold: true, color: HEX.white, align: "center", valign: "middle" });
          T(s, q[i], { x: MX + 1.15, y, w: CW - 1.4, h: rh, fontSize: 22, color: HEX.ink, valign: "middle" });
        }
        T(s, "정답은 발표자 노트에 있습니다", { x: MX, y: 6.5, w: CW, h: 0.35, fontSize: 12, color: HEX.muted, align: "right" });
        break;
      }
      case "summary": {
        const it = sl.items, rh = Math.min(0.78, (BOTTOM - TOP - 1.1) / it.length - 0.1);
        for (let i = 0; i < it.length; i++) {
          const y = TOP + 0.05 + i * (rh + 0.1);
          s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: y + 0.1, w: 1.3, h: rh - 0.2, rectRadius: 0.23, fill: { color: HEX.teal }, line: { color: HEX.teal } });
          T(s, it[i][0], { x: MX, y: y + 0.1, w: 1.3, h: rh - 0.2, fontSize: 15, bold: true, color: HEX.white, align: "center", valign: "middle" });
          T(s, it[i][1], { x: MX + 1.6, y, w: CW - 1.6, h: rh, fontSize: 22, color: HEX.navy, bold: true, valign: "middle" });
        }
        if (sl.diary) {
          const y = TOP + it.length * (rh + 0.1) + 0.2;
          card(s, MX, y, CW, 0.75, HEX.orangeL, HEX.orangeL);
          s.addImage({ data: await iconPng("NotebookPen", HEX.orange), x: MX + 0.3, y: y + 0.15, w: 0.45, h: 0.45 });
          T(s, sl.diary, { x: MX + 1.0, y, w: CW - 1.3, h: 0.75, fontSize: 16, color: HEX.orange, bold: true, valign: "middle" });
        }
        break;
      }
      case "code": {
        // 터미널 화면: code(명령) + out(결과, 선택) + points(오른쪽 설명, 선택)
        const lines = (sl.code || "").replace(/\n$/, "").split("\n"), outs = sl.out ? sl.out.replace(/\n$/, "").split("\n") : [];
        const hasPts = sl.points && sl.points.length, tw = hasPts ? 7.6 : CW;
        const availH = BOTTOM - TOP - (sl.callout ? 0.95 : 0.05);
        const vis = (l) => [...l].reduce((a, ch) => a + (ch.charCodeAt(0) > 0x2e80 ? 1.75 : 1), 0);
        const all = outs.length ? lines.concat([""], outs) : lines;
        let fsz = 17, total = all.length, lh = 0;
        for (const f of [17, 15, 14, 13, 12, 11]) {
          const cap = (tw - 0.65) * 72 / (f * 0.6);
          total = all.reduce((a, l) => a + Math.max(1, Math.ceil(vis(l) / cap)), 0);
          fsz = f; lh = f / 72 * 1.45;
          if (0.7 + total * lh * 1.05 <= availH) break;
        }
        const th = Math.min(availH, 0.7 + total * lh * 1.05), ty = TOP + Math.max(0, (availH - th) / 2);
        card(s, MX, ty, tw, th, "0F1E2E", "0F1E2E");
        ["FF5F57", "FEBC2E", "28C840"].forEach((c, i) => s.addShape(pres.shapes.OVAL, { x: MX + 0.25 + i * 0.28, y: ty + 0.2, w: 0.16, h: 0.16, fill: { color: c }, line: { color: c } }));
        T(s, sl.shell || "터미널", { x: MX + 1.2, y: ty + 0.12, w: tw - 1.5, h: 0.3, fontSize: 11, color: "7F95AA" });
        const runs = [];
        lines.forEach((l, i) => runs.push({ text: l === "" ? " " : l, options: { color: l.trim().startsWith("#") ? "7F95AA" : "E2E8F0", breakLine: true } }));
        if (outs.length) { runs.push({ text: " ", options: { breakLine: true } }); outs.forEach((l) => runs.push({ text: l === "" ? " " : l, options: { color: "8FD6A8", breakLine: true } })); }
        runs[runs.length - 1].options.breakLine = false;
        T(s, runs, { x: MX + 0.35, y: ty + 0.55, w: tw - 0.6, h: th - 0.7, fontSize: fsz, fontFace: "Consolas", lineSpacingMultiple: 1.05 });
        if (hasPts) {
          const px = MX + tw + 0.3, pw = CW - tw - 0.3, n = sl.points.length, ph = Math.min(1.25, (th - 0.15 * (n - 1)) / n);
          sl.points.forEach(([head, text], i) => {
            const y = ty + i * (ph + 0.15);
            card(s, px, y, pw, ph, i % 2 ? HEX.white : HEX.slateL, HEX.line);
            T(s, head, { x: px + 0.2, y: y + 0.1, w: pw - 0.4, h: 0.42, fontSize: 15, bold: true, color: HEX.tealD, fontFace: head.match(/^[-a-z0-9.:/ ]+$/i) ? "Consolas" : FONT });
            T(s, text, { x: px + 0.2, y: y + 0.5, w: pw - 0.4, h: ph - 0.58, fontSize: 14, color: HEX.slate });
          });
        }
        if (sl.callout) callout(s, Math.min(ty + th + 0.3, BOTTOM - 0.62), sl.callout, sl.callout_color || "teal");
        break;
      }
      default: throw new Error("unknown type " + sl.type);
    }
    let notes = sl.notes || "";
    if (sl.answers) notes = `[정답] ${sl.answers}\n\n${notes}`;
    if (notes) s.addNotes(notes);
  }
  await pres.writeFile({ fileName: outPath });
  if (SKILL) { const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js")); await applyTheme(outPath, THEME); }
  console.log("PPTX:", outPath);
})().catch((e) => { console.error(e); process.exit(1); });
