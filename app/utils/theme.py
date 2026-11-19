"""
Shared look and feel for ExoDetect AI.

Place this file at:  app/utils/theme.py

Every page only needs:
    from app.utils.theme import apply_theme
    apply_theme()          # right after st.set_page_config(...)
"""

import random

import streamlit as st

# How many shooting stars to show (try 3 to 12)
SHOOTING_STARS = 10

PALETTE = ["#56CFE1", "#8B7CF6", "#F5B942", "#3DDC97", "#FF6B81"]


# --------------------------------------------------
# BASE THEME
# --------------------------------------------------

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #070B16;
    --surface: #0F1830;
    --surface-2: #131F3D;
    --border: #22304F;
    --cyan: #56CFE1;
    --violet: #8B7CF6;
    --text: #E6EDF7;
    --muted: #93A4C3;
}

.stApp {
    background:
        radial-gradient(1100px 560px at 88% -8%, rgba(86, 207, 225, 0.10), transparent 60%),
        radial-gradient(900px 500px at -8% 8%, rgba(139, 124, 246, 0.11), transparent 55%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* ---------- Typography ---------- */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    color: var(--text);
    letter-spacing: -0.01em;
}

.stApp h2 {
    border-left: 4px solid var(--cyan);
    padding-left: 14px;
    margin-top: 0.6rem;
}

.stApp h3 { color: #CFE3F5; }

p, li { line-height: 1.65; }

[data-testid="stCaptionContainer"] { color: var(--muted); }

hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #2B3C61, transparent) !important;
    margin: 1.6rem 0 !important;
}

/* ---------- Hero banners ---------- */
.hero, .page-hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(125deg, #101D38 0%, #172B4D 55%, #1B2352 100%);
    padding: 34px 38px;
    border-radius: 20px;
    border: 1px solid #2A3F66;
    margin-bottom: 26px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
}

.hero::after, .page-hero::after {
    content: "";
    position: absolute;
    right: -80px;
    top: -80px;
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(86, 207, 225, 0.28), transparent 65%);
    pointer-events: none;
}

.hero h1, .page-hero h1 {
    font-size: 40px;
    margin: 6px 0 10px 0;
    padding: 0;
    background: linear-gradient(90deg, #FFFFFF, #8FE3F0);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p, .page-hero p {
    color: #B8C7DF;
    font-size: 17px;
    max-width: 760px;
    margin: 0;
}

.hero-tag {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--cyan);
    background: rgba(86, 207, 225, 0.10);
    border: 1px solid rgba(86, 207, 225, 0.35);
    padding: 4px 12px;
    border-radius: 999px;
}

.chip-row { margin-top: 18px; display: flex; flex-wrap: wrap; gap: 8px; }

.chip {
    font-size: 13px;
    color: #CFE3F5;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 5px 13px;
    border-radius: 999px;
}

/* ---------- Cards ---------- */
.metric-card, .feature-card, .info-card {
    background: linear-gradient(160deg, rgba(22, 35, 66, 0.95), rgba(13, 21, 40, 0.95));
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card {
    padding: 22px 18px;
    text-align: center;
}

.metric-card:hover, .feature-card:hover {
    transform: translateY(-3px);
    border-color: rgba(86, 207, 225, 0.55);
}

.metric-icon { font-size: 24px; margin-bottom: 6px; }

.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--cyan);
}

.metric-label {
    font-size: 13px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.feature-card { padding: 20px; margin-bottom: 15px; height: 100%; }
.feature-card .fc-icon { font-size: 26px; margin-bottom: 8px; }
.feature-card .fc-title { font-weight: 600; color: var(--text); margin-bottom: 4px; }
.feature-card .fc-text { font-size: 14px; color: var(--muted); line-height: 1.5; }

.info-card { padding: 22px 24px; }
.info-card h4 { margin: 0 0 14px 0; color: var(--cyan); }

.kv-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    padding: 9px 0;
    border-bottom: 1px dashed rgba(147, 164, 195, 0.18);
    font-size: 15px;
}
.kv-row:last-child { border-bottom: none; }
.kv-key { color: var(--muted); }
.kv-val { color: var(--text); font-weight: 600; text-align: right; }

.pill {
    display: inline-block;
    margin: 4px 6px 4px 0;
    padding: 7px 16px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    color: #E6EDF7;
    background: rgba(139, 124, 246, 0.14);
    border: 1px solid rgba(139, 124, 246, 0.45);
}

/* ---------- Prediction result ---------- */
.result-card {
    --accent: #56CFE1;
    background: linear-gradient(160deg, rgba(22, 35, 66, 0.95), rgba(13, 21, 40, 0.95));
    padding: 30px;
    border-radius: 18px;
    border: 1px solid var(--accent);
    box-shadow: 0 0 32px color-mix(in srgb, var(--accent) 25%, transparent);
    text-align: center;
    margin-bottom: 18px;
}

.result-label {
    font-size: 13px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
}

