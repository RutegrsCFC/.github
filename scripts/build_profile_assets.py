"""Generate the SVG assets for the RutegrsCFC organization profile README.

Design notes
- Every SVG is drawn at 846px wide, the width GitHub gives an org README on desktop,
  so font sizes here are the sizes people actually see.
- Flat palette from the RCFC logo and F2026 deck: ink #1f252e, ivory text, and the
  logo coral used only for small marks. One serif for display, one sans for detail.
- Every block is its own panel, in a -dark (ink) and a -light (ivory paper) variant.
  The README picks one with GitHub's #gh-dark-mode-only / #gh-light-mode-only image
  fragments, which follow the viewer's GitHub theme setting. (<picture> with
  prefers-color-scheme follows the operating system instead, so it mismatches for
  anyone whose GitHub theme differs from their system theme.)
- Self-contained (no external fonts or images): GitHub shows README images through
  <img>, which blocks external resources.
- Motion is slow and quiet: staggered reveals, a coral hairline that draws itself,
  contour lines (the deck's background motif) that slowly change shape, and an
  activity ticker. All of it switches off under prefers-reduced-motion.
"""
import base64
import hashlib
import re
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
LOGO = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

W = 846
X0 = 56            # left text edge, shared by every asset
X1 = W - 56

SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif")
SERIF = ("'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, "
         "'Songti SC', 'Noto Serif SC', serif")
CJK = "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif"
CJK_SERIF = "'Songti SC', 'STSong', 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', serif"

EXPO = "cubic-bezier(0.16, 1, 0.3, 1)"

THEMES = {
    "dark": dict(
        panel="#1f252e", on_panel="#f6f3ee", on_panel_muted="#aeb1ba",
        ink="#f6f3ee", muted="#b4b8c2", subtle="#8a90a2",
        line="rgba(246,243,238,0.12)", contour="rgba(246,243,238,0.075)",
        coral="#ff6b63", panel_border="rgba(246,243,238,0.08)", btn_border="rgba(246,243,238,0.14)",
    ),
    "light": dict(
        panel="#f4f0e8", on_panel="#1f252e", on_panel_muted="#5a5f6c",
        ink="#1f252e", muted="#4c5262", subtle="#7c8296",
        line="rgba(31,37,46,0.12)", contour="rgba(31,37,46,0.085)",
        coral="#d9443f", panel_border="rgba(31,37,46,0.07)", btn_border="rgba(31,37,46,0.14)",
    ),
}


WRITTEN = {}


def write(name, svg):
    """Write the asset under a content-hashed name (hero-dark.1a2b3c4d.svg).

    GitHub serves README images from raw.githubusercontent.com with a 5-minute cache
    and drops query strings on the way, so a new file name is the only reliable way
    to make browsers fetch an updated image.
    """
    body = svg.strip() + "\n"
    stem = name[:-4]
    hashed = f"{stem}.{hashlib.sha1(body.encode()).hexdigest()[:8]}.svg"
    (OUT / hashed).write_text(body, encoding="utf-8")
    WRITTEN[stem] = hashed


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def style(extra=""):
    return f"""
  .sans {{ font-family: {SANS}; }}
  .serif {{ font-family: {SERIF}; }}
  .cjk {{ font-family: {CJK}; }}
  .cjks {{ font-family: {CJK_SERIF}; }}
  .rv {{ opacity: 0; animation: rv 1.6s {EXPO} forwards; }}
  @keyframes rv {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .dr {{ animation: dr 1.8s {EXPO} forwards; }}
  @keyframes dr {{ to {{ stroke-dashoffset: 0; }} }}
  .grow {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0); animation: grow 1.6s {EXPO} forwards; }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  {extra}
  @media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; }}
    .rv, .fi {{ opacity: 1; }} .grow {{ transform: none; }} .dr {{ stroke-dashoffset: 0; }}
  }}
"""


def d(t):
    return f'style="animation-delay:{t:.2f}s"'


def est(text, size, latin=0.5):
    return sum(size * (1.0 if ord(ch) > 0x2E80 else latin) for ch in text)


