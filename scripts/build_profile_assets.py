"""Generate the SVG assets for the RutegrsCFC organization profile README.

Every SVG is self-contained (no external fonts or images) because GitHub renders
README images through <img>, which blocks external resources. Text uses system
font stacks, so every layout leaves horizontal slack for metric differences.
"""
import base64
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
LOGO = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif")
CJK = ("'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', "
       "'Source Han Sans SC', sans-serif")
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(
        canvas="#0d1117", surface="#0e0e12", surface2="#141419", border="rgba(255,255,255,0.09)",
        border2="rgba(255,255,255,0.16)", ink="#f4f4f6", muted="#c3c3cd", subtle="#8a8a97",
        brand="#cc0033", brand_ink="#ff3d63", gold="#e2b45c", grid="rgba(255,255,255,0.05)",
        icon_bg="rgba(204,0,51,0.12)",
    ),
    "light": dict(
        canvas="#ffffff", surface="#ffffff", surface2="#f6f7f9", border="rgba(13,17,23,0.10)",
        border2="rgba(13,17,23,0.18)", ink="#0b0b10", muted="#3d3d48", subtle="#6a6a76",
        brand="#cc0033", brand_ink="#c8002f", gold="#9a6b12", grid="rgba(13,17,23,0.06)",
        icon_bg="rgba(204,0,51,0.07)",
    ),
}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")


def base_style(t, extra=""):
    return f"""
  .sans {{ font-family: {SANS}; }}
  .cjk {{ font-family: {CJK}; }}
  .mono {{ font-family: {MONO}; }}
  {extra}
  {REDUCED}
"""


