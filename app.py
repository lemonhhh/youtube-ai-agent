import streamlit as st
import requests
import re

st.set_page_config(
    page_title="🍋 YouTube 笔记助手",
    page_icon="🍋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body { background-color: #FAFAF5 !important; }
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stSidebar"] { background-color: #FAFAF5 !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="collapsedControl"] { display: none !important; }
footer, #MainMenu { visibility: hidden !important; }

input, input[type="text"], input[type="password"] {
  background-color: #FFFFFF !important;
  background: #FFFFFF !important;
  color: #1a1a1a !important;
  border: 1.5px solid #FFE082 !important;
  border-radius: 8px !important;
  caret-color: #1a1a1a !important;
  box-shadow: none !important;
  outline: none !important;
}
input:focus {
  border-color: #FBC02D !important;
  box-shadow: 0 0 0 2px rgba(251,192,45,0.2) !important;
  outline: none !important;
}
input::placeholder { color: #bbb !important; }
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] > div > div {
  background-color: #FFFFFF !important;
  border-radius: 8px !important;
  border: none !important;
  box-shadow: none !important;
}
[data-testid="stTextInput"] button,
[data-testid="stTextInput"] [data-testid="baseButton-secondary"] { display: none !important; }
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p { color: #555 !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* ── Radio 选择器 ── */
[data-testid="stRadio"] { background: transparent !important; }
[data-testid="stRadio"] label { color: #555 !important; font-weight: 600 !important; font-size: 0.85rem !important; }
[data-testid="stRadio"] > div { gap: 0.6rem !important; }
[data-testid="stRadio"] > div > label {
  background: #FFFFFF !important;
  border: 1.5px solid #FFE082 !important;
  border-radius: 10px !important;
  padding: 0.5rem 1.2rem !important;
  cursor: pointer !important;
  transition: all 0.15s !important;
  color: #555 !important;
  font-weight: 600 !important;
}
[data-testid="stRadio"] > div > label:has(input:checked) {
  background: #FDD835 !important;
  border-color: #FBC02D !important;
  color: #1a1a1a !important;
}
/* 隐藏 radio 圆形指示器 */
[data-testid="stRadio"] > div > label > div:first-child,
[data-testid="stRadio"] span[data-testid="stMarkdownContainer"] ~ div,
[data-testid="stRadio"] input[type="radio"] { display: none !important; }

.stButton > button {
  background: linear-gradient(135deg, #FDD835, #FBC02D) !important;
  color: #1a1a1a !important; font-weight: 700 !important; border: none !important;
  border-radius: 10px !important; font-size: 1rem !important;
  box-shadow: 0 3px 12px rgba(253,216,53,0.4) !important;
  transition: all 0.2s !important; padding: 0.55rem 2rem !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 5px 18px rgba(253,216,53,0.55) !important; }

.stDownloadButton > button {
  background: linear-gradient(135deg, #FDD835, #FBC02D) !important;
  color: #1a1a1a !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; box-shadow: 0 2px 10px rgba(253,216,53,0.35) !important;
  width: 100% !important; transition: all 0.2s !important;
}
.stDownloadButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(253,216,53,0.5) !important; }

[data-baseweb="tab-list"] {
  background: #FFF9C4 !important; border-radius: 12px !important; padding: 6px !important; gap: 6px !important;
}
[data-baseweb="tab"] {
  background: transparent !important; border-radius: 8px !important; color: #777 !important;
  font-weight: 600 !important; border: none !important; padding: 0.5rem 1.2rem !important;
  font-size: 0.9rem !important; white-space: nowrap !important;
}
[aria-selected="true"] { background: #FDD835 !important; color: #1a1a1a !important; }
[data-baseweb="tab-panel"] {
  background: #FFFFFF !important; border: 1.5px solid #FFE082 !important;
  border-radius: 10px !important; padding: 1.4rem !important; margin-top: 8px !important;
}

[data-testid="stStatus"],
[data-testid="stStatus"] > div,
[data-testid="stStatus"] > div > div,
[data-testid="stStatusWidget"],
[data-testid="stStatusWidget"] > div,
.stStatus, .stStatus > div { background: #FFFDE7 !important; background-color: #FFFDE7 !important; }
[data-testid="stStatus"] { border: 1.5px solid #FFE082 !important; border-left: 4px solid #FDD835 !important; border-radius: 10px !important; }
[data-testid="stStatus"] *, [data-testid="stStatusWidget"] * { color: #444 !important; background-color: transparent !important; }
[data-testid="stStatus"] [data-testid="stVerticalBlock"],
[data-testid="stStatus"] [data-testid="stVerticalBlockBorderWrapper"] { background: #FFFDE7 !important; background-color: #FFFDE7 !important; }

details { background: #FFFDE7 !important; border-radius: 8px !important; border: 1px solid #FFE082 !important; }
summary { color: #555 !important; }
[data-testid="stAlert"] { background: #FFFDE7 !important; border: 1px solid #FFE082 !important; border-radius: 8px !important; }
[data-testid="stAlert"] p { color: #555 !important; }

textarea { background: #FFFDE7 !important; color: #1a1a1a !important; border: 1.5px solid #FFE082 !important; border-radius: 8px !important; box-shadow: none !important; }
[data-testid="stTextArea"] > div,
[data-testid="stTextArea"] > div > div { background: #FFFDE7 !important; border: none !important; box-shadow: none !important; }
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] label p { color: #555 !important; font-size: 0.85rem !important; }

[data-testid="stCode"], pre { background: #FFFDE7 !important; border: 1px solid #FFE082 !important; border-radius: 8px !important; }
code { color: #5D4037 !important; }
hr { border-color: #FFE082 !important; }

.lemon-header {
  background: linear-gradient(135deg, #FDD835 0%, #FFEE58 55%, #FFF176 100%);
  border-radius: 18px; padding: 2rem 2rem 1.6rem; margin-bottom: 1.4rem;
  position: relative; overflow: hidden; box-shadow: 0 4px 20px rgba(253,216,53,0.35); text-align: center;
}
.lemon-header::before {
  content: '🍋'; position: absolute; right: 1.5rem; top: 0.8rem;
  font-size: 5rem; opacity: 0.15; transform: rotate(15deg); pointer-events: none;
}
.lemon-header h1 { font-size: 1.8rem; font-weight: 800; color: #1a1a1a; margin: 0 0 0.3rem; }
.lemon-header p { color: #555; margin: 0; font-size: 0.88rem; }

.section-label { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #F9A825; margin-bottom: 0.5rem; }
.tip { font-size: 0.75rem; color: #aaa; margin-top: 0.2rem; }
.tip a { color: #FBC02D; text-decoration: none; }
.model-badge {
  display: inline-block; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.05em;
  padding: 0.15rem 0.55rem; border-radius: 20px; margin-left: 0.4rem; vertical-align: middle;
}
.badge-groq { background: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }
.badge-gemini { background: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }
.block-container { max-width: 720px !important; padding: 1.5rem 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── 工具函数 ─────────────────────────────────────────────────
def extract_video_id(url):
    m = re.search(r'(?:v=|\/|be\/|embed\/)([0-9A-Za-z_-]{11})', url)
    return m.group(1) if m else None

LEMON_SVG = '<svg width="22" height="22" viewBox="0 0 26 26" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0"><ellipse cx="13" cy="13.5" rx="10" ry="8.5" fill="#FDD835"/><ellipse cx="12.5" cy="13" rx="7.5" ry="6.2" fill="none" stroke="#FBC02D" stroke-width="0.7" opacity="0.5"/><path d="M12.5 5.5 Q10 2 8.5 4.5 Q10 3 12.5 5.5Z" fill="#7CB342"/><path d="M13.5 5.2 Q16 1.5 17.5 4 Q16 2.8 13.5 5.2Z" fill="#558B2F"/></svg>'

FORMULA_SPAN = (
    'font-family:var(--fm);display:inline-block;'
    'background:linear-gradient(135deg,#FFFDE7,#FEFCE8);'
    'border:1px solid #FFF59D;border-left:3px solid #FDD835;'
    'border-radius:6px;padding:.25em .7em;margin:.2em 0;'
    'font-size:.91em;color:#1a1a1a;line-height:1.6;'
)

def md_to_lemon_html(md_text, video_url_str, video_id_str):
    lines = md_text.strip().split('\n')
    doc_title = "YouTube 笔记"
    for i, line in enumerate(lines):
        if line.startswith('# '):
            doc_title = line[2:].strip(); lines.pop(i); break

    sections, current_section, current_lines = [], None, []
    def flush():
        if current_section is not None: sections.append((current_section, current_lines[:]))
        elif current_lines: sections.append((None, current_lines[:]))
    for line in lines:
        if line.startswith('## '): flush(); current_section = line[3:].strip(); current_lines = []
        else: current_lines.append(line)
    flush()

    def inline(t):
        # ── 第一步：用占位符保护行内 $...$ 公式，防止被后续正则（* ** ` 等）破坏
        math_slots = []
        def stash_math(m):
            math_slots.append(m.group(0))
            return f'\x00M{len(math_slots)-1}\x00'
        t = re.sub(r'\$[^$\n]+?\$', stash_math, t)

        # ── 第二步：处理其他 Markdown 语法
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         t)
        t = re.sub(r'`([^`]+)`',     r'<code>\1</code>',     t)
        t = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', t)

        # ── 第三步：还原行内公式（KaTeX auto-render 会在浏览器端渲染 $...$）
        for i, m in enumerate(math_slots):
            t = t.replace(f'\x00M{i}\x00', m)
        return t

    def render_block(blines):
        html, in_ul, in_ol, in_pre, pre_buf = [], False, False, False, []
        in_math = False
        math_buf = []

        def close_lists():
            nonlocal in_ul, in_ol
            if in_ul: html.append('</ul>'); in_ul = False
            if in_ol: html.append('</ol>'); in_ol = False

        for line in blines:
            # ── 多行 $$ 块（开头单独一行 $$，结尾单独一行 $$）
            if line.strip() == '$$':
                if not in_math:
                    close_lists(); in_math = True; math_buf = []
                else:
                    in_math = False
                    inner = ' '.join(math_buf)
                    html.append('<div class="formula-block">$$' + inner + '$$</div>')
                continue
            if in_math:
                math_buf.append(line.strip()); continue

            # ── 整行 $$公式$$（同一行开始和结束）
            stripped = line.strip()
            if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4:
                close_lists()
                inner = stripped[2:-2].strip()
                html.append('<div class="formula-block">$$' + inner + '$$</div>')
                continue

            # ── ``` 代码块（回退给没用 LaTeX 的情况）
            if stripped == '```' or stripped.startswith('```'):
                if not in_pre: close_lists(); in_pre = True; pre_buf = []
                else: in_pre = False; html.append('<div class="formula-block">' + chr(10).join(pre_buf) + '</div>')
                continue
            if in_pre: pre_buf.append(line); continue
            if not line.strip(): close_lists(); continue
            if line.startswith('#### '):
                close_lists()
                html.append(f'<h4 style="font-size:.95rem;font-weight:700;color:#4a4a4a;margin:1rem 0 .4rem;padding-left:.6rem;border-left:2px solid #FDD835">{inline(line[5:].strip())}</h4>')
            elif line.startswith('### '): close_lists(); html.append(f'<h3>{inline(line[4:].strip())}</h3>')
            elif line.startswith('> '): close_lists(); html.append(f'<div class="callout insight"><div class="callout-title">💡 要点</div><p>{inline(line[2:].strip())}</p></div>')
            elif re.match(r'^[\-\*] ', line):
                if in_ol: html.append('</ol>'); in_ol = False
                if not in_ul: html.append('<ul>'); in_ul = True
                html.append(f'<li>{inline(line[2:].strip())}</li>')
            elif re.match(r'^\d+\. ', line):
                if in_ul: html.append('</ul>'); in_ul = False
                if not in_ol: html.append('<ol>'); in_ol = True
                html.append(f'<li>{inline(re.sub(r"^\d+\. ", "", line).strip())}</li>')
            else: close_lists(); html.append(f'<p>{inline(line.strip())}</p>')
        close_lists()
        return '\n'.join(html)

    cards = ""
    for title, slines in sections:
        inner = render_block(slines)
        if title: cards += f'\n  <article class="section-card"><h2 class="section-title">{LEMON_SVG}{title}</h2>{inner}</article>'
        elif inner.strip(): cards += f'\n  <article class="section-card">{inner}</article>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_title}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}], throwOnError:false}});"></script>
  <style>
    :root{{--y50:#FFFDE7;--y100:#FFF9C4;--y200:#FFF59D;--y300:#FFF176;--y400:#FFEE58;--y500:#FDD835;--y600:#FBC02D;--y700:#F9A825;--leaf:#7CB342;--leafd:#558B2F;--t1:#1a1a1a;--t2:#4a4a4a;--tm:#777;--bg:#FAFAF5;--card:#fff;--bd:#E8E4D8;--md:0 4px 14px rgba(0,0,0,.06);--lg:0 10px 30px rgba(0,0,0,.08);--rlg:20px;--rmd:14px;--rsm:8px;--fb:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;--fm:"SF Mono","Fira Code",Consolas,monospace}}
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    html{{scroll-behavior:smooth}}
    body{{font-family:var(--fb);color:var(--t1);background:var(--bg);line-height:1.8;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
    body::before{{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 20% 0%,rgba(253,216,53,.07) 0%,transparent 50%),radial-gradient(ellipse at 80% 100%,rgba(253,216,53,.05) 0%,transparent 50%);pointer-events:none;z-index:0}}
    .corner-lemon{{position:fixed;top:-30px;right:-20px;z-index:1;opacity:.18;transform:rotate(25deg);pointer-events:none}}
    .page-header{{position:relative;z-index:2;background:linear-gradient(135deg,var(--y500) 0%,var(--y400) 40%,var(--y300) 100%);padding:3.5rem 2rem 3rem;text-align:center;overflow:hidden}}
    .page-header::before{{content:'';position:absolute;inset:0;background:radial-gradient(circle at 15% 80%,rgba(255,255,255,.25) 0%,transparent 40%),radial-gradient(circle at 85% 20%,rgba(255,255,255,.2) 0%,transparent 35%);pointer-events:none}}
    .page-header::after{{content:'';position:absolute;bottom:-2px;left:0;right:0;height:40px;background:var(--bg);border-radius:50% 50% 0 0/100% 100% 0 0}}
    .header-tag{{display:inline-block;background:rgba(255,255,255,.35);backdrop-filter:blur(4px);padding:.3rem 1rem;border-radius:20px;font-size:.82rem;font-weight:600;letter-spacing:.08em;color:var(--t1);margin-bottom:1rem;text-transform:uppercase}}
    .page-header h1{{position:relative;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:800;color:var(--t1);line-height:1.35;max-width:700px;margin:0 auto}}
    .header-sub{{position:relative;font-size:.9rem;color:var(--t2);margin-top:.8rem}}
    .header-sub a{{color:var(--t2)}}
    main{{position:relative;z-index:2;max-width:820px;margin:0 auto;padding:2rem 1.5rem 4rem}}
    .section-card{{background:var(--card);border-radius:var(--rlg);box-shadow:var(--md);padding:2.2rem 2.4rem;margin-bottom:2rem;border:1px solid rgba(232,228,216,.6);transition:box-shadow .3s ease;opacity:0;transform:translateY(18px);animation:fadeUp .5s ease forwards}}
    .section-card:hover{{box-shadow:var(--lg)}}
    .section-card:nth-child(1){{animation-delay:.05s}}.section-card:nth-child(2){{animation-delay:.1s}}.section-card:nth-child(3){{animation-delay:.15s}}.section-card:nth-child(4){{animation-delay:.2s}}.section-card:nth-child(5){{animation-delay:.25s}}.section-card:nth-child(6){{animation-delay:.3s}}.section-card:nth-child(n+7){{animation-delay:.35s}}
    @keyframes fadeUp{{to{{opacity:1;transform:translateY(0)}}}}
    .section-title{{display:flex;align-items:center;gap:.7rem;font-size:1.45rem;font-weight:700;color:var(--t1);margin-bottom:1.5rem;padding-bottom:.8rem;border-bottom:2px solid var(--y200)}}
    h3{{font-size:1.12rem;font-weight:700;color:var(--t1);margin:1.8rem 0 .8rem;padding-left:.8rem;border-left:3px solid var(--y500)}}
    h3:first-of-type{{margin-top:.3rem}}
    p{{margin-bottom:.9rem;color:var(--t2);line-height:1.85}}
    strong{{color:var(--t1);font-weight:650}}
    ul,ol{{margin:.6rem 0 1rem 1.4rem;color:var(--t2)}}
    li{{margin-bottom:.45rem;line-height:1.75}}
    li::marker{{color:var(--y600)}}
    code{{font-family:var(--fm);background:var(--y100);padding:.15em .45em;border-radius:4px;font-size:.88em;color:#6D4C00}}
    .formula-block{{background:linear-gradient(135deg,var(--y50),#FEFCE8);border:1px solid var(--y200);border-left:4px solid var(--y500);border-radius:var(--rsm);padding:1.2rem 1.6rem;margin:1rem 0;color:var(--t1);line-height:2;text-align:center;overflow-x:auto}}
    .callout{{background:var(--y50);border-radius:var(--rsm);padding:1rem 1.3rem;margin:1rem 0;border:1px solid var(--y200)}}
    .callout.insight{{border-left:4px solid var(--y600)}}
    .callout-title{{font-weight:700;font-size:.88rem;color:var(--t1);margin-bottom:.4rem;display:flex;align-items:center;gap:.4rem}}
    .callout p{{margin-bottom:.4rem;font-size:.92rem}}
    .page-footer{{position:relative;z-index:2;text-align:center;padding:3rem 1rem 2rem;color:var(--tm);font-size:.82rem}}
    .footer-lemon{{opacity:.06;margin:0 auto 1rem;display:block}}
    @media(max-width:640px){{.section-card{{padding:1.4rem 1.2rem}}.page-header{{padding:2.5rem 1rem 2rem}}}}
  </style>
</head>
<body>
<div class="corner-lemon" aria-hidden="true">
  <svg width="220" height="220" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="110" cy="105" rx="85" ry="72" fill="#FDD835"/>
    <ellipse cx="110" cy="105" rx="85" ry="72" fill="url(#cg)"/>
    <ellipse cx="100" cy="100" rx="68" ry="56" fill="none" stroke="#FBC02D" stroke-width="1" opacity="0.4"/>
    <path d="M108 34 Q95 18 85 30 Q92 22 108 34Z" fill="#7CB342"/>
    <path d="M112 33 Q125 15 135 28 Q128 20 112 33Z" fill="#558B2F"/>
    <line x1="110" y1="50" x2="110" y2="160" stroke="#FBC02D" stroke-width="0.8" opacity="0.3"/>
    <line x1="50" y1="105" x2="170" y2="105" stroke="#FBC02D" stroke-width="0.8" opacity="0.3"/>
    <defs><radialGradient id="cg" cx="40%" cy="35%"><stop offset="0%" stop-color="#FFEE58" stop-opacity="0.6"/><stop offset="100%" stop-color="#FDD835" stop-opacity="0"/></radialGradient></defs>
  </svg>
</div>
<header class="page-header">
  <div class="header-tag">📝 YouTube 视频笔记</div>
  <h1>{doc_title}</h1>
  <p class="header-sub"><a href="{video_url_str}" target="_blank">▶ 观看原视频</a></p>
</header>
<main>{cards}</main>
<footer class="page-footer">
  <svg class="footer-lemon" width="120" height="100" viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <ellipse cx="60" cy="55" rx="50" ry="40" fill="#FDD835"/>
    <path d="M59 16 Q50 4 44 12 Q50 6 59 16Z" fill="#7CB342"/>
    <path d="M62 15 Q72 2 78 11 Q72 5 62 15Z" fill="#558B2F"/>
    <line x1="60" y1="25" x2="60" y2="85" stroke="#FBC02D" stroke-width="0.6" opacity="0.35"/>
    <line x1="20" y1="55" x2="100" y2="55" stroke="#FBC02D" stroke-width="0.6" opacity="0.35"/>
  </svg>
  <p>🍋 YouTube AI 笔记生成</p>
</footer>
</body>
</html>"""


# ─── Prompt ──────────────────────────────────────────────────
# ★ 修改点 1：新增【核心任务：公式主动提取与转换】章节，
#   并将原公式说明从"突出重点"移入该专项章节，大幅强化 AI 的公式识别能力。
SYSTEM_PROMPT = """你是一个极其严谨的知识内化专家。你的任务是将视频脚本转化为一份结构清晰、逻辑严密、且极度详尽的 Markdown 学习笔记。

【核心任务：深度解构】
1. **零信息损失**：脚本中提到的每一个核心概念、数据点、案例研究、名人名言和结论都必须保留。
2. **逻辑还原**：不仅仅是记录文字，要还原视频讲解的逻辑体系。如果视频提到了"为什么"、"怎么做"以及"对比关系"，笔记必须完整体现这些推导过程。
3. **解释性细节**：对于复杂的概念，保留视频中的类比或具体例子（例如：通过生活实例来解释抽象原理）。
4. **数据与事实**：所有具体的数字、百分比、时间节点、专业术语必须原样保留，并用 **加粗** 标注。

【核心任务：公式主动提取与转换】
- **主动识别**：即使脚本中公式是用口语描述的（如"E等于m乘以c的平方"、"loss等于负log概率的期望"、"x的n次方对x求导得到n乘x的n减一次方"），你**必须**将其还原为标准的 LaTeX 数学公式，不得只保留文字描述。
- **行间公式**（独立成行的完整公式）：使用 `$$...$$` 包裹，且该行只有公式，例如：
  $$E = mc^2$$
- **行内公式**（嵌入句子中的短公式或变量名）：使用 `$...$` 包裹，例如：当 $x > 0$ 时，$f(x) = x^2$。
- **推导过程**：如果视频讲解了一个推导或证明的步骤，每一步都单独写成一个行间公式，并在公式前后用文字说明该步的含义。
- **常见口语转 LaTeX 参考**：
  - "A乘以B" → $A \times B$ 或 $AB$
  - "A除以B" / "A比B" → $\dfrac{A}{B}$
  - "x的n次方" → $x^n$
  - "根号A" / "A的平方根" → $\sqrt{A}$
  - "对x求偏导" / "关于x的偏导数" → $\dfrac{\partial f}{\partial x}$
  - "求和从i等于1到n" → $\sum_{i=1}^{n}$
  - "积分" → $\int_{a}^{b} f(x)\,dx$
  - "期望" → $\mathbb{E}[\cdot]$
  - "正态分布" → $\mathcal{N}(\mu, \sigma^2)$
  - "无穷大" → $\infty$
  - "约等于" → $\approx$
  - "属于" → $\in$
  - "向量/矩阵" → 用粗体 $\mathbf{x}$、$\mathbf{W}$

【笔记结构规范】
- **标题**：第一行使用一级标题 `# [视频主题全名]`。
- **模块化**：使用二级标题 `##` 划分视频的主要章节，必须覆盖视频从头到尾的完整流程。
- **多级嵌套**：在章节内，使用三级标题 `###` 或四级标题 `####` 来拆解子话题，确保内容不堆砌，易于扫描。
- **突出重点**：
    - 使用 `> ` 块来引用视频中的金句、重要警示或核心原则。
    - 使用无序列表 `- ` 展开详细的解释说明。

【语言与风格】
- 必须使用中文，除非术语本身是英文。
- 笔记的详尽程度应达到脚本词数的 90%，严禁过度简化。

【特别禁止】
- 严禁在笔记中写任何关于"脚本中断""脚本截断""此处省略""视频后续内容"等元评论
- 如果脚本内容到某处结束，笔记就在该处自然收尾，不做任何说明"""

USER_TEMPLATE = """请根据以下视频脚本，生成一份专业、详尽、具备深度教学意义的学习笔记。

【待处理脚本信息】
- 脚本字数：{wc}。
- 目标：确保笔记内容详尽到足以让没看过视频的人也能完全理解其中的核心逻辑和所有细节。

【脚本全文】
{transcript}"""


# ─── AI 调用函数 ──────────────────────────────────────────────
def call_groq(api_key, prompt_sys, prompt_user):
    from groq import Groq
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt_sys},
            {"role": "user",   "content": prompt_user}
        ],
        max_tokens=8000,
        temperature=0.2,
    )
    return completion.choices[0].message.content

def call_gemini(api_key, prompt_sys, prompt_user):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{prompt_sys}\n\n{prompt_user}",
    )
    return response.text


# ─── 页面渲染 ─────────────────────────────────────────────────
st.markdown("""
<div class="lemon-header">
  <h1>🍋 YouTube AI 笔记助手</h1>
  <p>输入链接 → 自动提取字幕 → AI 生成完整笔记 → 导出HTML</p>
</div>
""", unsafe_allow_html=True)

# ── 视频链接
st.markdown('<p class="section-label">🔗 视频链接</p>', unsafe_allow_html=True)
video_url = st.text_input("video_url", label_visibility="collapsed",
    placeholder="https://www.youtube.com/watch?v=xxxxxxxxxxx")

# ── 字幕 Token
st.markdown('<p class="section-label" style="margin-top:0.8rem">🔑 字幕 API</p>', unsafe_allow_html=True)
transcript_token = st.text_input("YouTube Transcript Token", type="password",
    placeholder="paste your token here")
st.markdown('<p class="tip">获取：<a href="https://www.youtube-transcript.io" target="_blank">youtube-transcript.io</a></p>',
    unsafe_allow_html=True)

# ── AI 模型选择
st.markdown('<p class="section-label" style="margin-top:0.8rem">AI 模型</p>', unsafe_allow_html=True)
model_choice = st.radio(
    "model_choice", ["Groq", "Gemini"],
    horizontal=True, label_visibility="collapsed"
)

# ── 根据选择显示对应 Token 输入框
if "Groq" in model_choice:
    ai_token = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.markdown('<p class="tip">免费注册：<a href="https://console.groq.com" target="_blank">console.groq.com</a> · 模型：llama-3.3-70b-versatile</p>',
        unsafe_allow_html=True)
    model_name = "groq"
else:
    ai_token = st.text_input("Gemini API Key", type="password", placeholder="AIza...")
    st.markdown('<p class="tip">获取：<a href="https://aistudio.google.com/apikey" target="_blank">aistudio.google.com/apikey</a> · 模型：gemini-2.5-flash</p>',
        unsafe_allow_html=True)
    model_name = "gemini"

# ── 居中按钮
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1.5, 2, 1.5])
with btn_col:
    run = st.button("🍋 开始生成笔记", use_container_width=True)


# ─── 执行逻辑 ─────────────────────────────────────────────────
if run:
    if not ai_token:
        st.error(f"❌ 请填写 {'Groq' if model_name == 'groq' else 'Gemini'} API Key")
        st.stop()

    if not video_url:
        st.error("❌ 请填写 YouTube 视频链接"); st.stop()
    if not transcript_token:
        st.error("❌ 请填写 YouTube Transcript Token"); st.stop()

    video_id = extract_video_id(video_url)
    final_url = video_url

    try:
        with st.status("🍋 正在处理，请稍候...", expanded=True) as status:

            # 步骤 1：获取字幕
            st.write("📡 正在获取字幕...")
            res = requests.post(
                "https://www.youtube-transcript.io/api/transcripts",
                headers={"Authorization": f"Basic {transcript_token}", "Content-Type": "application/json"},
                json={"ids": [video_id]}, timeout=30
            )
            if res.status_code != 200:
                st.error(f"字幕 API 失败 (状态码 {res.status_code})"); st.stop()
            data = res.json()
            with st.expander("🔍 原始字幕 API 数据"):
                st.json(data)
            if isinstance(data, list) and data:
                vd = data[0]
                if "error" in vd: st.error(f"API 错误: {vd['error']}"); st.stop()
                raw = vd.get('transcript') or []
                if not raw:
                    tracks = vd.get('tracks', [])
                    if tracks: raw = tracks[0].get('transcript', [])
                if not raw: st.warning("⚠️ 未找到字幕"); st.stop()
                transcript_text = " ".join(i.get('text', '') for i in raw)
            else:
                st.error("❌ API 返回格式异常"); st.stop()

            wc = len(transcript_text.split())
            st.write(f"✅ 字幕获取成功（{wc} 词）")

            # 步骤 2：生成笔记
            badge = "Groq · llama-3.3-70b" if model_name == "groq" else "Gemini · 2.5-flash"
            st.write(f"正在调用 {badge} 生成笔记...")

            prompt_user = USER_TEMPLATE.format(wc=wc, transcript=transcript_text)

            if model_name == "groq":
                md = call_groq(ai_token, SYSTEM_PROMPT, prompt_user)
            else:
                md = call_gemini(ai_token, SYSTEM_PROMPT, prompt_user)

            st.write(f"✅ 笔记生成完成（{len(md.split())} 词）")

            # 步骤 3：渲染 HTML
            st.write("🎨 正在渲染 HTML...")
            html_out = md_to_lemon_html(md, final_url, video_id)
            status.update(label="🍋 全部完成！", state="complete", expanded=False)

        st.divider()
        tab1, tab2, tab3 = st.tabs(["🌐 HTML", "📝 Markdown", "🔤 原始字幕"])

        with tab1:
            st.components.v1.html(html_out, height=720, scrolling=True)
            st.download_button("HTML", data=html_out,
                file_name=f"Note_{video_id}.html", mime="text/html", use_container_width=True)

        with tab2:
            st.code(md, language="markdown")
            st.download_button("Markdown", data=md,
                file_name=f"Note_{video_id}.md", use_container_width=True)

        with tab3:
            st.text_area("原始字幕内容", transcript_text, height=280, label_visibility="collapsed")
            st.download_button("原始字幕", data=transcript_text,
                file_name=f"Transcript_{video_id}.txt", mime="text/plain", use_container_width=True)

    except Exception as e:
        st.error(f"程序崩溃: {str(e)}")
        st.exception(e)