def wrap(text, size, width, latin=0.5):
    cjk = any(ord(ch) > 0x2E80 for ch in text)
    if cjk:  # balance line lengths so no line is left with one or two characters
        n = math.ceil(est(text, size, latin) / width)
        width = min(width, est(text, size, latin) / n + size * 1.5)
    units = list(text) if cjk else text.split(" ")
    lines, cur = [], ""
    for u in units:
        trial = (cur + u) if cjk else (cur + " " + u).strip()
        if cur and est(trial, size, latin) > width:
            lines.append(cur)
            cur = u
        else:
            cur = trial
    if cur:
        lines.append(cur)
    # never leave a lone CJK punctuation mark at the start of a line
    for i in range(1, len(lines)):
        if lines[i][:1] in "，。、；：":
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
    return lines


def tsp(lines, x, lh):
    return "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(s)}</tspan>' for i, s in enumerate(lines))


def ring(cx, cy, r, phase, k, sx=1.25, pts=60):
    out = []
    for i in range(pts):
        a = 2 * math.pi * i / pts
        w = (1 + 0.13 * math.sin(3 * a + phase + k * 0.21)
             + 0.07 * math.sin(5 * a - 1.6 * phase + k * 0.13)
             + 0.03 * math.sin(8 * a + 0.7 * phase + k * 0.37))
        out.append(f"{cx + r * w * math.cos(a) * sx:.1f},{cy + r * w * math.sin(a):.1f}")
    return "M" + " L".join(out) + "Z"


def contours(cx, cy, n, r0, step, stroke, dur=16, sx=1.25):
    """Concentric warped rings that slowly morph between two shapes (SMIL, works in <img>)."""
    paths = []
    for k in range(n):
        r = r0 + k * step
        a, b = ring(cx, cy, r, 0.4, k, sx), ring(cx, cy, r, 2.2, k, sx)
        paths.append(
            f'<path d="{a}"><animate attributeName="d" dur="{dur}s" repeatCount="indefinite" '
            f'values="{a};{b};{a}" keyTimes="0;0.5;1" calcMode="spline" '
            f'keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/></path>')
    return f'<g fill="none" stroke="{stroke}" stroke-width="1">{"".join(paths)}</g>'


def panel(H, body, t, label):
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<style>{style()}</style>
<defs><clipPath id="f"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<g clip-path="url(#f)">
  <rect width="{W}" height="{H}" fill="{t['panel']}"/>
  {body}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="{t['panel_border']}"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- hero