# --------------------------------------------------------------------------- hero
def hero():
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    t = THEMES["dark"]
    # Market-line path across the bottom: deterministic, gently rising.
    pts = [(0, 470), (70, 455), (130, 462), (190, 438), (250, 446), (320, 420), (380, 431),
           (440, 404), (500, 414), (560, 392), (630, 399), (690, 372), (750, 383), (810, 360),
           (880, 368), (940, 341), (1000, 352), (1060, 326), (1120, 333), (1180, 309), (1280, 296)]
    line = "M" + " L".join(f"{x},{y}" for x, y in pts)
    area = line + " L1280,560 L0,560 Z"
    candles = ""
    for i, (x, y) in enumerate(pts[1:-1]):
        up = i % 3 != 1
        h = 14 + (i * 7) % 16
        c = t["brand_ink"] if up else t["subtle"]
        candles += (f'<line x1="{x}" y1="{y-h-8}" x2="{x}" y2="{y+h+8}" stroke="{c}" stroke-opacity="0.35" stroke-width="1.5"/>'
                    f'<rect x="{x-4}" y="{y-h}" width="8" height="{2*h}" rx="1.5" fill="{c}" fill-opacity="0.28"/>')
    css = base_style(t, f"""
  .drift {{ animation: drift 16s ease-in-out infinite alternate; transform-origin: center; }}
  @keyframes drift {{ from {{ transform: translate(0,0) scale(1); }} to {{ transform: translate(-60px,30px) scale(1.12); }} }}
  .drift2 {{ animation: drift2 20s ease-in-out infinite alternate; }}
  @keyframes drift2 {{ from {{ transform: translate(0,0); }} to {{ transform: translate(70px,-20px); }} }}
  .spin {{ animation: spin 60s linear infinite; transform-origin: 250px 270px; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .draw {{ stroke-dasharray: 1700; stroke-dashoffset: 1700; animation: draw 3.2s cubic-bezier(0.22,1,0.28,1) 0.3s forwards; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  .fade {{ opacity: 0; animation: fade 1.4s ease 1.2s forwards; }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  .rise {{ opacity: 0; animation: rise 1s cubic-bezier(0.22,1,0.28,1) forwards; }}
  .d1 {{ animation-delay: .1s; }} .d2 {{ animation-delay: .25s; }} .d3 {{ animation-delay: .4s; }} .d4 {{ animation-delay: .55s; }} .d5 {{ animation-delay: .7s; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ .draw {{ stroke-dashoffset: 0; }} .fade, .rise {{ opacity: 1; }} }}
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 560" width="1280" height="560" role="img" aria-labelledby="t d">
<title id="t">Rutgers Chinese Finance Club · 罗格斯华人金融社团</title>
<desc id="d">Bridging Cultures, Advancing Careers. Founding cohort, Fall 2026.</desc>
<style>{css}</style>
<defs>
  <clipPath id="frame"><rect width="1280" height="560" rx="28"/></clipPath>
  <clipPath id="disc"><circle cx="250" cy="270" r="146"/></clipPath>
  <radialGradient id="glowR" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#cc0033" stop-opacity="0.55"/>
    <stop offset="0.45" stop-color="#cc0033" stop-opacity="0.16"/>
    <stop offset="1" stop-color="#cc0033" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowG" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#e2b45c" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#e2b45c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="badgeGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0.55" stop-color="#cc0033" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#cc0033" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="lineG" x1="0" x2="1">
    <stop offset="0" stop-color="#cc0033" stop-opacity="0.2"/>
    <stop offset="0.6" stop-color="#ff3d63"/>
    <stop offset="1" stop-color="#e2b45c"/>
  </linearGradient>
  <linearGradient id="areaG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#cc0033" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#cc0033" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{t['grid']}" stroke-width="1"/>
  </pattern>
  <radialGradient id="gridFade" cx="0.55" cy="0.4" r="0.75">
    <stop offset="0" stop-color="#fff" stop-opacity="1"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="gridMask"><rect width="1280" height="560" fill="url(#gridFade)"/></mask>
</defs>
<g clip-path="url(#frame)">
  <rect width="1280" height="560" fill="#060608"/>
  <rect width="1280" height="560" fill="url(#grid)" mask="url(#gridMask)"/>
  <g class="drift"><ellipse cx="1080" cy="80" rx="520" ry="360" fill="url(#glowR)"/></g>
  <g class="drift2"><ellipse cx="160" cy="560" rx="420" ry="260" fill="url(#glowG)"/></g>
  <g>{candles}</g>
  <path d="{area}" fill="url(#areaG)"/>
  <path d="{line}" fill="none" stroke="url(#lineG)" stroke-opacity="0.35" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="{line}" fill="none" stroke="url(#lineG)" stroke-width="2.5" stroke-linejoin="round" class="draw"/>
  <circle cx="1280" cy="296" r="5" fill="#e2b45c"/>

  <!-- badge -->
  <circle cx="250" cy="270" r="230" fill="url(#badgeGlow)"/>
  <circle cx="250" cy="270" r="182" fill="none" stroke="rgba(255,255,255,0.10)"/>
  <g class="spin"><circle cx="250" cy="270" r="166" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="1.5" stroke-dasharray="2 10"/>
    <circle cx="250" cy="104" r="4" fill="#ff3d63"/></g>
  <image x="104" y="124" width="292" height="292" clip-path="url(#disc)" href="data:image/png;base64,{logo}" xlink:href="data:image/png;base64,{logo}"/>
  <circle cx="250" cy="270" r="146" fill="none" stroke="rgba(255,255,255,0.14)"/>

  <!-- copy -->
  <g>
    <rect x="470" y="98" width="500" height="40" rx="20" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.14)"/>
    <circle cx="494" cy="118" r="5" fill="#ff3d63" class="pulse"/>
    <text x="512" y="124" class="mono" font-size="16" letter-spacing="2.4" fill="#e2b45c">FOUNDING COHORT · FALL 2026</text>
    <text x="944" y="124" text-anchor="end" class="cjk" font-size="16" letter-spacing="1" fill="#c3c3cd">创始成员</text>
  </g>
  <text x="466" y="222" class="sans" font-size="72" font-weight="700" letter-spacing="-2" fill="#f4f4f6">Rutgers Chinese</text>
  <text x="466" y="302" class="sans" font-size="72" font-weight="700" letter-spacing="-2" fill="#f4f4f6">Finance Club<tspan fill="#ff3d63">.</tspan></text>
  <text x="470" y="358" class="cjk" font-size="34" font-weight="500" letter-spacing="8" fill="#c3c3cd">罗格斯华人金融社团</text>
  <g>
    <rect x="470" y="388" width="36" height="2" fill="#cc0033"/>
    <text x="520" y="396" class="sans" font-size="22" fill="#8a8a97">Bridging Cultures, Advancing Careers</text>
    <text x="520" y="430" class="cjk" font-size="19" letter-spacing="3" fill="#7a7a86">跨越文化 · 驱动未来</text>
  </g>
  <text x="1236" y="62" text-anchor="end" class="mono" font-size="14" letter-spacing="3" fill="#8a8a97">EST. 2026</text>
  <rect x="0.5" y="0.5" width="1279" height="559" rx="27.5" fill="none" stroke="rgba(255,255,255,0.10)"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- ticker
TOPICS = [
    ("Equity Research", "股票研究"), ("Investment Banking", "投资银行"),
    ("Bloomberg Terminal", "彭博终端"), ("China A-Shares", "中国 A 股"),
    ("Private Equity", "私募股权"), ("Quantitative Finance", "量化金融"),
    ("Cross-Border M&A", "跨境并购"), ("ESG", "ESG"), ("Venture Capital", "风险投资"),
    ("Risk Management", "风险管理"),
]


def est(text, size, latin=0.58):
    w = 0
    for ch in text:
        w += size * (1.0 if ord(ch) > 0x2E80 else latin)
    return w


def ticker():
    size, zsize = 20, 17
    x, items = 0, []
    arrows = ["▲", "▲", "▼", "▲", "▲", "▼", "▲", "▲", "▼", "▲"]
    for (en, zh), arrow in zip(TOPICS, arrows):
        color = "#ff3d63" if arrow == "▲" else "#8a8a97"
        en_w = est(en, size, 0.6)
        zh_w = est(zh, zsize) if zh != en else 0
        items.append(
            f'<text x="{x:.0f}" y="40" font-size="{size}" class="sans" fill="#f4f4f6" font-weight="600">{en.replace("&", "&amp;")}</text>'
            + (f'<text x="{x + en_w + 14:.0f}" y="40" font-size="{zsize}" class="cjk" fill="#8a8a97">{zh}</text>' if zh_w else "")
            + f'<text x="{x + en_w + (zh_w + 28 if zh_w else 14):.0f}" y="39" font-size="12" class="sans" fill="{color}">{arrow}</text>'
        )
        x += en_w + (zh_w + 28 if zh_w else 14) + 64
    period = round(x)
    row = "".join(items)
    dur = period / 55
    css = base_style(THEMES["dark"], f"""
  .run {{ animation: run {dur:.1f}s linear infinite; }}
  @keyframes run {{ to {{ transform: translateX(-{period}px); }} }}
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 64" width="1280" height="64" role="img" aria-label="Focus areas: Equity Research, Investment Banking, Bloomberg Terminal, China A-Shares, Private Equity, Quantitative Finance, Cross-Border M&amp;A, ESG, Venture Capital, Risk Management">
<style>{css}</style>
<defs>
  <clipPath id="c"><rect width="1280" height="64" rx="16"/></clipPath>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.07" stop-color="#fff"/>
    <stop offset="0.93" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="m"><rect width="1280" height="64" fill="url(#fade)"/></mask>
</defs>
<g clip-path="url(#c)">
  <rect width="1280" height="64" fill="#060608"/>
  <g mask="url(#m)"><g class="run">
    <g transform="translate(24 0)">{row}</g>
    <g transform="translate({24 + period} 0)">{row}</g>
  </g></g>
  <rect x="0.5" y="0.5" width="1279" height="63" rx="15.5" fill="none" stroke="rgba(255,255,255,0.10)"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- section header
def header(num, en, zh, t):
    css = base_style(t, """
  .grow { transform-origin: 640px 0; animation: grow 1.6s cubic-bezier(0.22,1,0.28,1) forwards; transform: scaleX(0.2); }
  @keyframes grow { to { transform: scaleX(1); } }
  @media (prefers-reduced-motion: reduce) { .grow { transform: none; } }
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 150" width="1280" height="150" role="img" aria-label="{en} · {zh}">
<style>{css}</style>
<defs><linearGradient id="h" x1="0" x2="1">
  <stop offset="0" stop-color="{t['border2']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['border2']}"/>
  <stop offset="1" stop-color="{t['border2']}" stop-opacity="0"/></linearGradient></defs>
<g class="grow"><rect x="140" y="28" width="1000" height="1" fill="url(#h)"/></g>
<rect x="633" y="21" width="14" height="14" transform="rotate(45 640 28)" fill="{t['canvas']}" stroke="{t['brand']}" stroke-width="1.5"/>
<rect x="637" y="25" width="6" height="6" transform="rotate(45 640 28)" fill="{t['brand']}"/>
<text x="640" y="72" text-anchor="middle" class="mono" font-size="15" letter-spacing="4" fill="{t['brand_ink']}">{num}</text>
<text x="640" y="118" text-anchor="middle" class="sans" font-size="42" font-weight="700" letter-spacing="-1" fill="{t['ink']}">{en} <tspan class="cjk" font-size="30" font-weight="500" letter-spacing="2" fill="{t['subtle']}">{zh}</tspan></text>
</svg>"""


# --------------------------------------------------------------------------- program cards
ICONS = {
    # 48x48 icons, stroked
    "terminal": """<rect x="4" y="8" width="40" height="28" rx="4"/><path d="M16 42h16M24 36v6"/>
      <path d="M12 28v-6M12 18v-2M20 28v-10M28 28v-4M28 20v-4M36 28v-12" stroke-linecap="round"/>""",
    "mic": """<rect x="17" y="4" width="14" height="24" rx="7"/><path d="M10 22a14 14 0 0 0 28 0M24 36v8M16 44h16" stroke-linecap="round"/>""",
    "network": """<circle cx="24" cy="10" r="5"/><circle cx="9" cy="36" r="5"/><circle cx="39" cy="36" r="5"/>
      <circle cx="24" cy="27" r="3.5"/><path d="M24 15v8.5M21.2 29.2 13 33.5M26.8 29.2 35 33.5M13 33l8-21M35 33l-8-21" stroke-linecap="round"/>""",
}

PROGRAMS = [
    ("01", "terminal", ["Skill Advancement", "Workshops"], "技能进阶工作坊",
     ["Bloomberg Terminal, BMC and ESG", "certifications, and hands-on work", "with AI tools in finance."],
     ["彭博终端、BMC 与 ESG 认证，", "以及 AI 工具在金融中的实操。"]),
    ("02", "mic", ["Engage with", "Industry Leaders"], "对话行业领袖",
     ["Frontline practitioners on how the", "work actually happens — markets,", "careers, and current trends."],
     ["一线从业者讲真实的工作方式——", "市场、职业路径与当下趋势。"]),
    ("03", "network", ["Build an Exclusive", "Community"], "构建精英社群",
     ["Peers to job-hunt and study with,", "from across finance, economics,", "and business."],
     ["一起求职和学习的同伴，", "来自金融、经济与商科。"]),
]


def programs(t):
    W, H, gap = 400, 520, 40
    cards = []
    for i, (num, icon, title, zh_title, desc, zh_desc) in enumerate(PROGRAMS):
        x = i * (W + gap)
        tl = "".join(f'<tspan x="{x+36}" dy="{0 if j == 0 else 38}">{s}</tspan>' for j, s in enumerate(title))
        dl = "".join(f'<tspan x="{x+36}" dy="{0 if j == 0 else 30}">{s}</tspan>' for j, s in enumerate(desc))
        zl = "".join(f'<tspan x="{x+36}" dy="{0 if j == 0 else 28}">{s}</tspan>' for j, s in enumerate(zh_desc))
        cards.append(f"""
  <g>
    <rect x="{x+0.5}" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="{t['surface']}" stroke="{t['border']}"/>
    <rect x="{x+36}" y="0" width="120" height="2" fill="url(#accent)" class="sweep"/>
    <rect x="{x+36}" y="40" width="72" height="72" rx="16" fill="{t['icon_bg']}" stroke="{t['border']}"/>
    <g transform="translate({x+48} 52)" fill="none" stroke="{t['brand_ink']}" stroke-width="2.2" stroke-linejoin="round">{ICONS[icon]}</g>
    <text x="{x+W-36}" y="68" text-anchor="end" class="mono" font-size="15" letter-spacing="3" fill="{t['subtle']}">{num}</text>
    <text y="168" class="sans" font-size="29" font-weight="700" letter-spacing="-0.6" fill="{t['ink']}">{tl}</text>
    <text x="{x+36}" y="246" class="cjk" font-size="21" font-weight="500" letter-spacing="2" fill="{t['brand_ink']}">{zh_title}</text>
    <rect x="{x+36}" y="270" width="{W-72}" height="1" fill="{t['border']}"/>
    <text y="314" class="sans" font-size="19" fill="{t['muted']}">{dl}</text>
    <text y="430" class="cjk" font-size="17" fill="{t['subtle']}">{zl}</text>
  </g>""")
    css = base_style(t, """
  .card { opacity: 0; animation: up 1s cubic-bezier(0.22,1,0.28,1) forwards; }
  .c0 { animation-delay: .05s; } .c1 { animation-delay: .2s; } .c2 { animation-delay: .35s; }
  @keyframes up { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
  .sweep { animation: sweep 6s ease-in-out infinite; }
  @keyframes sweep { 0%,100% { transform: translateX(0); } 50% { transform: translateX(208px); } }
  @media (prefers-reduced-motion: reduce) { .card { opacity: 1; } }
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 520" width="1280" height="520" role="img" aria-label="Programs: Skill Advancement Workshops; Engage with Industry Leaders; Build an Exclusive Community">
<style>{css}</style>
<defs><linearGradient id="accent" x1="0" x2="1">
  <stop offset="0" stop-color="#cc0033" stop-opacity="0"/><stop offset="0.5" stop-color="#ff3d63"/>
  <stop offset="1" stop-color="#cc0033" stop-opacity="0"/></linearGradient></defs>
{''.join(cards)}
</svg>"""


# --------------------------------------------------------------------------- facts
FACTS = [
    ("users", "Open to all", ["All Rutgers students", "面向所有罗格斯学生"]),
    ("spark", "No prerequisites", ["No finance background required", "无需金融背景"]),
    ("lang", "English · 中文", ["Content in both languages", "中英双语内容"]),
    ("flag", "Fall 2026", ["Founding cohort", "创始成员招募中"]),
]
FACT_ICONS = {
    "users": '<circle cx="12" cy="9" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/><path d="M17 4.6a4 4 0 0 1 0 8M20 14.5c2.4 1 4 3.2 4 6.5" stroke-linecap="round"/>',
    "spark": '<path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l4 4M15 15l4 4M19 5l-4 4M9 15l-4 4" stroke-linecap="round"/>',
    "lang": '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="M6 15l3-7 3 7M7 13h4M15 9h5M17.5 9v6M15 15h5" stroke-linecap="round"/>',
    "flag": '<path d="M5 22V3M5 4h12l-2 4 2 4H5" stroke-linecap="round"/>',
}


def facts(t):
    W, gap, H = 290, 40, 200
    tiles = []
    for i, (icon, big, sub) in enumerate(FACTS):
        x = i * (W + gap)
        big_cls = "sans" if "中" not in big else "sans"
        tiles.append(f"""
  <g>
    <rect x="{x+0.5}" y="0.5" width="{W-1}" height="{H-1}" rx="20" fill="{t['surface2']}" stroke="{t['border']}"/>
    <g transform="translate({x+28} 28)" fill="none" stroke="{t['brand_ink']}" stroke-width="1.8" stroke-linejoin="round">{FACT_ICONS[icon]}</g>
    <text x="{x+28}" y="106" class="{big_cls}" font-size="30" font-weight="700" letter-spacing="-0.6" fill="{t['ink']}">{big}</text>
    <text x="{x+28}" y="144" class="sans" font-size="17" fill="{t['muted']}">{sub[0]}</text>
    <text x="{x+28}" y="172" class="cjk" font-size="15" fill="{t['subtle']}">{sub[1]}</text>
  </g>""")
    css = base_style(t, """
  .tile { opacity: 0; animation: up .9s cubic-bezier(0.22,1,0.28,1) forwards; }
  .t0 { animation-delay: .05s; } .t1 { animation-delay: .15s; } .t2 { animation-delay: .25s; } .t3 { animation-delay: .35s; }
  @keyframes up { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: reduce) { .tile { opacity: 1; } }
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 200" width="1280" height="200" role="img" aria-label="Open to all Rutgers students. No finance background required. Content in English and Chinese. Founding cohort, Fall 2026.">
<style>{css}</style>
{''.join(tiles)}
</svg>"""


# --------------------------------------------------------------------------- buttons
def button(label, zh, width, t, primary=False, icon=None):
    H = 60
    if primary:
        bg = f'<rect x="0" y="0" width="{width}" height="{H}" rx="30" fill="url(#bg)"/>'
        ink, sub = "#ffffff", "rgba(255,255,255,0.78)"
        stroke = '<rect x="0.5" y="0.5" width="{w}" height="59" rx="29.5" fill="none" stroke="rgba(255,255,255,0.22)"/>'.format(w=width - 1)
        shine = f'<rect x="-120" y="0" width="80" height="{H}" fill="url(#shine)" class="shine"/>'
    else:
        bg = f'<rect x="0.5" y="0.5" width="{width-1}" height="{H-1}" rx="29.5" fill="{t["surface"]}" stroke="{t["border2"]}"/>'
        ink, sub = t["ink"], t["subtle"]
        stroke, shine = "", ""
    icon_svg = ""
    tx = 28
    if icon == "globe":
        icon_svg = f'<g transform="translate(26 19)" fill="none" stroke="{ink}" stroke-width="1.7"><circle cx="11" cy="11" r="10"/><path d="M1 11h20M11 1c3 3 4 6.5 4 10s-1 7-4 10c-3-3-4-6.5-4-10s1-7 4-10z"/></g>'
        tx = 60
    elif icon == "in":
        icon_svg = (f'<g transform="translate(26 19)"><rect width="22" height="22" rx="5" fill="{ink}"/>'
                    f'<text x="11" y="17" text-anchor="middle" class="sans" font-size="14" font-weight="800" fill="{t["surface"] if not primary else "#cc0033"}">in</text></g>')
        tx = 60
    elif icon == "plus":
        icon_svg = f'<g transform="translate(26 19)" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="10"/><path d="M11 6v10M6 11h10"/></g>'
        tx = 60
    css = base_style(t, """
  .shine { animation: shine 4.5s ease-in-out infinite; }
  @keyframes shine { 0%, 60% { transform: translateX(0); } 100% { transform: translateX(520px); } }
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}" role="img" aria-label="{label}">
<style>{css}</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e30a3d"/><stop offset="1" stop-color="#b3002d"/></linearGradient>
  <linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <clipPath id="pill"><rect width="{width}" height="{H}" rx="30"/></clipPath>
</defs>
<g clip-path="url(#pill)">{bg}{shine}</g>{stroke}
{icon_svg}
<text x="{tx}" y="37" class="sans" font-size="19" font-weight="600" letter-spacing="-0.2" fill="{ink}">{label} <tspan class="cjk" font-size="15" font-weight="400" fill="{sub}">{zh}</tspan></text>
<text x="{width-30}" y="37" text-anchor="end" class="sans" font-size="19" fill="{ink}">→</text>
</svg>"""


# --------------------------------------------------------------------------- footer
def footer(t):
    pts = [(0, 120), (80, 112), (150, 118), (230, 100), (300, 106), (380, 88), (450, 96),
           (520, 76), (600, 84), (680, 64), (760, 72), (840, 52), (920, 60), (1000, 42),
           (1080, 50), (1160, 30), (1280, 24)]
    line = "M" + " L".join(f"{x},{y}" for x, y in pts)
    css = base_style(t, """
  .draw { stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 3s cubic-bezier(0.22,1,0.28,1) forwards; }
  @keyframes draw { to { stroke-dashoffset: 0; } }
  .blink { animation: blink 2.4s ease-in-out infinite; }
  @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: .2; } }
  @media (prefers-reduced-motion: reduce) { .draw { stroke-dashoffset: 0; } }
""")
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 300" width="1280" height="300" role="img" aria-label="Bridging Cultures, Advancing Careers: Empowering Global Excellence in Finance.">
<style>{css}</style>
<defs><linearGradient id="l" x1="0" x2="1">
  <stop offset="0" stop-color="{t['brand']}" stop-opacity="0"/><stop offset="0.5" stop-color="{t['brand_ink']}" stop-opacity="0.7"/>
  <stop offset="1" stop-color="{t['gold']}"/></linearGradient></defs>
<path d="{line}" fill="none" stroke="url(#l)" stroke-opacity="0.35" stroke-width="2"/>
<path d="{line}" fill="none" stroke="url(#l)" stroke-width="2" class="draw"/>
<circle cx="1276" cy="24" r="4" fill="{t['gold']}" class="blink"/>
<text x="640" y="176" text-anchor="middle" class="sans" font-size="34" font-weight="700" letter-spacing="-0.8" fill="{t['ink']}">Bridging Cultures, Advancing Careers</text>
<text x="640" y="214" text-anchor="middle" class="sans" font-size="19" fill="{t['muted']}">Empowering Global Excellence in Finance.</text>
<text x="640" y="248" text-anchor="middle" class="cjk" font-size="17" letter-spacing="4" fill="{t['subtle']}">跨越文化 · 驱动未来</text>
<text x="640" y="288" text-anchor="middle" class="mono" font-size="12" letter-spacing="3" fill="{t['subtle']}">© 2026 RUTGERS CHINESE FINANCE CLUB · <tspan class="cjk" letter-spacing="1">罗格斯华人金融社团</tspan></text>
</svg>"""


write("hero.svg", hero())
write("ticker.svg", ticker())
for name, t in THEMES.items():
    write(f"h-programs-{name}.svg", header("01 · WHAT WE DO", "Programs &amp; Events", "项目与活动", t))
    write(f"h-who-{name}.svg", header("02 · WHO IT'S FOR", "Built for Rutgers", "为罗格斯学生而建", t))
    write(f"h-join-{name}.svg", header("03 · JOIN US", "Become a Member", "成为会员", t))
    write(f"programs-{name}.svg", programs(t))
    write(f"facts-{name}.svg", facts(t))
    write(f"btn-join-{name}.svg", button("Become a Member", "成为会员", 340, t, primary=True, icon="plus"))
    write(f"btn-site-{name}.svg", button("Visit Website", "官网", 260, t, icon="globe"))
    write(f"btn-linkedin-{name}.svg", button("LinkedIn", "领英", 220, t, icon="in"))
    write(f"footer-{name}.svg", footer(t))
print("ok", sorted(p.name for p in OUT.iterdir()))
