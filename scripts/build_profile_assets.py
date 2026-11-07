"""Generate the SVG assets for the RutegrsCFC organization profile README.

Every SVG is self-contained (no external fonts or images) because GitHub renders
README images through <img>, which blocks external resources. Text uses system
font stacks, so every layout leaves horizontal slack for metric differences.

Palette follows the RCFC F2026 deck and logo: midnight slate (#1f252e, #2a2f42,
#373d53), logo coral (#ff5757), ivory text, with periwinkle and rose as the
secondary accents used in the deck's activity map.
"""
import base64
import math
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
LOGO = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif")
SERIF = ("'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, "
         "'Songti SC', 'Noto Serif SC', 'Source Han Serif SC', serif")
CJK = ("'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', "
       "'Source Han Sans SC', sans-serif")
CJK_SERIF = "'Songti SC', 'STSong', 'Noto Serif SC', 'Source Han Serif SC', 'SimSun', serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

EXPO = "cubic-bezier(0.16, 1, 0.3, 1)"

# Banner colours (hero, ticker) are fixed: they read as dark panels on both GitHub themes.
NIGHT = "#1f252e"
NIGHT2 = "#2a2f42"
SLATE = "#373d53"
CORAL = "#ff5757"
CORAL_SOFT = "#ff7a70"
PERI = "#8f97e8"
IVORY = "#f6f3ee"

THEMES = {
    "dark": dict(
        canvas="#0d1117", card="#1a1f28", card2="#222837", border="rgba(246,243,238,0.08)",
        border2="rgba(246,243,238,0.16)", ink="#f6f3ee", muted="#c4c7d4", subtle="#8b91a7",
        coral="#ff6b63", peri="#9aa1ee", rose="#ef8a80", stone="#d6d3cc",
        contour="rgba(246,243,238,0.05)", glow="0.16",
    ),
    "light": dict(
        canvas="#ffffff", card="#f8f7f4", card2="#f1f0ec", border="rgba(31,37,46,0.10)",
        border2="rgba(31,37,46,0.20)", ink="#1f252e", muted="#474d60", subtle="#767c91",
        coral="#d83f3a", peri="#4f58b3", rose="#b8504a", stone="#5b5f6b",
        contour="rgba(31,37,46,0.06)", glow="0.08",
    ),
}

REDUCED = "@media (prefers-reduced-motion: reduce) { *, *::before { animation: none !important; } .rv { opacity: 1 !important; transform: none !important; } .dr { stroke-dashoffset: 0 !important; } }"


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def css(extra=""):
    return f"""
  .sans {{ font-family: {SANS}; }}
  .serif {{ font-family: {SERIF}; }}
  .cjk {{ font-family: {CJK}; }}
  .cjks {{ font-family: {CJK_SERIF}; }}
  .mono {{ font-family: {MONO}; }}
  .rv {{ opacity: 0; animation: rv 1.4s {EXPO} forwards; }}
  @keyframes rv {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: none; }} }}
  .dr {{ animation: dr 2.2s {EXPO} forwards; }}
  @keyframes dr {{ to {{ stroke-dashoffset: 0; }} }}
  {extra}
  {REDUCED}
"""


def delay(i, base=0.0, step=0.12):
    return f'style="animation-delay:{base + i * step:.2f}s"'


def est(text, size, latin=0.56):
    """Rough rendered width: CJK glyphs are 1em, latin about `latin` em."""
    return sum(size * (1.0 if ord(ch) > 0x2E80 else latin) for ch in text)


def wrap(text, size, width, latin=0.56):
    cjk = any(ord(ch) > 0x2E80 for ch in text)
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
    return lines


def tspans(lines, x, lh):
    return "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(s)}</tspan>' for i, s in enumerate(lines))