def hero(t):
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    H = 452
    cx, cy = 700, 236
    extra = """
  .fi { opacity: 0; animation: fi 3s ease .2s forwards; }
  @keyframes fi { to { opacity: 1; } }
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">Rutgers Chinese Finance Club — Bridging Western finance and Chinese markets. 连接西方金融与中国市场。</title>
<style>{style(extra)}</style>
<defs>
  <clipPath id="f"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <clipPath id="logo"><circle cx="{X0 + 18}" cy="66" r="18"/></clipPath>
  <radialGradient id="rf" cx="{cx / W:.3f}" cy="{cy / H:.3f}" r="0.6">
    <stop offset="0" stop-color="#fff"/><stop offset="0.6" stop-color="#fff" stop-opacity="0.75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="rm"><rect width="{W}" height="{H}" fill="url(#rf)"/></mask>
</defs>
<g clip-path="url(#f)">
  <rect width="{W}" height="{H}" fill="{t['panel']}"/>
  <g mask="url(#rm)" class="fi">
    {contours(cx, cy, 16, 22, 16, t['contour'])}
  </g>

  <g class="rv" {d(0.05)}>
    <circle cx="{X0 + 18}" cy="66" r="18.5" fill="#212730"/>
    <image x="{X0 - 1}" y="47" width="38" height="38" clip-path="url(#logo)" href="data:image/png;base64,{logo}" xlink:href="data:image/png;base64,{logo}"/>
    <text x="{X0 + 50}" y="71" class="sans" font-size="15" font-weight="600" letter-spacing="2.5" fill="{t['on_panel']}">RCFC</text>
    <text x="{X1}" y="71" text-anchor="end" class="sans" font-size="11.5" letter-spacing="2.4" fill="{t['on_panel_muted']}">FALL 2026 · NEW BRUNSWICK, NJ</text>
  </g>

  <text class="serif rv" x="{X0 - 3}" y="212" font-size="56" letter-spacing="-1.2" fill="{t['on_panel']}" {d(0.18)}>Bridging Western finance</text>
  <text class="serif rv" x="{X0 - 3}" y="276" font-size="56" letter-spacing="-1.2" fill="{t['on_panel']}" {d(0.30)}>and Chinese markets<tspan fill="{t['coral']}">.</tspan></text>
  <text class="cjks rv" x="{X0}" y="326" font-size="21" letter-spacing="7" fill="{t['on_panel']}" fill-opacity="0.78" {d(0.42)}>连接西方金融与中国市场</text>
  <path d="M{X0} 362 H{X0 + 40}" stroke="{t['coral']}" stroke-width="1.5" stroke-dasharray="40" stroke-dashoffset="40" class="dr" {d(0.7)}/>
  <text class="sans rv" x="{X0}" y="396" font-size="15" fill="{t['on_panel_muted']}" {d(0.55)}>Practical insight into China’s financial systems and tech sector, for Rutgers students.</text>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="{t['panel_border']}"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- activity ticker
# Only activities from the F2026 activity map. Keep out topics the club does not
# actually run (compliance, M&A, policy and the like).
ACTIVITIES = [
    ("Chinese AI Workshop", "国产大模型工坊"), ("Financial Engineering", "金融工程"),
    ("Student AI Toolkit", "学生 AI 福利与经验"), ("Alumni Stories", "校友分享"),
    ("Career Opportunities", "机会分享"), ("Company Tours", "行业参观"),
    ("Industry Expert Talks", "行业专家分享"), ("Equity Research", "股票分析"),
    ("Certificates", "证书"), ("Exchange Programs", "交换项目"),
]


def ticker(t):
    H = 64
    x, items = 0, []
    for en, zh in ACTIVITIES:
        ew = est(en, 15, 0.5)
        zw = est(zh, 12.5)
        # One <text> per item so the browser lays out the English, Chinese and dot with real
        # glyph widths; only the start of each item relies on the width estimate.
        items.append(
            f'<text x="{x:.0f}" y="0" class="serif" font-size="15" fill="{t["on_panel"]}">{en}'
            f'<tspan dx="10" class="cjk" font-size="12.5" fill="{t["on_panel_muted"]}">{zh}</tspan>'
            f'<tspan dx="22" dy="-3" class="sans" font-size="6.5" fill="{t["coral"]}">●</tspan></text>')
        x += ew + 10 + zw + 20 + 8 + 30
    period = round(x)
    row = "".join(items)
    extra = f"""
  .run {{ animation: run {period / 30:.0f}s linear infinite; }}
  @keyframes run {{ to {{ transform: translateX(-{period}px); }} }}
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Activities: {esc(', '.join(en for en, _ in ACTIVITIES))}">
<style>{style(extra)}</style>
<defs>
  <clipPath id="f"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <linearGradient id="tf" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.07" stop-color="#fff"/>
    <stop offset="0.93" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="tm"><rect width="{W}" height="{H}" fill="url(#tf)"/></mask>
</defs>
<g clip-path="url(#f)">
  <rect width="{W}" height="{H}" fill="{t['panel']}"/>
  <g mask="url(#tm)" class="rv" {d(0.6)}><g transform="translate(28 37)"><g class="run">
    <g>{row}</g><g transform="translate({period} 0)">{row}</g>
  </g></g></g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="{t['panel_border']}"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- mission & vision
MISSION = ("Bridge Western finance with Chinese market dynamics, giving Rutgers Business School "
           "students practical insight into China’s financial systems and tech sector to power "
           "their global careers.")
MISSION_ZH = "将西方金融与中国市场的动态相结合，为罗格斯商学院的学生提供关于中国金融体系和科技行业的实践性见解，助力他们在全球职业生涯中取得成功。"
VISION = "Preparing Rutgers students for global finance through cross-border education, insight and skills practice."
VISION_ZH = "通过跨境教育、专业洞见和技能实践，帮助罗格斯大学的学生为投身全球金融领域做好准备。"