.result-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 40px;
    font-weight: 700;
    color: var(--accent);
    margin: 6px 0;
}

.result-conf { color: #B8C7DF; font-size: 15px; }

/* ---------- Streamlit widgets ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(160deg, rgba(22, 35, 66, 0.95), rgba(13, 21, 40, 0.95));
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22);
}

[data-testid="stMetricLabel"] { color: var(--muted); }

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--cyan);
}

[data-testid="stPlotlyChart"] {
    background: rgba(15, 24, 48, 0.65);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 8px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stExpander"] {
    background: rgba(15, 24, 48, 0.75);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 8px;
}

[data-testid="stForm"] {
    background: rgba(15, 24, 48, 0.55);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 24px;
}

div[data-baseweb="input"], div[data-baseweb="select"] > div {
    background-color: var(--surface) !important;
    border-radius: 10px !important;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    border-radius: 12px;
    border: 1px solid rgba(86, 207, 225, 0.45);
    background: rgba(86, 207, 225, 0.08);
    color: var(--text);
    font-weight: 600;
    padding: 0.6rem 1rem;
    transition: all 0.2s ease;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    border-color: var(--cyan);
    background: rgba(86, 207, 225, 0.18);
    color: #FFFFFF;
    transform: translateY(-1px);
}

[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, #2BB6CF, #6C63F0);
    border: none;
    font-size: 16px;
    padding: 0.8rem 1rem;
    box-shadow: 0 8px 24px rgba(108, 99, 240, 0.35);
}

[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(90deg, #35C6DF, #7C74FF);
    transform: translateY(-2px);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1224 0%, #090F1E 100%);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1 {
    font-size: 24px;
    background: linear-gradient(90deg, #FFFFFF, #8FE3F0);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #26344D; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #35496E; }

"""


# --------------------------------------------------
# ANIMATED SPACE BACKGROUND
# --------------------------------------------------

def _star_shadows(count, seed):
    """Generate random star positions as a CSS box-shadow list."""
    rng = random.Random(seed)
    shadows = []

    for _ in range(count):
        x = rng.uniform(0, 100)
        y = rng.uniform(0, 100)
        size = rng.choice([0, 0, 1])
        alpha = rng.uniform(0.35, 0.95)
        shadows.append(f"{x:.1f}vw {y:.1f}vh 0 {size}px rgba(255,255,255,{alpha:.2f})")

    return ",".join(shadows)


ANIMATION_CSS = """
.space-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.block-container, [data-testid="stSidebar"] {
    position: relative;
    z-index: 1;
}

.element-container:has(.space-bg),
[data-testid="stElementContainer"]:has(.space-bg) {
    height: 0;
    margin: 0;
    padding: 0;
    overflow: visible;
}

/* ---------- Stars ---------- */
.stars {
    position: absolute;
    top: 0;
    left: 0;
    width: 2px;
    height: 2px;
    border-radius: 50%;
    animation: twinkle 5s ease-in-out infinite alternate;
}

.stars.layer-a { box-shadow: __STARS_A__; }
.stars.layer-b { box-shadow: __STARS_B__; animation-duration: 8s; animation-delay: -3s; }

@keyframes twinkle {
    from { opacity: 0.25; }
    to   { opacity: 1; }
}

/* ---------- Planets ---------- */
.planet {
    position: absolute;
    border-radius: 50%;
}

.planet-1 {
    width: 230px;
    height: 230px;
    right: -70px;
    top: 12vh;
    background: radial-gradient(circle at 30% 28%, #9A8CFF 0%, #4B3DB0 52%, #15112E 100%);
    box-shadow: inset -34px -24px 66px rgba(0, 0, 0, 0.65), 0 0 90px rgba(139, 124, 246, 0.28);
    opacity: 0.55;
    animation: drift-a 38s ease-in-out infinite alternate;
}

.planet-1::after {
    content: "";
    position: absolute;
    left: -48%;
    top: 40%;
    width: 196%;
    height: 22%;
    border: 3px solid rgba(206, 196, 255, 0.38);
    border-radius: 50%;
    transform: rotate(-18deg);
}

.planet-2 {
    width: 96px;
    height: 96px;
    left: 5vw;
    bottom: 12vh;
    background: radial-gradient(circle at 32% 30%, #8FF0FF 0%, #1FA7C4 50%, #072B3A 100%);
    box-shadow: inset -16px -12px 30px rgba(0, 0, 0, 0.6), 0 0 50px rgba(86, 207, 225, 0.28);
    opacity: 0.5;
    animation: drift-b 52s ease-in-out infinite alternate;
}

.planet-3 {
    width: 38px;
    height: 38px;
    right: 28vw;
    bottom: 9vh;
    background: radial-gradient(circle at 30% 30%, #FFD08A 0%, #D9772B 55%, #3A1708 100%);
    box-shadow: inset -7px -5px 14px rgba(0, 0, 0, 0.6), 0 0 28px rgba(245, 185, 66, 0.25);
    opacity: 0.55;
    animation: drift-a 30s ease-in-out infinite alternate-reverse;
}

@keyframes drift-a {
    from { transform: translate(0, 0) rotate(0deg); }
    to   { transform: translate(-34px, 26px) rotate(6deg); }
}

@keyframes drift-b {
    from { transform: translate(0, 0); }
    to   { transform: translate(30px, -24px); }
}

/* ---------- Orbit ring with a tiny satellite ---------- */
.orbit {
    position: absolute;
    left: -190px;
    top: -190px;
    width: 560px;
    height: 560px;
    border: 1px dashed rgba(86, 207, 225, 0.22);
    border-radius: 50%;
    animation: spin 90s linear infinite;
}

.orbit::after {
    content: "";
    position: absolute;
    top: -5px;
    left: 50%;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #56CFE1;
    box-shadow: 0 0 16px 4px rgba(86, 207, 225, 0.65);
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ---------- Shooting star ---------- */
.comet {
    position: absolute;
    width: 140px;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.9));
    transform: rotate(24deg);
    opacity: 0;
    animation: comet 16s ease-in infinite;
}

@keyframes comet {
    0%   { transform: translate(0, 0) rotate(24deg); opacity: 0; }
    3%   { opacity: 1; }
    12%  { transform: translate(60vw, 28vw) rotate(24deg); opacity: 0; }
    100% { transform: translate(60vw, 28vw) rotate(24deg); opacity: 0; }
}

/* Respect users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
    .stars, .planet, .orbit, .comet { animation: none !important; }
}
"""

def _comets(count):
    """Shooting stars with random start positions, speeds and delays."""
    rng = random.Random(99)
    items = []

    for _ in range(count):
        top = rng.uniform(2, 60)
        left = rng.uniform(-5, 45)
        duration = rng.uniform(9, 22)
        delay = rng.uniform(0, 14)
        items.append(
            f'<div class="comet" style="top:{top:.0f}vh;left:{left:.0f}vw;'
            f'animation-duration:{duration:.1f}s;animation-delay:{delay:.1f}s;"></div>'
        )

    return ''.join(items)


BACKGROUND_HTML = (
    '<div class="space-bg">'
    '<div class="orbit"></div>'
    '<div class="stars layer-a"></div>'
    '<div class="stars layer-b"></div>'
    '<div class="planet planet-1"></div>'
    '<div class="planet planet-2"></div>'
    '<div class="planet planet-3"></div>'
    + _comets(SHOOTING_STARS) +
    '</div>'
)


def _clean(css):
    """Remove blank lines so Streamlit's markdown parser never splits the block."""
    return "\n".join(line for line in css.splitlines() if line.strip())


def apply_theme(animated=True):
    """Inject the shared CSS (and the animated planets) into the current page."""

    css = BASE_CSS

    if animated:
        css += (
            ANIMATION_CSS
            .replace("__STARS_A__", _star_shadows(70, seed=7))
            .replace("__STARS_B__", _star_shadows(50, seed=21))
        )

    st.markdown(f"<style>{_clean(css)}</style>", unsafe_allow_html=True)

    if animated:
        st.markdown(BACKGROUND_HTML, unsafe_allow_html=True)


# --------------------------------------------------
# REUSABLE UI COMPONENTS
# --------------------------------------------------

def page_hero(icon, title, subtitle, tag):
    st.markdown(
        '<div class="page-hero">'
        f'<span class="hero-tag">{tag}</span>'
        f'<h1>{icon} {title}</h1>'
        f'<p>{subtitle}</p>'
        '</div>',
        unsafe_allow_html=True
    )


def metric_card(icon, value, label):
    return (
        '<div class="metric-card">'
        f'<div class="metric-icon">{icon}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div>'
        '</div>'
    )


def feature_card(icon, title, text):
    return (
        '<div class="feature-card">'
        f'<div class="fc-icon">{icon}</div>'
        f'<div class="fc-title">{title}</div>'
        f'<div class="fc-text">{text}</div>'
        '</div>'
    )


def sidebar_brand():
    with st.sidebar:
        st.title("🪐 ExoDetect AI")
        st.caption("NASA Exoplanet Detection System")
        st.divider()
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.caption("CatBoost · Kepler · TESS")


def show_chart(fig, use_container_width=True):
    """Plotly chart with the ExoDetect colours and transparent background."""

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#E6EDF7"),
        colorway=PALETTE,
        title=dict(font=dict(size=18, family="Space Grotesk, Inter, sans-serif")),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(gridcolor="rgba(120,140,180,0.15)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(120,140,180,0.15)", zeroline=False)

    for i, trace in enumerate(fig.data):
        if trace.type == "bar" and getattr(trace.marker, "coloraxis", None) is None:
            trace.marker.color = PALETTE[i % len(PALETTE)]

    st.plotly_chart(fig, use_container_width=use_container_width)
