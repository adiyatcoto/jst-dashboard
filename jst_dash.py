"""
Jordà-Schularick-Taylor Dataset R6
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="JST Macrohistory Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# THEME & CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

:root {
    --bg:        #0a0e17;
    --surface:   #111827;
    --surface2:  #1a2235;
    --border:    #1e2d45;
    --accent:    #3b82f6;
    --accent2:   #06b6d4;
    --accent3:   #f59e0b;
    --accent4:   #10b981;
    --danger:    #ef4444;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --mono:      'IBM Plex Mono', monospace;
    --sans:      'IBM Plex Sans', sans-serif;
    --serif:     'Playfair Display', serif;
}

html, body, [class*="css"] {
    font-family: var(--sans);
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Main header */
.dash-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f1e3d 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
}
.dash-header h1 {
    font-family: var(--serif);
    font-size: 2.2rem;
    color: #f1f5f9;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.dash-header .subtitle {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.dash-header .meta {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 8px;
}

/* KPI cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
}
.kpi-card.amber::after { background: var(--accent3); }
.kpi-card.cyan::after  { background: var(--accent2); }
.kpi-card.green::after { background: var(--accent4); }
.kpi-card .label {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
}
.kpi-card .value {
    font-family: var(--mono);
    font-size: 1.9rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1;
}
.kpi-card .delta {
    font-size: 0.75rem;
    margin-top: 6px;
    color: var(--muted);
}

/* Section labels */
.section-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin: 32px 0 12px 0;
    border-left: 3px solid var(--accent);
    padding-left: 12px;
}

/* Chart containers */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 16px;
}

/* Insight boxes */
.insight-box {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent3);
    border-radius: 8px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 0.85rem;
    line-height: 1.6;
}
.insight-box .insight-title {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: var(--accent3);
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* Tables */
.stDataFrame { background: var(--surface) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 8px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--mono);
    font-size: 0.75rem;
    letter-spacing: 1px;
    color: var(--muted) !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: var(--surface2) !important;
    border-radius: 6px;
}

/* Select / Multiselect */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Slider */
.stSlider > div > div > div { background: var(--accent) !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
}

/* Footer */
.dash-footer {
    text-align: center;
    padding: 24px;
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 2px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#111827",
    plot_bgcolor="#0f172a",
    font=dict(family="IBM Plex Mono", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", zeroline=False),
    yaxis=dict(gridcolor="#1e2d45", linecolor="#1e2d45", zeroline=False),
    legend=dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1),
    margin=dict(l=50, r=20, t=40, b=40),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#1e293b", bordercolor="#3b82f6", font_family="IBM Plex Mono"),
)

PALETTE = ["#3b82f6","#06b6d4","#10b981","#f59e0b","#8b5cf6","#ef4444","#f97316","#ec4899",
           "#14b8a6","#a78bfa","#fb923c","#34d399","#60a5fa","#fbbf24","#e879f9","#4ade80","#f472b6"]

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
JST_URL = "https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.dta"

@st.cache_data(show_spinner=False)
def load_data_from_url(url):
    import urllib.request, tempfile, os, io
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/octet-stream,*/*",
        "Referer": "https://www.macrohistory.net/",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    tmp = tempfile.NamedTemporaryFile(suffix=".dta", delete=False)
    tmp.write(data)
    tmp.flush()
    tmp.close()
    df = pd.read_stata(tmp.name)
    os.unlink(tmp.name)
    return df

@st.cache_data(show_spinner=False)
def load_data(path):
    try:
        df = pd.read_stata(path)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()
    return df

@st.cache_data(show_spinner=False)
def enrich_data(df):
    """Compute derived variables."""
    d = df.copy()

    # Credit-to-GDP ratios
    if "tloans" in d.columns and "gdp" in d.columns:
        d["credit_gdp"] = d["tloans"] / d["gdp"] * 100
    if "hh_mortgage" in d.columns and "gdp" in d.columns:
        d["mortgage_gdp"] = d["hh_mortgage"] / d["gdp"] * 100
    if "nfc_loans" in d.columns and "gdp" in d.columns:
        d["nfc_gdp"] = d["nfc_loans"] / d["gdp"] * 100

    # Money / GDP
    if "money" in d.columns and "gdp" in d.columns:
        d["money_gdp"] = d["money"] / d["gdp"] * 100

    # Real returns
    if "tloans" in d.columns:
        d["loan_growth"] = d.groupby("iso")["tloans"].pct_change() * 100
    if "gdp" in d.columns:
        d["gdp_growth"] = d.groupby("iso")["gdp"].pct_change() * 100
    if "cpi" in d.columns:
        d["inflation"] = d.groupby("iso")["cpi"].pct_change() * 100

    # Leverage cycle: excess credit growth (credit_gdp change)
    if "credit_gdp" in d.columns:
        d["credit_gdp_chg"] = d.groupby("iso")["credit_gdp"].diff()

    # Real house prices
    if "hpnom" in d.columns and "cpi" in d.columns:
        d["hp_real"] = d["hpnom"] / d["cpi"]
        d["hp_real_growth"] = d.groupby("iso")["hp_real"].pct_change() * 100

    # Real equity
    if "eq_tr" in d.columns and "cpi" in d.columns:
        d["eq_real_tr"] = d["eq_tr"] / d["cpi"]

    # Current account / GDP
    if "ca" in d.columns and "gdp" in d.columns:
        d["ca_gdp"] = d["ca"] / d["gdp"] * 100

    # Investment / GDP
    if "iy" in d.columns:
        d["inv_gdp"] = d["iy"] * 100

    return d

# ─────────────────────────────────────────────
# SIDEBAR — DATA SOURCE
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;letter-spacing:3px;color:#3b82f6;text-transform:uppercase;margin-bottom:20px;">⬡ JST Macrohistory</div>', unsafe_allow_html=True)

    load_mode = st.radio("Data Source", ["⬇ Auto-load from URL", "📂 Upload .dta file"], index=0)

    uploaded   = None

    if load_mode == "⬇ Auto-load from URL":
        st.markdown(
            f'<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;'
            f'color:#64748b;word-break:break-all;margin-bottom:12px;">'
            f'{JST_URL}</div>', unsafe_allow_html=True
        )
        if "auto_load" not in st.session_state:
            st.session_state["auto_load"] = False
        if st.button("🚀 Load Dataset Now", use_container_width=True):
            st.session_state["auto_load"] = True
        if not st.session_state["auto_load"]:
            st.info("Click **Load Dataset Now** to stream the dataset directly from macrohistory.net")
            st.stop()
    else:
        uploaded = st.file_uploader("Upload JSTdatasetR6.dta", type=["dta"])
        if uploaded is None:
            st.info("👆 Upload the JST .dta file to begin.")
            st.stop()

    st.markdown("---")
    st.markdown('<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;letter-spacing:2px;color:#64748b;text-transform:uppercase;margin-bottom:10px;">Filters</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD & ENRICH
# ─────────────────────────────────────────────
with st.spinner("Loading JST dataset..."):
    if uploaded is not None:
        df_raw = load_data(uploaded)
    else:
        df_raw = load_data_from_url(JST_URL)
    df = enrich_data(df_raw)

COUNTRIES = sorted(df["iso"].unique().tolist()) if "iso" in df.columns else []
YEARS = sorted(df["year"].unique().tolist()) if "year" in df.columns else []

# All numeric columns
NUM_COLS = df.select_dtypes(include=np.number).columns.tolist()
NON_ID = [c for c in NUM_COLS if c not in ["year","crisisJST","crisisdate"]]

with st.sidebar:
    selected_countries = st.multiselect("Countries", COUNTRIES, default=COUNTRIES[:6] if len(COUNTRIES)>=6 else COUNTRIES)
    year_range = st.slider("Year Range", int(min(YEARS)), int(max(YEARS)), (1950, int(max(YEARS)))) if YEARS else (1870, 2020)
    st.markdown("---")
    crisis_only = st.checkbox("Highlight Crisis Episodes", value=True)
    log_scale   = st.checkbox("Log Scale (where applicable)", value=False)
    st.markdown("---")
    st.markdown('<div style="font-family:\'IBM Plex Mono\';font-size:0.6rem;color:#334155;letter-spacing:1px;">JST Dataset R6 · Jordà, Schularick & Taylor · macrohistory.net</div>', unsafe_allow_html=True)

if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

# Filter
mask = df["iso"].isin(selected_countries) & df["year"].between(*year_range)
dff = df[mask].copy()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="subtitle">Jordà–Schularick–Taylor Macrohistory Lab</div>
    <h1>Global Financial History Dashboard</h1>
    <div class="meta">
        Dataset R6 &nbsp;·&nbsp; {len(COUNTRIES)} economies &nbsp;·&nbsp;
        {int(min(YEARS))}–{int(max(YEARS))} &nbsp;·&nbsp;
        {len(df_raw.columns)} variables &nbsp;·&nbsp;
        {len(df_raw):,} observations
        &nbsp;·&nbsp; <span style="color:#3b82f6;">Filtered: {len(dff):,} obs</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI SUMMARY ROW
# ─────────────────────────────────────────────
crisis_col = "crisisJST" if "crisisJST" in dff.columns else ("crisisdate" if "crisisdate" in dff.columns else None)
n_crises   = int(dff[crisis_col].sum()) if crisis_col else 0

avg_credit_gdp = dff["credit_gdp"].mean() if "credit_gdp" in dff.columns else None
avg_gdp_growth = dff["gdp_growth"].mean() if "gdp_growth" in dff.columns else None
avg_inflation  = dff["inflation"].mean()  if "inflation"  in dff.columns else None
avg_ltrate     = dff["ltrate"].mean()     if "ltrate"     in dff.columns else None

c1,c2,c3,c4 = st.columns(4)
def kpi(col, label, value, suffix="", css_class=""):
    with col:
        val_str = f"{value:.1f}{suffix}" if value is not None else "N/A"
        st.markdown(f"""
        <div class="kpi-card {css_class}">
            <div class="label">{label}</div>
            <div class="value">{val_str}</div>
        </div>""", unsafe_allow_html=True)

kpi(c1, "Crisis Episodes", n_crises, "", "")
kpi(c2, "Avg Credit / GDP", avg_credit_gdp, "%", "amber")
kpi(c3, "Avg GDP Growth", avg_gdp_growth, "%", "cyan")
kpi(c4, "Avg Inflation", avg_inflation, "%", "green")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📈 Credit & Leverage",
    "🏦 Money & Banking",
    "🏠 Asset Prices",
    "🌐 Macro Aggregates",
    "⚡ Crisis Analysis",
    "📊 Cross-Country",
    "🔬 Correlations",
    "🗂 Data Explorer",
])

# helper: add crisis shading
def add_crisis_shading(fig, country_data, crisis_col, yref="y"):
    if not crisis_only or crisis_col is None or crisis_col not in country_data.columns:
        return fig
    in_crisis = False
    x0 = None
    rows = country_data.sort_values("year")
    for _, row in rows.iterrows():
        val = row[crisis_col]
        yr  = row["year"]
        if val == 1 and not in_crisis:
            in_crisis = True
            x0 = yr
        elif val != 1 and in_crisis:
            in_crisis = False
            fig.add_vrect(x0=x0, x1=yr, fillcolor="rgba(239,68,68,0.08)",
                          layer="below", line_width=0)
    if in_crisis:
        fig.add_vrect(x0=x0, x1=rows["year"].max(), fillcolor="rgba(239,68,68,0.08)",
                      layer="below", line_width=0)
    return fig

# ══════════════════════════════════════════════
# TAB 1 — CREDIT & LEVERAGE
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-label">Credit Dynamics & Leverage Cycles</div>', unsafe_allow_html=True)

    # Credit/GDP over time
    if "credit_gdp" in dff.columns:
        fig = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig.add_trace(go.Scatter(
                x=d["year"], y=d["credit_gdp"],
                name=iso, mode="lines",
                line=dict(color=PALETTE[i%len(PALETTE)], width=1.8),
                hovertemplate=f"<b>{iso}</b><br>Year: %{{x}}<br>Credit/GDP: %{{y:.1f}}%<extra></extra>"
            ))
            fig = add_crisis_shading(fig, d, crisis_col)
        fig.update_layout(**PLOTLY_LAYOUT, title="Total Loans / GDP (%)", height=400,
                          yaxis_type="log" if log_scale else "linear")
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if "mortgage_gdp" in dff.columns:
            fig2 = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig2.add_trace(go.Scatter(x=d["year"], y=d["mortgage_gdp"],
                    name=iso, mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig2 = add_crisis_shading(fig2, d, crisis_col)
            fig2.update_layout(**PLOTLY_LAYOUT, title="Mortgage Loans / GDP (%)", height=320)
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        if "nfc_gdp" in dff.columns:
            fig3 = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig3.add_trace(go.Scatter(x=d["year"], y=d["nfc_gdp"],
                    name=iso, mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig3 = add_crisis_shading(fig3, d, crisis_col)
            fig3.update_layout(**PLOTLY_LAYOUT, title="Non-Financial Corporate Loans / GDP (%)", height=320)
            st.plotly_chart(fig3, use_container_width=True)

    # Credit growth distribution
    if "loan_growth" in dff.columns:
        st.markdown('<div class="section-label">Credit Growth Distribution</div>', unsafe_allow_html=True)
        fig4 = go.Figure()
        for i, iso in enumerate(selected_countries):
            vals = dff[dff["iso"]==iso]["loan_growth"].dropna()
            hx = PALETTE[i%len(PALETTE)].lstrip("#")
            r, g, b = int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)
            fig4.add_trace(go.Violin(x=vals, name=iso, line_color=PALETTE[i%len(PALETTE)],
                                     fillcolor=f"rgba({r},{g},{b},0.15)",
                                     box_visible=True, meanline_visible=True, orientation="h"))
        fig4.update_layout(**PLOTLY_LAYOUT, title="Distribution of Annual Loan Growth (%)", height=60+40*len(selected_countries))
        st.plotly_chart(fig4, use_container_width=True)

    # Insight box
    if "credit_gdp" in dff.columns:
        latest = dff.groupby("iso")["credit_gdp"].last().sort_values(ascending=False)
        top = latest.index[0] if len(latest) else "N/A"
        top_val = latest.iloc[0] if len(latest) else 0
        early_avg = dff[dff["year"]<=1929]["credit_gdp"].mean()
        late_avg  = dff[dff["year"]>=1980]["credit_gdp"].mean()
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">🔍 Leverage Cycle Intelligence</div>
            Among selected economies, <b>{top}</b> shows the highest recent Credit/GDP at
            <b>{top_val:.0f}%</b>. Average credit/GDP pre-1929 was <b>{early_avg:.0f}%</b>
            vs <b>{late_avg:.0f}%</b> post-1980 — a structural upward shift consistent with
            the "Great Leveraging" documented by Schularick & Taylor (2012).
            Red bands indicate JST-coded financial crisis episodes.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — MONEY & BANKING
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-label">Monetary Aggregates & Interest Rates</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "money_gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["money_gdp"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Broad Money / GDP (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "ltrate" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["ltrate"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Long-Term Interest Rate (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if "stir" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["stir"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Short-Term Interest Rate (%)", height=320)
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "ltrate" in dff.columns and "stir" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["term_spread"] = d["ltrate"] - d["stir"]
                fig.add_trace(go.Scatter(x=d["year"], y=d["term_spread"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Term Spread: LT − ST Rate (%)", height=320)
            st.plotly_chart(fig, use_container_width=True)

    # Inflation
    if "inflation" in dff.columns:
        st.markdown('<div class="section-label">Inflation History</div>', unsafe_allow_html=True)
        fig_inf = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig_inf.add_trace(go.Scatter(x=d["year"], y=d["inflation"],
                name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6),
                fill="tozeroy" if len(selected_countries)==1 else None,
                fillcolor="rgba(59,130,246,0.07)"))
            fig_inf = add_crisis_shading(fig_inf, d, crisis_col)
        fig_inf.add_hline(y=2, line_dash="dot", line_color="#64748b",
                          annotation_text="2% target", annotation_font_color="#64748b")
        fig_inf.update_layout(**PLOTLY_LAYOUT, title="CPI Inflation Rate (%)", height=360)
        st.plotly_chart(fig_inf, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — ASSET PRICES
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-label">Asset Price Cycles: Housing & Equities</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if "hp_real_growth" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Bar(x=d["year"], y=d["hp_real_growth"],
                    name=iso, marker_color=PALETTE[i%len(PALETTE)],
                    opacity=0.75))
            fig.update_layout(**PLOTLY_LAYOUT, title="Real House Price Growth (%)", height=360,
                              barmode="overlay")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "hpnom" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["hpnom"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Nominal House Price Index", height=360,
                              yaxis_type="log" if log_scale else "linear")
            st.plotly_chart(fig, use_container_width=True)

    # Equity returns
    if "eq_tr" in dff.columns:
        st.markdown('<div class="section-label">Equity Total Returns</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                eq = d["eq_tr"].dropna()
                yr = d.loc[eq.index, "year"]
                cumret = (1 + eq/100).cumprod()
                fig.add_trace(go.Scatter(x=yr, y=cumret,
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Equity Cumulative Total Return (Base=1)", height=360,
                              yaxis_type="log")
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            # Rolling 10yr average equity return
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["eq_roll10"] = d["eq_tr"].rolling(10).mean()
                fig.add_trace(go.Scatter(x=d["year"], y=d["eq_roll10"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**PLOTLY_LAYOUT, title="Equity Total Return – 10Y Rolling Avg (%)", height=360)
            st.plotly_chart(fig, use_container_width=True)

    # House-price vs credit scatter
    if "credit_gdp" in dff.columns and "hp_real_growth" in dff.columns:
        st.markdown('<div class="section-label">Credit–House Price Nexus</div>', unsafe_allow_html=True)
        scatter_data = dff[["iso","year","credit_gdp_chg","hp_real_growth",crisis_col if crisis_col else "year"]].dropna()
        if crisis_col and crisis_col in scatter_data.columns:
            scatter_data["crisis_label"] = scatter_data[crisis_col].map({1:"Crisis",0:"Normal"})
        else:
            scatter_data["crisis_label"] = "Normal"
        fig_s = go.Figure()
        symbols = {"Crisis": "x", "Normal": "circle"}
        for i, iso in enumerate(selected_countries):
            for label, sym in symbols.items():
                d_s = scatter_data[(scatter_data["iso"]==iso) & (scatter_data["crisis_label"]==label)]
                if len(d_s) == 0: continue
                fig_s.add_trace(go.Scatter(
                    x=d_s["credit_gdp_chg"], y=d_s["hp_real_growth"],
                    mode="markers", name=f"{iso} ({label})",
                    marker=dict(color=PALETTE[i%len(PALETTE)], symbol=sym, size=5, opacity=0.7),
                    customdata=d_s["year"],
                    hovertemplate=f"<b>{iso}</b> %{{customdata}}<br>ΔCredit/GDP: %{{x:.2f}}pp<br>Real HP Growth: %{{y:.2f}}%<extra></extra>"
                ))
        # Manual OLS trendline using scipy
        sd_clean = scatter_data[["credit_gdp_chg","hp_real_growth"]].dropna()
        if len(sd_clean) > 10:
            from scipy import stats as _stats
            _slope, _intercept, _r, _p, _ = _stats.linregress(sd_clean["credit_gdp_chg"], sd_clean["hp_real_growth"])
            x_line = np.linspace(sd_clean["credit_gdp_chg"].min(), sd_clean["credit_gdp_chg"].max(), 100)
            fig_s.add_trace(go.Scatter(
                x=x_line, y=_slope*x_line+_intercept,
                mode="lines", name=f"OLS (R²={_r**2:.2f})",
                line=dict(color="#f59e0b", width=2, dash="dash")
            ))
        fig_s.update_layout(**PLOTLY_LAYOUT, title="Credit Expansion vs Real House Price Growth", height=420)
        st.plotly_chart(fig_s, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — MACRO AGGREGATES
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-label">National Accounts & External Sector</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if "gdp_growth" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["gdp_growth"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**PLOTLY_LAYOUT, title="Real GDP Growth (%)", height=350)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["gdp"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="GDP (National Currency)", height=350,
                              yaxis_type="log" if log_scale else "linear")
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if "ca_gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["ca_gdp"],
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6),
                    fill="tozeroy" if len(selected_countries)==1 else None))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**PLOTLY_LAYOUT, title="Current Account / GDP (%)", height=320)
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "iy" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["iy"]*100,
                    name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**PLOTLY_LAYOUT, title="Investment / GDP (%)", height=320)
            st.plotly_chart(fig, use_container_width=True)

    # GDP per capita
    if "rgdppc" in dff.columns:
        st.markdown('<div class="section-label">Real GDP per Capita</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig.add_trace(go.Scatter(x=d["year"], y=d["rgdppc"],
                name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=2),
                hovertemplate=f"<b>{iso}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>"))
            fig = add_crisis_shading(fig, d, crisis_col)
        fig.update_layout(**PLOTLY_LAYOUT, title="Real GDP per Capita (2005 USD)", height=400,
                          yaxis_type="log" if log_scale else "linear")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 — CRISIS ANALYSIS
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-label">Financial Crisis Anatomy</div>', unsafe_allow_html=True)

    if crisis_col is None:
        st.warning("No crisis indicator column found in dataset.")
    else:
        crisis_df = dff[dff[crisis_col]==1].copy()

        # Count crises per country
        crisis_counts = (
            dff.groupby(["iso","year"])[crisis_col]
            .max().reset_index()
            .query(f"{crisis_col}==1")
            .groupby("iso")[crisis_col].sum()
            .reset_index()
            .rename(columns={crisis_col:"crisis_count","iso":"Country"})
            .sort_values("crisis_count", ascending=True)
        )

        col1, col2 = st.columns([2,1])
        with col1:
            fig = px.bar(crisis_counts, x="crisis_count", y="Country",
                         orientation="h", color="crisis_count",
                         color_continuous_scale=[[0,"#1e2d45"],[0.5,"#3b82f6"],[1,"#ef4444"]],
                         title="Financial Crisis Episodes by Country",
                         labels={"crisis_count":"Number of Crisis Years"})
            fig.update_layout(**PLOTLY_LAYOUT, height=max(300, 40*len(crisis_counts)+60),
                              showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Crisis decade distribution
            crisis_decades = crisis_df.copy()
            crisis_decades["decade"] = (crisis_decades["year"]//10*10).astype(int)
            dec_counts = crisis_decades.groupby("decade")[crisis_col].sum().reset_index()
            dec_counts.columns = ["Decade","Count"]

            fig2 = px.bar(dec_counts, x="Decade", y="Count",
                          color="Count",
                          color_continuous_scale=[[0,"#1e293b"],[1,"#ef4444"]],
                          title="Crisis Years by Decade")
            fig2.update_layout(**PLOTLY_LAYOUT, height=350, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        # Crisis episode analysis: avg macro before/during/after crisis
        if len(crisis_df) > 0:
            st.markdown('<div class="section-label">Crisis Event Study: Mean Macro Dynamics</div>', unsafe_allow_html=True)

            event_vars = [v for v in ["gdp_growth","credit_gdp_chg","inflation","hp_real_growth","ltrate"]
                          if v in dff.columns]

            if event_vars:
                # Build -5 to +5 window around each crisis start
                records = []
                for iso in selected_countries:
                    cdata = dff[dff["iso"]==iso].sort_values("year").reset_index(drop=True)
                    crisis_years = cdata[cdata[crisis_col]==1]["year"].values
                    # find crisis starts
                    starts = []
                    prev = False
                    for yr in sorted(cdata["year"].values):
                        row = cdata[cdata["year"]==yr]
                        if row[crisis_col].values[0]==1 and not prev:
                            starts.append(yr)
                        prev = row[crisis_col].values[0]==1

                    for s in starts:
                        for t in range(-5, 6):
                            yr_t = s + t
                            row = cdata[cdata["year"]==yr_t]
                            if len(row)==0: continue
                            rec = {"iso":iso, "t":t}
                            for v in event_vars:
                                rec[v] = row[v].values[0]
                            records.append(rec)

                if records:
                    ev = pd.DataFrame(records)
                    ev_mean = ev.groupby("t")[event_vars].mean().reset_index()

                    n_vars = len(event_vars)
                    fig_ev = make_subplots(rows=1, cols=n_vars, subplot_titles=event_vars)
                    for j, var in enumerate(event_vars):
                        row_data = ev_mean
                        fig_ev.add_trace(
                            go.Scatter(x=row_data["t"], y=row_data[var],
                                       mode="lines+markers",
                                       line=dict(color=PALETTE[j], width=2),
                                       marker=dict(size=6),
                                       name=var),
                            row=1, col=j+1
                        )
                        fig_ev.add_vline(x=0, line_dash="dot", line_color="#ef4444", row=1, col=j+1)
                        fig_ev.add_hline(y=0, line_dash="dot", line_color="#475569", row=1, col=j+1)

                    fig_ev.update_layout(**PLOTLY_LAYOUT, height=350,
                                         title="Event Study: Average Macro Dynamics Around Crisis Onset (t=0)",
                                         showlegend=False)
                    st.plotly_chart(fig_ev, use_container_width=True)

                    st.markdown("""
                    <div class="insight-box">
                        <div class="insight-title">🔍 Event Study Intelligence</div>
                        Event window: t = −5 (5 years pre-crisis) to t = +5 (post-crisis). 
                        The red dashed line marks crisis onset (t=0). 
                        Patterns typically show: accelerating credit growth pre-crisis, sharp GDP contraction at/after onset,
                        elevated interest rates, and declining house prices post-crisis.
                    </div>""", unsafe_allow_html=True)

        # Timeline heatmap
        st.markdown('<div class="section-label">Crisis Timeline Heatmap</div>', unsafe_allow_html=True)
        pivot = dff.groupby(["iso","year"])[crisis_col].max().unstack(fill_value=0)
        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0,"#0f172a"],[1,"#ef4444"]],
            showscale=False,
            hovertemplate="Country: %{y}<br>Year: %{x}<br>Crisis: %{z}<extra></extra>"
        ))
        heat_layout = {**PLOTLY_LAYOUT, "title": "Crisis Episodes: Country × Year",
                        "height": max(200, 30*len(pivot)+80)}
        heat_layout["yaxis"] = {**heat_layout.get("yaxis", {}), "tickfont": dict(size=10)}
        fig_heat.update_layout(**heat_layout)
        st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 6 — CROSS-COUNTRY
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-label">Cross-Country Benchmarking</div>', unsafe_allow_html=True)

    yr_select = st.slider("Select Year for Cross-Section", int(min(YEARS)), int(max(YEARS)), min(2015, int(max(YEARS))), key="cs_year")
    cs = df[df["year"]==yr_select][["iso"] + [c for c in NON_ID if c in df.columns]].dropna(subset=["iso"])

    avail_vars = [c for c in ["credit_gdp","gdp_growth","inflation","ltrate","stir","ca_gdp","money_gdp","hp_real_growth"] if c in cs.columns]

    if len(avail_vars) >= 2:
        x_var = st.selectbox("X Variable", avail_vars, index=0, key="cs_x")
        y_var = st.selectbox("Y Variable", avail_vars, index=min(1,len(avail_vars)-1), key="cs_y")
        size_var = st.selectbox("Bubble Size", ["(none)"] + avail_vars, key="cs_size")

        plot_data = cs[["iso", x_var, y_var]].dropna()
        if size_var != "(none)" and size_var in cs.columns:
            plot_data = cs[["iso", x_var, y_var, size_var]].dropna()
            plot_data = plot_data[plot_data[size_var] > 0]
            fig = px.scatter(plot_data, x=x_var, y=y_var, size=size_var,
                             text="iso", color="iso", color_discrete_sequence=PALETTE,
                             title=f"Cross-Country: {x_var} vs {y_var} ({yr_select})",
                             size_max=50)
        else:
            fig = px.scatter(plot_data, x=x_var, y=y_var,
                             text="iso", color="iso", color_discrete_sequence=PALETTE,
                             title=f"Cross-Country: {x_var} vs {y_var} ({yr_select})")

        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(**PLOTLY_LAYOUT, height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Bar race-style: latest values
    st.markdown('<div class="section-label">Latest Values Ranking</div>', unsafe_allow_html=True)
    rank_var = st.selectbox("Variable to Rank", avail_vars, key="rank_var")
    latest_cs = df.groupby("iso")[rank_var].last().dropna().sort_values(ascending=False).reset_index()
    latest_cs.columns = ["Country", rank_var]

    fig_rank = px.bar(latest_cs, x=rank_var, y="Country", orientation="h",
                       color=rank_var,
                       color_continuous_scale=[[0,"#1e3a5f"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                       title=f"Latest {rank_var} — All Countries")
    fig_rank.update_layout(**PLOTLY_LAYOUT, height=max(300, 28*len(latest_cs)+80),
                           showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_rank, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 7 — CORRELATIONS
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-label">Correlation Structure & Statistical Relationships</div>', unsafe_allow_html=True)

    corr_vars = [c for c in ["credit_gdp","gdp_growth","inflation","ltrate","stir",
                              "ca_gdp","money_gdp","hp_real_growth","loan_growth","eq_tr","iy"] if c in dff.columns]

    if len(corr_vars) >= 3:
        corr_matrix = dff[corr_vars].corr()
        labels = corr_vars

        fig_corr = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=labels, y=labels,
            colorscale=[[0,"#ef4444"],[0.5,"#0f172a"],[1,"#3b82f6"]],
            zmid=0, zmin=-1, zmax=1,
            text=np.round(corr_matrix.values,2),
            texttemplate="%{text}",
            textfont=dict(size=9),
            hovertemplate="%{y} × %{x}: %{z:.3f}<extra></extra>"
        ))
        fig_corr.update_layout(**PLOTLY_LAYOUT, title="Correlation Matrix — Key Variables", height=520)
        st.plotly_chart(fig_corr, use_container_width=True)

    # Rolling correlation
    if "credit_gdp" in dff.columns and "gdp_growth" in dff.columns:
        st.markdown('<div class="section-label">Rolling 10-Year Correlation: Credit/GDP vs GDP Growth</div>', unsafe_allow_html=True)
        fig_roll = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year").copy()
            d["roll_corr"] = d["credit_gdp"].rolling(10).corr(d["gdp_growth"])
            fig_roll.add_trace(go.Scatter(x=d["year"], y=d["roll_corr"],
                name=iso, mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
            fig_roll = add_crisis_shading(fig_roll, d, crisis_col)
        fig_roll.add_hline(y=0, line_dash="dot", line_color="#475569")
        fig_roll.update_layout(**PLOTLY_LAYOUT, title="Rolling 10Y Corr: Credit/GDP vs GDP Growth", height=360, yaxis_range=[-1,1])
        st.plotly_chart(fig_roll, use_container_width=True)

    # Scatter with OLS
    if len(corr_vars) >= 2:
        st.markdown('<div class="section-label">Bivariate Scatter with OLS Fit</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            xv = st.selectbox("X", corr_vars, index=0, key="biv_x")
        with c2:
            yv = st.selectbox("Y", corr_vars, index=min(1,len(corr_vars)-1), key="biv_y")

        biv = dff[["iso","year",xv,yv]].dropna()
        if len(biv) > 10:
            from scipy import stats
            slope, intercept, r, p, se = stats.linregress(biv[xv], biv[yv])
            x_line = np.linspace(biv[xv].min(), biv[xv].max(), 100)
            y_line = slope * x_line + intercept

            fig_biv = go.Figure()
            for i, iso in enumerate(selected_countries):
                d_biv = biv[biv["iso"]==iso]
                fig_biv.add_trace(go.Scatter(x=d_biv[xv], y=d_biv[yv],
                    mode="markers", name=iso,
                    marker=dict(color=PALETTE[i%len(PALETTE)], size=5, opacity=0.7),
                    customdata=d_biv["year"],
                    hovertemplate=f"<b>{iso}</b> %{{customdata}}<br>{xv}: %{{x:.2f}}<br>{yv}: %{{y:.2f}}<extra></extra>"))
            fig_biv.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
                name=f"OLS (r={r:.2f}, p={p:.3f})",
                line=dict(color="#f59e0b", width=2, dash="dash")))
            fig_biv.update_layout(**PLOTLY_LAYOUT, title=f"{xv} vs {yv} — OLS: β={slope:.3f}, R²={r**2:.3f}", height=420)
            st.plotly_chart(fig_biv, use_container_width=True)

            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">📐 OLS Regression Result</div>
                <b>{yv} = {intercept:.3f} + {slope:.3f} × {xv}</b><br>
                R² = {r**2:.3f} &nbsp;·&nbsp; p-value = {p:.4f} &nbsp;·&nbsp; N = {len(biv):,}
                {"— statistically significant at 5% level" if p < 0.05 else "— NOT significant at 5% level"}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 8 — DATA EXPLORER
# ══════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-label">Raw Data & Variable Catalogue</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("**Dataset Dimensions**")
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">📋 Metadata</div>
            <b>Observations:</b> {len(df_raw):,}<br>
            <b>Variables:</b> {len(df_raw.columns)}<br>
            <b>Countries:</b> {len(COUNTRIES)} ({', '.join(COUNTRIES)})<br>
            <b>Time span:</b> {int(min(YEARS))} – {int(max(YEARS))}<br>
            <b>Numeric variables:</b> {len(NUM_COLS)}<br>
            <b>Source:</b> Jordà, Schularick & Taylor (2017, 2022) — macrohistory.net
        </div>""", unsafe_allow_html=True)

    with col2:
        # Variable coverage
        coverage = (df_raw.notna().sum() / len(df_raw) * 100).sort_values(ascending=False)
        fig_cov = go.Figure(go.Bar(
            x=coverage.values[:30], y=coverage.index[:30],
            orientation="h",
            marker=dict(color=coverage.values[:30],
                       colorscale=[[0,"#1e3a5f"],[1,"#3b82f6"]]),
            text=[f"{v:.0f}%" for v in coverage.values[:30]],
            textposition="outside", textfont=dict(size=8)
        ))
        _cov_layout = {**PLOTLY_LAYOUT}
        _cov_layout["xaxis"] = {**_cov_layout.get("xaxis", {}), "range": [0, 115]}
        fig_cov.update_layout(**_cov_layout, title="Variable Coverage (% non-null, top 30)",
                              height=600, showlegend=False)
        st.plotly_chart(fig_cov, use_container_width=True)

    st.markdown('<div class="section-label">Variable Summary Statistics</div>', unsafe_allow_html=True)
    summary_cols = st.multiselect("Select variables for summary", NON_ID[:20], default=NON_ID[:8])
    if summary_cols:
        desc = dff[summary_cols].describe().T
        desc.index.name = "Variable"
        desc = desc.round(3)
        st.dataframe(desc.style.background_gradient(cmap="Blues", subset=["mean","std"])
                     .format("{:.3f}"), use_container_width=True)

    st.markdown('<div class="section-label">Filtered Data Table</div>', unsafe_allow_html=True)
    show_cols = st.multiselect("Columns to display", ["iso","year"] + NON_ID,
                               default=["iso","year","gdp_growth","credit_gdp","inflation","ltrate"] if "gdp_growth" in dff.columns else ["iso","year"])
    page_size = 50
    page = st.number_input("Page", 1, max(1, len(dff)//page_size+1), 1)
    display_df = dff[show_cols].sort_values(["iso","year"]).iloc[(page-1)*page_size:page*page_size]
    st.dataframe(display_df.style.format({c:"{:.2f}" for c in display_df.select_dtypes(float).columns}),
                 use_container_width=True, height=400)

    # Download
    @st.cache_data
    def to_csv(d): return d.to_csv(index=False).encode()
    csv_data = to_csv(dff[show_cols].sort_values(["iso","year"]))
    st.download_button("⬇ Download filtered data as CSV", csv_data, "jst_filtered.csv", "text/csv")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
    JST MACROHISTORY DASHBOARD &nbsp;·&nbsp;
    DATASET R6 &nbsp;·&nbsp;
    JORDÀ · SCHULARICK · TAYLOR &nbsp;·&nbsp;
    macrohistory.net &nbsp;·&nbsp;
    17 ECONOMIES · 1870–PRESENT
    <br style="margin-bottom:6px;">
    © 2026 ADIYAT COTO &nbsp;·&nbsp; ALL RIGHTS RESERVED
</div>""", unsafe_allow_html=True)