def mission(t):
    col = 236
    width = X1 - col
    blocks, y, i = [], 12, 0
    for label, zh, en_text, zh_text in [("Mission", "使命", MISSION, MISSION_ZH),
                                        ("Vision", "愿景", VISION, VISION_ZH)]:
        en_l = wrap(en_text, 22, width, 0.47)
        zh_l = wrap(zh_text, 14.5, width)
        top = y
        en_y = top + 58
        zh_y = en_y + 34 * (len(en_l) - 1) + 40
        y = zh_y + 25 * (len(zh_l) - 1) + 44
        blocks.append(f"""
  {f'<rect x="{X0}" y="{top}" width="{X1 - X0}" height="1" fill="{t["line"]}" class="grow" {d(0.05 + i * 0.2)}/>' if i else ''}
  <g class="rv" {d(0.15 + i * 0.2)}>
    <circle cx="{X0 + 3}" cy="{top + 52}" r="3" fill="{t['coral']}"/>
    <text x="{X0 + 16}" y="{top + 58}" class="serif" font-size="20" fill="{t['ink']}">{label}</text>
    <text x="{X0 + 16}" y="{top + 84}" class="cjks" font-size="14" letter-spacing="4" fill="{t['subtle']}">{zh}</text>
    <text y="{en_y}" class="serif" font-size="22" fill="{t['ink']}">{tsp(en_l, col, 34)}</text>
    <text y="{zh_y}" class="cjk" font-size="14.5" fill="{t['muted']}">{tsp(zh_l, col, 25)}</text>
  </g>""")
        i += 1
    H = y + 8
    return panel(H, "".join(blocks), t, f"Mission: {esc(MISSION)} Vision: {esc(VISION)}")


# --------------------------------------------------------------------------- pillars
PILLARS = [
    ("FinTech &amp; AI", "金融科技", [("Chinese AI Workshop", "国产大模型工坊"), ("Financial Engineering", "金融工程"), ("Student AI Toolkit", "学生 AI 福利与经验")]),
    ("Networking", "交流会", [("Alumni Stories", "校友分享"), ("Company Tours", "行业参观"), ("Industry Expert Talks", "行业专家分享")]),
    ("Practice", "实践", [("Equity Research", "股票分析"), ("Certificates", "证书"), ("Exchange Programs", "交换项目")]),
]


OFF = 12


def pillars(t):
    gap = 28
    cw = (X1 - X0 - 2 * gap) / 3
    cols = []
    for i, (title, zh, items) in enumerate(PILLARS):
        x = X0 + i * (cw + gap)
        rows = []
        for j, (en, izh) in enumerate(items):
            y = 210 + j * 56
            rows.append(f"""
    <g class="rv" {d(0.45 + i * 0.12 + j * 0.08)}>
      <rect x="{x:.0f}" y="{y - 24}" width="{cw:.0f}" height="1" fill="{t['line']}"/>
      <text x="{x:.0f}" y="{y}" class="sans" font-size="14.5" fill="{t['ink']}">{en}</text>
      <text x="{x:.0f}" y="{y + 20}" class="cjk" font-size="12.5" fill="{t['subtle']}">{izh}</text>
    </g>""")
        cols.append(f"""
  <g class="rv" {d(0.2 + i * 0.12)}>
    <text x="{x:.0f}" y="104" class="sans" font-size="11.5" letter-spacing="2.5" fill="{t['coral']}">0{i + 1}</text>
    <text x="{x:.0f}" y="140" class="serif" font-size="26" letter-spacing="-0.3" fill="{t['ink']}">{title}</text>
    <text x="{x:.0f}" y="166" class="cjks" font-size="14" letter-spacing="3" fill="{t['subtle']}">{zh}</text>
  </g>{''.join(rows)}""")
    H = 210 + 2 * 56 + 56
    head = f"""<g class="rv" {d(0.05)}>
  <circle cx="{X0 + 3}" cy="{OFF + 46}" r="3" fill="{t['coral']}"/>
  <text x="{X0 + 16}" y="{OFF + 52}" class="serif" font-size="20" fill="{t['ink']}">What we do <tspan class="cjks" dx="8" font-size="14" letter-spacing="4" fill="{t['subtle']}">我们做什么</tspan></text>
</g>"""
    return panel(H + OFF, f'{head}<g transform="translate(0 {OFF})">{"".join(cols)}</g>', t,
                 "What we do. FinTech and AI: Chinese AI workshop, financial engineering, student AI toolkit. Networking: alumni stories, company tours, industry expert talks. Practice: equity research, certificates, exchange programs.")