def contour_rings(cx, cy, n, r0, step, seed=0.0, pts=96):
    """Concentric, gently warped rings: the topographic motif from the deck backgrounds."""
    paths = []
    for k in range(n):
        r = r0 + k * step
        d = []
        for i in range(pts):
            a = 2 * math.pi * i / pts
            w = (1 + 0.07 * math.sin(3 * a + seed + k * 0.17)
                 + 0.04 * math.sin(5 * a - seed * 1.7 + k * 0.11)
                 + 0.02 * math.sin(9 * a + k * 0.3))
            x = cx + r * w * math.cos(a) * 1.18
            y = cy + r * w * math.sin(a)
            d.append(f"{x:.1f},{y:.1f}")
        paths.append("M" + " L".join(d) + " Z")
    return paths


# --------------------------------------------------------------------------- hero
def hero():
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    W, H = 1280, 600
    cx, cy = 1000, 300
    rings = contour_rings(cx, cy, 26, 26, 17, seed=0.6)
    ring_svg = "".join(f'<path d="{d}"/>' for d in rings)
    hi = rings[15]

    ax, ay, bx, by = 772, 448, 1166, 384     # New Brunswick -> Shanghai
    arc = f"M{ax},{ay} C{ax + 90},{ay - 300} {bx - 120},{by - 290} {bx},{by}"

    extra = f"""
  .turn {{ animation: turn 140s linear infinite; transform-box: view-box; transform-origin: {cx}px {cy}px; }}
  @keyframes turn {{ to {{ transform: rotate(360deg); }} }}
  .breathe {{ animation: breathe 14s ease-in-out infinite alternate; transform-box: view-box; transform-origin: {cx}px {cy}px; }}
  @keyframes breathe {{ from {{ transform: scale(1); }} to {{ transform: scale(1.045); }} }}
  .orbit {{ stroke-dasharray: 180 2600; animation: orbit 11s linear infinite; }}
  @keyframes orbit {{ to {{ stroke-dashoffset: -2780; }} }}
  .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 3.2s {EXPO} infinite; }}
  @keyframes ping {{ 0% {{ transform: scale(.4); opacity: .9; }} 100% {{ transform: scale(3.4); opacity: 0; }} }}
  .glowA {{ animation: glowA 18s ease-in-out infinite alternate; }}
  @keyframes glowA {{ from {{ transform: translate(0,0); }} to {{ transform: translate(-50px,26px); }} }}
  .fadeIn {{ opacity: 0; animation: fi 2s ease forwards; }}
  @keyframes fi {{ to {{ opacity: 1; }} }}
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Rutgers Chinese Finance Club · 罗格斯华人金融社团</title>
<desc id="d">Bridging Western finance and Chinese markets. RCFC, Fall 2026.</desc>
<style>{css(extra)}</style>
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
  <clipPath id="disc"><circle cx="128" cy="112" r="34"/></clipPath>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{SLATE}"/><stop offset="0.55" stop-color="{NIGHT2}"/><stop offset="1" stop-color="{NIGHT}"/>
  </linearGradient>
  <radialGradient id="gC" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CORAL}" stop-opacity="0.30"/><stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gP" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{PERI}" stop-opacity="0.20"/><stop offset="1" stop-color="{PERI}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="ringFade" cx="{cx / W:.3f}" cy="{cy / H:.3f}" r="0.62">
    <stop offset="0" stop-color="#fff"/><stop offset="0.7" stop-color="#fff" stop-opacity="0.6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="rm"><rect width="{W}" height="{H}" fill="url(#ringFade)"/></mask>
  <linearGradient id="arcG" gradientUnits="userSpaceOnUse" x1="{ax}" y1="0" x2="{bx}" y2="0">
    <stop offset="0" stop-color="{PERI}"/><stop offset="1" stop-color="{CORAL}"/>
  </linearGradient>
  <radialGradient id="comet" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#fff"/><stop offset="0.35" stop-color="{CORAL_SOFT}" stop-opacity="0.8"/><stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="veil" x1="0" x2="1">
    <stop offset="0" stop-color="{NIGHT2}" stop-opacity="0.92"/><stop offset="0.48" stop-color="{NIGHT2}" stop-opacity="0.55"/><stop offset="0.62" stop-color="{NIGHT2}" stop-opacity="0"/>
  </linearGradient>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g class="glowA"><ellipse cx="1060" cy="180" rx="420" ry="300" fill="url(#gC)"/></g>
  <ellipse cx="760" cy="560" rx="460" ry="220" fill="url(#gP)"/>

  <g mask="url(#rm)" class="fadeIn">
    <g class="breathe"><g class="turn" fill="none" stroke="rgba(246,243,238,0.11)" stroke-width="1">{ring_svg}</g></g>
    <path d="{hi}" fill="none" stroke="{CORAL}" stroke-opacity="0.55" stroke-width="1.4" stroke-linecap="round" class="orbit"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#veil)"/>

  <!-- the bridge: New Brunswick to Shanghai -->
  <path d="{arc}" fill="none" stroke="rgba(246,243,238,0.16)" stroke-width="1" stroke-dasharray="2 7"/>
  <path d="{arc}" fill="none" stroke="url(#arcG)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="760" stroke-dashoffset="760" class="dr" style="animation-delay:.9s; animation-duration:2.8s"/>
  <circle r="14" fill="url(#comet)" opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.85;1" dur="4.2s" begin="3s" repeatCount="indefinite"/>
    <animateMotion dur="4.2s" begin="3s" repeatCount="indefinite" path="{arc}" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines="0.45 0 0.25 1"/>
  </circle>
  <g>
    <circle cx="{ax}" cy="{ay}" r="5" fill="none" stroke="{PERI}" class="ping"/>
    <circle cx="{ax}" cy="{ay}" r="4.5" fill="{PERI}"/>
    <circle cx="{bx}" cy="{by}" r="5" fill="none" stroke="{CORAL}" class="ping" style="animation-delay:1.6s"/>
    <circle cx="{bx}" cy="{by}" r="4.5" fill="{CORAL}"/>
  </g>
  <g class="rv" {delay(0, 1.4)}>
    <text x="{ax}" y="{ay + 36}" text-anchor="middle" class="mono" font-size="13" letter-spacing="3" fill="{IVORY}" fill-opacity="0.85">NEW BRUNSWICK</text>
    <text x="{ax}" y="{ay + 58}" text-anchor="middle" class="mono" font-size="11" letter-spacing="1.5" fill="{IVORY}" fill-opacity="0.45">40.49°N  74.45°W</text>
    <text x="{bx}" y="{by + 36}" text-anchor="middle" class="mono" font-size="13" letter-spacing="3" fill="{IVORY}" fill-opacity="0.85">SHANGHAI</text>
    <text x="{bx}" y="{by + 58}" text-anchor="middle" class="mono" font-size="11" letter-spacing="1.5" fill="{IVORY}" fill-opacity="0.45">31.23°N  121.47°E</text>
  </g>

  <!-- identity -->
  <g class="rv" {delay(0, 0.05)}>
    <circle cx="128" cy="112" r="35" fill="{NIGHT}" stroke="rgba(246,243,238,0.18)"/>
    <image x="91" y="75" width="74" height="74" clip-path="url(#disc)" href="data:image/png;base64,{logo}" xlink:href="data:image/png;base64,{logo}"/>
    <text x="184" y="108" class="sans" font-size="21" font-weight="700" letter-spacing="1" fill="{IVORY}">RCFC <tspan font-weight="300">F2026</tspan></text>
    <text x="185" y="132" class="sans" font-size="11" letter-spacing="4.4" fill="{IVORY}" fill-opacity="0.6">RUTGERS CHINESE FINANCE CLUB</text>
  </g>

  <text class="serif rv" x="92" y="262" font-size="70" letter-spacing="-1" fill="{IVORY}" {delay(1, 0.05)}>Rutgers Chinese</text>
  <text class="serif rv" x="92" y="342" font-size="70" letter-spacing="-1" fill="{IVORY}" {delay(2, 0.05)}>Finance Club<tspan fill="{CORAL}">.</tspan></text>
  <text class="cjks rv" x="96" y="398" font-size="28" letter-spacing="10" fill="{IVORY}" fill-opacity="0.72" {delay(3, 0.05)}>罗格斯华人金融社团</text>
  <path d="M96 440 H160" stroke="{CORAL}" stroke-width="2" stroke-dasharray="64" stroke-dashoffset="64" class="dr" style="animation-delay:.7s"/>
  <text class="sans rv" x="96" y="484" font-size="22" fill="{IVORY}" fill-opacity="0.86" {delay(4, 0.05)}>Bridging Western finance and Chinese markets.</text>
  <text class="cjk rv" x="96" y="518" font-size="17" letter-spacing="3" fill="{IVORY}" fill-opacity="0.5" {delay(5, 0.05)}>连接西方金融与中国市场</text>

  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="27.5" fill="none" stroke="rgba(246,243,238,0.10)"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- ticker
TOPICS = [
    ("Chinese Financial Systems", "中国金融体系"), ("A-Shares &amp; Hong Kong", "A股与港股"),
    ("Chinese AI Models", "国产大模型"), ("FinTech", "金融科技"), ("Supply Chains", "供应链"),
    ("Cross-Border Investment", "跨境投资"), ("Policy &amp; Regulation", "政策与监管"),
    ("Equity Research", "股票研究"), ("Financial Engineering", "金融工程"),
    ("Exchange Programs", "交换项目"),
]


def ticker():
    size, zsize, H = 18, 15, 60
    x, items = 0, []
    for en, zh in TOPICS:
        plain = en.replace("&amp;", "&")
        en_w = est(plain, size, 0.6)
        zh_w = est(zh, zsize)
        items.append(
            f'<text x="{x:.0f}" y="37" font-size="{size}" class="serif" fill="{IVORY}">{en}</text>'
            f'<text x="{x + en_w + 12:.0f}" y="36" font-size="{zsize}" class="cjk" fill="{IVORY}" fill-opacity="0.5">{zh}</text>'
            f'<rect x="{x + en_w + zh_w + 40:.0f}" y="27" width="6" height="6" transform="rotate(45 {x + en_w + zh_w + 43:.0f} 30)" fill="{CORAL}"/>'
        )
        x += en_w + zh_w + 12 + 64
    period = round(x)
    row = "".join(items)
    extra = f"""
  .run {{ animation: run {period / 38:.1f}s linear infinite; }}
  @keyframes run {{ to {{ transform: translateX(-{period}px); }} }}
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 {H}" width="1280" height="{H}" role="img" aria-label="Focus areas: Chinese financial systems, A-shares and Hong Kong, Chinese AI models, FinTech, supply chains, cross-border investment, policy and regulation, equity research, financial engineering, exchange programs">
<style>{css(extra)}</style>
<defs>
  <clipPath id="c"><rect width="1280" height="{H}" rx="16"/></clipPath>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.08" stop-color="#fff"/>
    <stop offset="0.92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="1280" height="{H}" fill="url(#fade)"/></mask>
</defs>
<g clip-path="url(#c)">
  <rect width="1280" height="{H}" fill="{NIGHT}"/>
  <g mask="url(#m)"><g class="run">
    <g transform="translate(32 0)">{row}</g>
    <g transform="translate({32 + period} 0)">{row}</g>
  </g></g>
  <rect x="0.5" y="0.5" width="1279" height="{H - 1}" rx="15.5" fill="none" stroke="rgba(246,243,238,0.10)"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- section header
def header(num, en, zh, t):
    extra = """
  .grow { transform-box: fill-box; transform-origin: left center; transform: scaleX(0); animation: grow 1.8s cubic-bezier(0.16,1,0.3,1) .15s forwards; }
  @keyframes grow { to { transform: scaleX(1); } }
  @media (prefers-reduced-motion: reduce) { .grow { transform: none; } }
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 130" width="1280" height="130" role="img" aria-label="{en} · {zh}">
<style>{css(extra)}</style>
<g class="rv">
  <text x="0" y="40" class="mono" font-size="13" letter-spacing="4" fill="{t['coral']}">{num}</text>
  <text x="0" y="96" class="serif" font-size="44" letter-spacing="-0.6" fill="{t['ink']}">{en}<tspan class="cjks" dx="18" font-size="24" letter-spacing="4" fill="{t['subtle']}">{zh}</tspan></text>
</g>
<rect x="0" y="122" width="1280" height="1" fill="{t['border2']}" class="grow"/>
<rect x="0" y="121" width="56" height="3" fill="{t['coral']}" class="grow"/>
</svg>"""


# --------------------------------------------------------------------------- mission & vision
MISSION = ("Bridge Western finance with Chinese market dynamics, giving Rutgers Business School "
           "students practical insight into China’s financial systems and tech sector to power "
           "their global careers.")
MISSION_ZH = "将西方金融与中国市场的动态相结合，为罗格斯商学院的学生提供关于中国金融体系和科技行业的实践性见解，助力他们在全球职业生涯中取得成功。"
VISION = "Preparing Rutgers students for global finance through cross-border education, insight and skills practice."
VISION_ZH = "通过跨境教育、专业洞见和技能实践，帮助罗格斯大学的学生为投身全球金融领域做好准备。"


def mission(t):
    W, gap, H, pad = 610, 60, 440, 44
    inner = W - 2 * pad
    cards = []
    for i, (label, zh, en_text, zh_text, accent) in enumerate([
        ("MISSION", "使命", MISSION, MISSION_ZH, t["coral"]),
        ("VISION", "愿景", VISION, VISION_ZH, t["peri"]),
    ]):
        x = i * (W + gap)
        en_lines = wrap(en_text, 25, inner, 0.5)
        zh_lines = wrap(zh_text, 16, inner - 10)
        en_y = 150
        zh_y = en_y + 38 * (len(en_lines) - 1) + 56
        cards.append(f"""
  <g class="rv" {delay(i, 0.05, 0.18)}>
    <rect x="{x + 0.5}" y="0.5" width="{W - 1}" height="{H - 1}" rx="20" fill="{t['card']}" stroke="{t['border']}"/>
    <path d="{contour_rings(x + W - 40, 40, 1, 150, 0, seed=i)[0]}" fill="none" stroke="{t['contour']}"/>
    <path d="{contour_rings(x + W - 40, 40, 1, 110, 0, seed=i + 1)[0]}" fill="none" stroke="{t['contour']}"/>
    <path d="{contour_rings(x + W - 40, 40, 1, 70, 0, seed=i + 2)[0]}" fill="none" stroke="{t['contour']}"/>
    <rect x="{x + pad}" y="44" width="10" height="10" transform="rotate(45 {x + pad + 5} 49)" fill="{accent}"/>
    <text x="{x + pad + 26}" y="54" class="mono" font-size="13" letter-spacing="4" fill="{accent}">{label}</text>
    <text x="{x + pad + 26 + est(label, 13, 0.62) + 4 * len(label) + 10:.0f}" y="54" class="cjks" font-size="15" letter-spacing="3" fill="{t['subtle']}">{zh}</text>
    <path d="M{x + pad} 92 H{x + W - pad}" stroke="{t['border']}"/>
    <path d="M{x + pad} 92 H{x + pad + 120}" stroke="{accent}" stroke-width="1.5" stroke-dasharray="120" stroke-dashoffset="120" class="dr" style="animation-delay:{0.5 + i * 0.18:.2f}s"/>
    <text y="{en_y}" class="serif" font-size="25" fill="{t['ink']}">{tspans(en_lines, x + pad, 38)}</text>
    <text y="{zh_y}" class="cjk" font-size="16" fill="{t['subtle']}">{tspans(zh_lines, x + pad, 28)}</text>
  </g>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 {H}" width="1280" height="{H}" role="img" aria-label="Mission: {esc(MISSION)} Vision: {esc(VISION)}">
<style>{css()}</style>
{''.join(cards)}
</svg>"""


# --------------------------------------------------------------------------- pillars
ICONS = {
    # 40x40 stroked icons
    "chip": '<rect x="9" y="9" width="22" height="22" rx="4"/><rect x="15" y="15" width="10" height="10" rx="1.5"/>'
            '<path d="M15 4v5M20 4v5M25 4v5M15 31v5M20 31v5M25 31v5M4 15h5M4 20h5M4 25h5M31 15h5M31 20h5M31 25h5"/>',
    "nodes": '<circle cx="20" cy="9" r="4.5"/><circle cx="8" cy="31" r="4.5"/><circle cx="32" cy="31" r="4.5"/>'
             '<path d="M17.8 13 10.2 27M22.2 13l7.6 14M12.5 31h15"/>',
    "chart": '<path d="M5 35h30"/><path d="M8 29l8-9 6 5 11-13"/><path d="M27 12h6v6"/>',
}

PILLARS = [
    ("chip", "peri", "FinTech &amp; AI", "金融科技",
     [("Chinese AI Workshop", "国产大模型工坊"), ("Financial Engineering", "金融工程"),
      ("AI tools &amp; benefits for students", "学生 AI 福利与经验")]),
    ("nodes", "stone", "Networking", "交流会",
     [("Alumni Stories", "校友分享"), ("Company Tours", "行业参观"),
      ("Analysis by Industry Experts", "行业专家分享")]),
    ("chart", "rose", "Practice", "实践",
     [("Equity Research", "股票分析"), ("Certificates", "证书"),
      ("Exchange Programs", "交换项目")]),
]


def pillars(t):
    W, gap, H, pad = 400, 40, 470, 36
    cards = []
    for i, (icon, key, title, zh, items) in enumerate(PILLARS):
        x = i * (W + gap)
        accent = t[key]
        rows = []
        for j, (en, izh) in enumerate(items):
            y = 236 + j * 70
            rows.append(
                f'<path d="M{x + pad} {y - 30} H{x + W - pad}" stroke="{t["border"]}"/>'
                f'<text x="{x + pad}" y="{y}" class="sans" font-size="18" fill="{t["ink"]}">{en}</text>'
                f'<text x="{x + pad}" y="{y + 24}" class="cjk" font-size="14" fill="{t["subtle"]}">{izh}</text>'
                f'<text x="{x + W - pad}" y="{y}" text-anchor="end" class="mono" font-size="12" fill="{accent}">0{j + 1}</text>'
            )
        cards.append(f"""
  <g class="rv" {delay(i, 0.05, 0.15)}>
    <rect x="{x + 0.5}" y="0.5" width="{W - 1}" height="{H - 1}" rx="20" fill="{t['card']}" stroke="{t['border']}"/>
    <rect x="{x + pad}" y="0" width="64" height="3" fill="{accent}"/>
    <g transform="translate({x + pad} 44)" fill="none" stroke="{accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <g stroke-dasharray="220" stroke-dashoffset="220" class="dr" style="animation-delay:{0.35 + i * 0.15:.2f}s; animation-duration:2.6s">{ICONS[icon]}</g>
    </g>
    <text x="{x + W - pad}" y="66" text-anchor="end" class="mono" font-size="13" letter-spacing="3" fill="{t['subtle']}">0{i + 1}</text>
    <text x="{x + pad}" y="138" class="serif" font-size="34" letter-spacing="-0.4" fill="{t['ink']}">{title}</text>
    <text x="{x + pad}" y="168" class="cjks" font-size="17" letter-spacing="3" fill="{accent}">{zh}</text>
    {''.join(rows)}
  </g>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 {H}" width="1280" height="{H}" role="img" aria-label="What we do. FinTech and AI: Chinese AI workshop, financial engineering, AI tools for students. Networking: alumni stories, company tours, analysis by industry experts. Practice: equity research, certificates, exchange programs.">
<style>{css()}</style>
{''.join(cards)}
</svg>"""


# --------------------------------------------------------------------------- why
WHY = [
    ("China-focused", "聚焦中国", ["Chinese finance, tech and", "regulation, a gap at RBS today"]),
    ("East ↔ West", "连接东西方", ["Connecting both sides,", "not one market"]),
    ("English · 中文", "中英双语", ["Programming in", "both languages"]),
    ("Open to all", "面向全体", ["Any Rutgers student,", "no finance background needed"]),
]


def why(t):
    W, gap, H, pad = 290, 40, 210, 28
    tiles = []
    for i, (big, zh, sub) in enumerate(WHY):
        x = i * (W + gap)
        tiles.append(f"""
  <g class="rv" {delay(i, 0.05, 0.1)}>
    <rect x="{x + 0.5}" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{t['card2']}" stroke="{t['border']}"/>
    <text x="{x + pad}" y="46" class="cjks" font-size="14" letter-spacing="3" fill="{t['coral']}">{zh}</text>
    <text x="{x + pad}" y="100" class="serif" font-size="31" letter-spacing="-0.4" fill="{t['ink']}">{big}</text>
    <path d="M{x + pad} 126 H{x + pad + 28}" stroke="{t['coral']}" stroke-width="1.5"/>
    <text y="160" class="sans" font-size="15.5" fill="{t['muted']}">{tspans(sub, x + pad, 22)}</text>
  </g>""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 {H}" width="1280" height="{H}" role="img" aria-label="Why RCFC: China-focused, covering Chinese finance, tech and regulation, a gap at RBS today. East and West: connecting both sides. Bilingual programming in English and Chinese. Open to all Rutgers students, no finance background needed.">
<style>{css()}</style>
{''.join(tiles)}
</svg>"""


# --------------------------------------------------------------------------- buttons
def button(label, zh, width, t, primary=False, icon=None):
    H = 60
    if primary:
        body = (f'<rect width="{width}" height="{H}" rx="30" fill="url(#bg)"/>'
                f'<rect x="-140" width="90" height="{H}" fill="url(#shine)" class="shine"/>')
        ring = f'<rect x="0.5" y="0.5" width="{width - 1}" height="{H - 1}" rx="29.5" fill="none" stroke="rgba(255,255,255,0.25)"/>'
        ink, sub = "#ffffff", "rgba(255,255,255,0.75)"
    else:
        body = f'<rect x="0.5" y="0.5" width="{width - 1}" height="{H - 1}" rx="29.5" fill="{t["card"]}" stroke="{t["border2"]}"/>'
        ring, ink, sub = "", t["ink"], t["subtle"]
    icons = {
        "plus": f'<g transform="translate(26 19)" fill="none" stroke="{ink}" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="10"/><path d="M11 6.5v9M6.5 11h9"/></g>',
        "globe": f'<g transform="translate(26 19)" fill="none" stroke="{ink}" stroke-width="1.6"><circle cx="11" cy="11" r="10"/><path d="M1 11h20M11 1c3 3 4 6.5 4 10s-1 7-4 10c-3-3-4-6.5-4-10s1-7 4-10z"/></g>',
        "in": (f'<g transform="translate(26 19)"><rect width="22" height="22" rx="5" fill="{ink}"/>'
               f'<text x="11" y="16.5" text-anchor="middle" class="sans" font-size="13" font-weight="800" fill="{t["card"]}">in</text></g>'),
    }
    extra = """
  .shine { animation: shine 5s cubic-bezier(0.65,0,0.35,1) 1s infinite; }
  @keyframes shine { 0% { transform: translateX(0); } 45%, 100% { transform: translateX(560px); } }
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}" role="img" aria-label="{label}">
<style>{css(extra)}</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff6a5f"/><stop offset="1" stop-color="#e2453f"/></linearGradient>
  <linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="pill"><rect width="{width}" height="{H}" rx="30"/></clipPath>
</defs>
<g clip-path="url(#pill)">{body}</g>{ring}
{icons[icon]}
<text x="60" y="37" class="sans" font-size="18" font-weight="600" fill="{ink}">{label} <tspan class="cjk" font-size="14" font-weight="400" fill="{sub}">{zh}</tspan></text>
<text x="{width - 30}" y="37" text-anchor="end" class="sans" font-size="18" fill="{ink}">→</text>
</svg>"""


# --------------------------------------------------------------------------- footer
def footer(t):
    W, H = 1280, 220
    rings = contour_rings(640, 300, 14, 120, 20, seed=2.1)
    ring_svg = "".join(f'<path d="{d}"/>' for d in rings)
    extra = """
  .drift { animation: drift 30s ease-in-out infinite alternate; }
  @keyframes drift { from { transform: translateX(-24px); } to { transform: translateX(24px); } }
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rutgers Chinese Finance Club, RCFC F2026, New Brunswick, New Jersey.">
<style>{css(extra)}</style>
<defs>
  <linearGradient id="fx" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="fm"><rect width="{W}" height="{H}" fill="url(#fx)"/></mask>
</defs>
<g mask="url(#fm)"><g class="drift" fill="none" stroke="{t['contour']}">{ring_svg}</g></g>
<rect x="633" y="40" width="14" height="14" transform="rotate(45 640 47)" fill="none" stroke="{t['coral']}" stroke-width="1.5"/>
<rect x="637" y="44" width="6" height="6" transform="rotate(45 640 47)" fill="{t['coral']}"/>
<text x="640" y="116" text-anchor="middle" class="serif rv" font-size="30" fill="{t['ink']}">Rutgers Chinese Finance Club</text>
<text x="640" y="150" text-anchor="middle" class="cjks rv" font-size="16" letter-spacing="8" fill="{t['subtle']}" style="animation-delay:.12s">罗格斯华人金融社团</text>
<text x="640" y="196" text-anchor="middle" class="mono rv" font-size="12" letter-spacing="3" fill="{t['subtle']}" style="animation-delay:.24s">RCFC · F2026 · NEW BRUNSWICK, NJ</text>
</svg>"""


write("hero.svg", hero())
write("ticker.svg", ticker())
for name, t in THEMES.items():
    write(f"h-mission-{name}.svg", header("01 — ABOUT", "Mission &amp; Vision", "使命与愿景", t))
    write(f"h-pillars-{name}.svg", header("02 — WHAT WE DO", "Three Pillars", "三大板块", t))
    write(f"h-why-{name}.svg", header("03 — WHY RCFC", "Why Us", "为什么选择我们", t))
    write(f"h-join-{name}.svg", header("04 — JOIN", "Become a Member", "成为会员", t))
    write(f"mission-{name}.svg", mission(t))
    write(f"pillars-{name}.svg", pillars(t))
    write(f"why-{name}.svg", why(t))
    write(f"btn-join-{name}.svg", button("Become a Member", "成为会员", 330, t, primary=True, icon="plus"))
    write(f"btn-site-{name}.svg", button("Website", "官网", 220, t, icon="globe"))
    write(f"btn-linkedin-{name}.svg", button("LinkedIn", "领英", 220, t, icon="in"))
    write(f"footer-{name}.svg", footer(t))
print("ok", len(list(OUT.iterdir())), "files")