# --------------------------------------------------------------------------- join
def join(t):
    H = 250
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Join membership. China-focused, bilingual, and open to every Rutgers student. No finance background required.">
<style>{style()}</style>
<defs>
  <clipPath id="f"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <linearGradient id="jf" x1="0" x2="1"><stop offset="0.35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="jm"><rect width="{W}" height="{H}" fill="url(#jf)"/></mask>
</defs>
<g clip-path="url(#f)">
  <rect width="{W}" height="{H}" fill="{t['panel']}"/>
  <g mask="url(#jm)">{contours(760, 230, 12, 30, 18, t['contour'], dur=20)}</g>
  <text class="sans rv" x="{X0}" y="66" font-size="11.5" letter-spacing="2.4" fill="{t['coral']}" {d(0.05)}>MEMBERSHIP · 会员招募</text>
  <text class="serif rv" x="{X0 - 2}" y="122" font-size="36" letter-spacing="-0.6" fill="{t['on_panel']}" {d(0.15)}>Join membership<tspan fill="{t['coral']}">.</tspan></text>
  <text class="cjks rv" x="{X0}" y="158" font-size="17" letter-spacing="3" fill="{t['on_panel']}" fill-opacity="0.75" {d(0.25)}>加入会员</text>
  <text class="sans rv" x="{X0}" y="198" font-size="14.5" fill="{t['on_panel_muted']}" {d(0.35)}>China-focused · Bilingual · Open to every Rutgers student, no finance background required.</text>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="{t['panel_border']}"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- buttons
def button(label, zh, width, t, primary=False):
    H = 44
    if primary:
        body = f'<rect width="{width}" height="{H}" rx="22" fill="#f05a52"/>'
        ink, sub, arrow = "#ffffff", "#ffffff", "#ffffff"
    else:
        body = (f'<rect width="{width}" height="{H}" rx="22" fill="{t["panel"]}"/>'
                f'<rect x="0.5" y="0.5" width="{width - 1}" height="{H - 1}" rx="21.5" fill="none" stroke="{t["btn_border"]}"/>')
        ink, sub, arrow = t["ink"], t["subtle"], t["coral"]
    extra = """
  .nudge { animation: nudge 3.2s cubic-bezier(0.65,0,0.35,1) 1.2s infinite; }
  @keyframes nudge { 0%, 70%, 100% { transform: none; } 82% { transform: translateX(4px); } }
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}" role="img" aria-label="{label}">
<style>{style(extra)}</style>
{body}
<text x="22" y="27.5" class="sans" font-size="14.5" font-weight="600" fill="{ink}">{label}<tspan class="cjk" dx="7" font-size="12.5" font-weight="400" fill="{sub}" fill-opacity="0.7">{zh}</tspan></text>
<g class="{'nudge' if primary else ''}"><path d="M{width - 34} 22 H{width - 22} M{width - 27} 17 L{width - 22} 22 L{width - 27} 27" fill="none" stroke="{arrow}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>"""


for name, t in THEMES.items():
    write(f"hero-{name}.svg", hero(t))
    write(f"ticker-{name}.svg", ticker(t))
    write(f"mission-{name}.svg", mission(t))
    write(f"pillars-{name}.svg", pillars(t))
    write(f"join-{name}.svg", join(t))
    write(f"btn-join-{name}.svg", button("Become a Member", "成为会员", 262, t, primary=True))
    write(f"btn-site-{name}.svg", button("Website", "官网", 158, t))
    write(f"btn-linkedin-{name}.svg", button("LinkedIn", "领英", 164, t))
# Point profile/README.md at the new file names.
readme = OUT.parent / "README.md"
if readme.exists():
    text = readme.read_text(encoding="utf-8")
    for stem, hashed in WRITTEN.items():
        text = re.sub(rf"assets/{re.escape(stem)}(\.[0-9a-f]{{8}})?\.svg(\?v=\d+)?", f"assets/{hashed}", text)
    readme.write_text(text, encoding="utf-8")
print("ok", len(WRITTEN), "assets")
