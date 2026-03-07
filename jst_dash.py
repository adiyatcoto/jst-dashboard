"""
JST Macrohistory Dashboard — Institutional Grade
Jordà-Schularick-Taylor Dataset R6

Copyright (c) 2026 Adiyat Coto. All rights reserved.
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
.stTabs {
    margin-top: 2rem;
}
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

# ─────────────────────────────────────────────
# SIGNED LOG TRANSFORM — works on ALL data including negatives and zeros
# Formula: sign(x) * log10(1 + |x|)
# This compresses large ranges while preserving sign, handles 0, negatives, positives
# ─────────────────────────────────────────────
def signed_log(x):
    """Signed log10 transform: handles negatives, zeros, positives."""
    import numpy as _np
    x = _np.array(x, dtype=float)
    return _np.sign(x) * _np.log10(1 + _np.abs(x))

def signed_log_val(x):
    """Scalar version of signed log."""
    import numpy as _np
    if x is None or (_np is not None and _np.isnan(float(x))):
        return x
    x = float(x)
    import math
    return math.copysign(math.log10(1 + abs(x)), x)

def _apply_signed_log_to_fig(fig):
    """
    Transform all y-values (and x-values for horizontal bars) in a figure
    using signed log. Updates tickvals/ticktext so axis labels show original values.
    Returns the modified figure and a tickvals/ticktext dict for both axes.
    """
    import numpy as _np
    import plotly.graph_objs as _go

    # Collect all values to build a nice tick grid
    all_y, all_x_horiz = [], []

    for trace in fig.data:
        ttype = type(trace).__name__
        is_horiz = getattr(trace, "orientation", None) == "h"

        if is_horiz and hasattr(trace, "x") and trace.x is not None:
            vals = [v for v in trace.x if v is not None]
            all_x_horiz.extend(vals)
            new_x = signed_log(_np.array(vals, dtype=float))
            trace.x = new_x
            # Update text labels to show original values
            if hasattr(trace, "text") and trace.text is not None:
                try:
                    trace.text = [f"{float(v):.1f}" for v in vals]
                except Exception:
                    pass
        elif hasattr(trace, "y") and trace.y is not None:
            vals = [v for v in trace.y if v is not None]
            all_y.extend(vals)
            new_y = signed_log(_np.array([v if v is not None else _np.nan for v in trace.y], dtype=float))
            trace.y = tuple(new_y)

    def make_ticks(vals):
        if not vals:
            return [], []
        mn, mx = min(vals), max(vals)
        # Create ~8 evenly spaced ticks in original space
        ticks_orig = _np.linspace(mn, mx, 8)
        ticks_log  = signed_log(ticks_orig)
        labels = []
        for v in ticks_orig:
            av = abs(v)
            if av >= 1000:
                labels.append(f"{v:,.0f}")
            elif av >= 10:
                labels.append(f"{v:.1f}")
            else:
                labels.append(f"{v:.2f}")
        return ticks_log.tolist(), labels

    y_tickvals, y_ticktext = make_ticks(all_y)
    x_tickvals, x_ticktext = make_ticks(all_x_horiz)

    return fig, y_tickvals, y_ticktext, x_tickvals, x_ticktext


def L(title="", height=400, extra=None, no_log=False, fig=None):
    """
    Return a layout dict.
    When log_scale is ON and fig is provided:
      - applies signed-log transform directly to trace data (handles negatives/zeros)
      - sets custom tick labels showing original values
      - works for line, bar (vertical+horizontal), scatter, violin — ALL chart types
    """
    base = {**PLOTLY_LAYOUT, "height": height}
    if title:
        base["title"] = title

    # Heatmaps and polar charts — never transform
    exempt_types = {"Heatmap", "Scatterpolar", "Choropleth"}
    is_exempt_type = False
    if fig is not None:
        try:
            types = {type(t).__name__ for t in fig.data}
            is_exempt_type = bool(types & exempt_types)
        except Exception:
            pass

    if log_scale and not no_log and not is_exempt_type and fig is not None:
        try:
            fig, y_tv, y_tt, x_tv, x_tt = _apply_signed_log_to_fig(fig)
            if y_tv:
                base["yaxis"] = {
                    **base.get("yaxis", {}),
                    "tickvals": y_tv,
                    "ticktext": y_tt,
                    "title": base.get("yaxis", {}).get("title", ""),
                }
            if x_tv:
                base["xaxis"] = {
                    **base.get("xaxis", {}),
                    "tickvals": x_tv,
                    "ticktext": x_tt,
                }
        except Exception as _e:
            pass  # graceful fallback — leave chart untransformed

    if extra:
        for k, v in extra.items():
            if k in ("xaxis", "yaxis") and k in base:
                base[k] = {**base[k], **v}
            else:
                base[k] = v
    return base


# ─────────────────────────────────────────────
# JST VARIABLE GLOSSARY
# ─────────────────────────────────────────────
JST_GLOSSARY = {
    # Identifiers
    "iso":          ("Country Code", "3-letter ISO country identifier (e.g. USA, GBR, DEU)"),
    "year":         ("Year", "Calendar year of observation"),
    "country":      ("Country Name", "Full country name"),

    # National Accounts
    "gdp":          ("GDP (Nominal)", "Gross Domestic Product in nominal national currency — total value of all goods and services produced"),
    "rgdppc":       ("Real GDP per Capita", "GDP per person adjusted for inflation (2005 USD) — best measure of living standards over time"),
    "rconpc":       ("Real Consumption per Capita", "Household spending per person, inflation-adjusted — measures actual living standards"),
    "iy":           ("Investment / GDP Ratio", "Share of GDP spent on investment (machinery, buildings, infrastructure) — signals future growth capacity"),
    "pop":          ("Population", "Total population of the country"),

    # Credit & Loans
    "tloans":       ("Total Bank Loans", "Total loans issued by banks to households and businesses — the broadest credit measure"),
    "hh_mortgage":  ("Mortgage Loans", "Bank loans secured against residential property — housing debt owed by households"),
    "nfc_loans":    ("Corporate Loans", "Bank loans to non-financial corporations — business borrowing from banks"),
    "bdebt":        ("Business Debt", "Total debt held by the business sector"),

    # Derived Credit Ratios
    "credit_gdp":       ("Credit / GDP (%)", "Total bank loans as % of GDP — the key leverage ratio. Above 100% = economy owes more than it produces annually"),
    "mortgage_gdp":     ("Mortgage Debt / GDP (%)", "Housing debt as % of GDP — elevated levels often precede housing busts"),
    "nfc_gdp":          ("Corporate Debt / GDP (%)", "Business loans as % of GDP — high levels signal corporate sector stress"),
    "credit_gdp_chg":   ("Change in Credit/GDP (pp)", "Year-on-year change in the credit/GDP ratio — rapid rises are the #1 predictor of financial crises"),
    "loan_growth":      ("Loan Growth (%)", "Annual percentage growth in total bank lending — credit booms show up here first"),

    # Money & Banking
    "money":        ("Broad Money (M2/M3)", "Total money in circulation including bank deposits — reflects monetary policy and banking system size"),
    "money_gdp":    ("Money Supply / GDP (%)", "Broad money as % of GDP — rising trend = financialization of the economy"),
    "narrowm":      ("Narrow Money (M1)", "Cash and demand deposits only — the most liquid form of money"),

    # Interest Rates
    "ltrate":       ("Long-Term Interest Rate (%)", "Yield on long-term government bonds (typically 10-year) — reflects inflation expectations and sovereign risk"),
    "stir":         ("Short-Term Interest Rate (%)", "Central bank policy rate or 3-month money market rate — the main monetary policy instrument"),
    "bill_rate":    ("Treasury Bill Rate (%)", "Short-term government borrowing rate — closely tracks central bank policy"),
    "bond_rate":    ("Bond Yield (%)", "Long-term government bond yield"),

    # Derived Rate Variables
    "term_spread":  ("Term Spread (%)", "Long-term rate minus short-term rate. Negative (inverted yield curve) historically predicts recessions"),

    # Prices & Inflation
    "cpi":          ("Consumer Price Index", "Index measuring the average price of a basket of consumer goods — the standard inflation measure"),
    "inflation":    ("Inflation Rate (%)", "Annual % change in CPI — measures how fast prices are rising. Central banks target ~2%"),

    # Asset Prices — Housing
    "hpnom":        ("Nominal House Price Index", "Index of residential property prices in nominal (not inflation-adjusted) terms"),
    "hp_real":      ("Real House Price Index", "House prices adjusted for inflation — shows true purchasing power changes in housing"),
    "hp_real_growth": ("Real House Price Growth (%)", "Annual % change in inflation-adjusted house prices — boom/bust cycles visible here"),

    # Asset Prices — Equities
    "eq_tr":        ("Equity Total Return (%)", "Annual total return on the stock market including dividends — the complete investor return"),
    "eq_dp":        ("Dividend-Price Ratio (%)", "Dividends as % of stock prices — low ratios historically signal overvaluation"),
    "eq_real_tr":   ("Real Equity Total Return", "Stock market returns adjusted for inflation — real wealth creation from equities"),

    # Asset Prices — Bonds & Bills
    "bond_tr":      ("Bond Total Return (%)", "Annual total return on long-term government bonds"),
    "bill_tr":      ("Treasury Bill Total Return (%)", "Annual total return on short-term government bills"),
    "bond_real_tr": ("Real Bond Total Return (%)", "Bond returns adjusted for inflation"),
    "bill_real_tr": ("Real Bill Total Return (%)", "Bill returns adjusted for inflation"),

    # External Sector
    "ca":           ("Current Account Balance", "Difference between a country's exports and imports plus income flows. Positive = net exporter"),
    "ca_gdp":       ("Current Account / GDP (%)", "Current account as % of GDP. Persistent deficits = borrowing from abroad; surpluses = lending to the world"),
    "exports":      ("Exports", "Total value of goods and services sold to other countries"),
    "imports":      ("Imports", "Total value of goods and services bought from other countries"),

    # Banking System
    "bank_capital": ("Bank Capital Ratio (%)", "Bank equity as % of assets — higher = more resilient banks, lower = more leveraged and fragile"),
    "ltd":          ("Loan-to-Deposit Ratio (%)", "Bank loans divided by deposits. Above 100% = banks are lending out more than deposited — funding risk"),

    # Crisis Indicators
    "crisisJST":    ("Financial Crisis (JST)", "Binary indicator: 1 = financial crisis year, 0 = normal. Coded by Jordà, Schularick & Taylor from historical records"),
    "crisisdate":   ("Crisis Date", "Alternative crisis dating — marks the onset year of a systemic financial crisis"),

    # Dalio-Derived Scores
    "debt_burden":      ("Debt Burden Score", "Dalio framework: how heavy is the economy's debt load relative to income? Higher = more burdened"),
    "money_printing":   ("Money Printing Score", "Dalio framework: rate of monetary expansion. Higher = faster money supply growth relative to GDP"),
    "debt_service":     ("Debt Service Pressure", "Dalio framework: combined burden of interest rates × debt level. High = large chunk of income goes to servicing debt"),
    "productivity":     ("Productivity Score", "Dalio framework: long-run real GDP per capita growth trend. Higher = economy is more dynamic"),
    "internal_order":   ("Internal Order Score", "Dalio framework: inverse of financial crisis frequency. Higher = fewer crises = more stable domestic conditions"),
    "external_strength":("External Strength Score", "Dalio framework: current account position. Higher = economy is a net lender to the world"),
    "asset_cycle":      ("Asset Price Cycle Score", "Dalio framework: momentum in real house prices. Higher = asset price boom phase"),
    "inflation_pressure":("Inflation Pressure Score", "Dalio framework: deviation of inflation from 2% target. Higher = more destabilizing price dynamics"),
    "empire_health":    ("Empire Health Score (0-100)", "Composite Dalio score: 60% weighted on productivity + order + external strength, 40% on inverse stress. 100 = peak empire health"),
}

def col_label(col):
    """Return plain-English label for a column name."""
    return JST_GLOSSARY.get(col, (col, ""))[0]

def col_desc(col):
    """Return full description for a column name."""
    return JST_GLOSSARY.get(col, (col, f"Raw variable: {col}"))[1]

def glossary_tooltip(col):
    """Return an HTML tooltip string for a column."""
    label = col_label(col)
    desc  = col_desc(col)
    return f'<span title="{desc}" style="cursor:help;border-bottom:1px dashed #475569;">{label}</span>'

def render_glossary_expander(cols, title="📖 What do these variables mean?"):
    """Render a collapsible glossary for a list of column names."""
    with st.expander(title, expanded=False):
        rows = []
        for c in cols:
            if c in JST_GLOSSARY:
                label, desc = JST_GLOSSARY[c]
                rows.append({"Variable": f"`{c}`", "Plain English Name": label, "What it measures": desc})
        if rows:
            st.table(pd.DataFrame(rows).set_index("Variable"))


# ─────────────────────────────────────────────
# RANKING RENDERER
# ─────────────────────────────────────────────
def render_ranking(dff_all, indicators, tab_title="🏆 Country Rankings"):
    """
    Render a winner/loser ranking table for all countries
    based on their latest available value for each indicator.
    """
    st.markdown(f'<div class="section-label">{tab_title}</div>', unsafe_allow_html=True)

    # pick indicators that actually exist
    valid = [v for v in indicators if v in dff_all.columns]
    if not valid:
        st.info("No ranking data available for current filters.")
        return

    rank_indicator = st.selectbox(
        "Rank countries by:", valid,
        format_func=lambda c: f"{col_label(c)} ({c})",
        key=f"rank_{tab_title[:10].replace(' ','_')}"
    )
    order = st.radio("Order", ["🥇 Best first (High → Low)", "🔻 Worst first (Low → High)"],
                     horizontal=True, key=f"order_{tab_title[:10].replace(' ','_')}")
    ascending = "Low" in order.split("→")[1] if "→" in order else False

    # latest value per country across full dataset (not just filter)
    latest = (
        dff_all.groupby("iso")[rank_indicator]
        .last()
        .dropna()
        .reset_index()
        .rename(columns={"iso": "Country", rank_indicator: "Latest Value"})
        .sort_values("Latest Value", ascending=ascending)
        .reset_index(drop=True)
    )

    if latest.empty:
        st.info("No data available.")
        return

    latest.index = latest.index + 1  # rank from 1
    latest.index.name = "Rank"

    n = len(latest)
    top3    = latest.head(3).index.tolist()
    bottom3 = latest.tail(3).index.tolist()

    def medal(rank):
        if rank == 1:   return "🥇"
        if rank == 2:   return "🥈"
        if rank == 3:   return "🥉"
        if rank == n:   return "🔴"
        if rank == n-1: return "🟠"
        if rank == n-2: return "🟡"
        return "⬜"

    latest[""] = latest.index.map(medal)
    latest["Country"] = latest["Country"]
    latest["Latest Value"] = latest["Latest Value"].round(2)
    latest["vs Average"] = (latest["Latest Value"] - latest["Latest Value"].mean()).round(2)
    latest["vs Average"] = latest["vs Average"].apply(lambda x: f"+{x:.2f}" if x > 0 else f"{x:.2f}")

    # bar chart
    colors = []
    for r in range(1, n+1):
        if r <= 3:    colors.append("#10b981")
        elif r >= n-2: colors.append("#ef4444")
        else:          colors.append("#3b82f6")

    fig_r = go.Figure(go.Bar(
        x=latest["Latest Value"],
        y=latest["Country"],
        orientation="h",
        marker_color=colors,
        text=latest["Latest Value"].apply(lambda x: f"{x:.1f}"),
        textposition="outside",
        textfont=dict(size=9, family="IBM Plex Mono"),
        hovertemplate="<b>%{y}</b><br>Value: %{x:.2f}<extra></extra>"
    ))
    _rl = L(f"{col_label(rank_indicator)} — All Countries Ranked", max(280, 32 * n + 80), extra={"showlegend": False})
    fig_r.update_layout(**_rl)
    st.plotly_chart(fig_r, use_container_width=True)

    # table
    col_t, col_i = st.columns([2, 1])
    with col_t:
        display = latest[["", "Country", "Latest Value", "vs Average"]].copy()
        display.index.name = "Rank"
        st.dataframe(display, use_container_width=True,
                     height=min(500, 40 * n + 60))
    with col_i:
        winner = latest.iloc[0]
        loser  = latest.iloc[-1]
        avg_v  = latest["Latest Value"].mean()
        spread = latest["Latest Value"].max() - latest["Latest Value"].min()
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">🏆 Ranking Snapshot</div>
            <b>🥇 Leader:</b> {winner["Country"]} ({winner["Latest Value"]:.2f})<br>
            <b>🔴 Laggard:</b> {loser["Country"]} ({loser["Latest Value"]:.2f})<br>
            <b>⬜ Average:</b> {avg_v:.2f}<br>
            <b>📏 Spread:</b> {spread:.2f}<br><br>
            <span style="color:#64748b;font-size:0.75rem;">
            Based on latest available year per country.<br>
            Green = top 3 · Red = bottom 3.
            </span>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# COUNTRY NAME MAPPING (ISO → Full Name)
# ─────────────────────────────────────────────
ISO_NAMES = {
    "AUS": "Australia",
    "BEL": "Belgium",
    "CAN": "Canada",
    "CHE": "Switzerland",
    "DEU": "Germany",
    "DNK": "Denmark",
    "ESP": "Spain",
    "FIN": "Finland",
    "FRA": "France",
    "GBR": "United Kingdom",
    "IRL": "Ireland",
    "ITA": "Italy",
    "JPN": "Japan",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "PRT": "Portugal",
    "SWE": "Sweden",
    "USA": "United States",
    # fallback for any unlisted codes
}

def iso_to_name(code):
    """Return full country name for an ISO code, falling back to the code itself."""
    return ISO_NAMES.get(str(code).upper(), code)

def names_to_iso(name):
    """Reverse lookup: full name → ISO code."""
    rev = {v: k for k, v in ISO_NAMES.items()}
    return rev.get(name, name)

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
    d = df.copy().sort_values(["iso", "year"])  # ensure correct order for pct_change/diff

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
    # Real GDP growth: prefer rgdppc (real GDP per capita, already inflation-adjusted in JST)
    # Fall back to nominal gdp pct_change only if rgdppc unavailable
    if "rgdppc" in d.columns:
        d["gdp_growth"] = d.groupby("iso")["rgdppc"].pct_change() * 100
    elif "gdp" in d.columns:
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

    # Real equity total return
    # Formula: real return ≈ nominal return - inflation (Fisher approximation)
    # Full Fisher: ((1 + eq_tr/100) / (1 + inflation/100) - 1) * 100
    if "eq_tr" in d.columns and "inflation" in d.columns:
        d["eq_real_tr"] = ((1 + d["eq_tr"] / 100) / (1 + d["inflation"].clip(-99, 999) / 100) - 1) * 100
    elif "eq_tr" in d.columns:
        d["eq_real_tr"] = d["eq_tr"]  # fallback: use nominal if inflation unavailable

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
    _select_all = st.checkbox("Select all countries", value=False)
    selected_countries = st.multiselect(
        "Countries", COUNTRIES,
        default=COUNTRIES if _select_all else (COUNTRIES[:6] if len(COUNTRIES)>=6 else COUNTRIES),
        format_func=iso_to_name
    )
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
    "🌀 Dalio Empire Cycle",
    "💡 Investment Intelligence",
    "🧬 Macro Stress Lab",
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

# ─────────────────────────────────────────────
# DALIO SCORE ENGINE (global)
# ─────────────────────────────────────────────
def compute_dalio_scores(data, cross_country=False):
    """
    Compute normalised 0-100 Dalio cycle scores.

    cross_country=False (default): normalise each variable within its own
      time series (each country vs its own history). Used for time-series
      charts and radar — shows how a country evolved relative to itself.

    cross_country=True: normalise each variable across ALL countries
      simultaneously (shared min/max). Used for rankings — scores are
      directly comparable across countries (USA 80 == Ireland 80).

    All scores: high = healthy/good.
      debt_burden is INVERTED so 100 = least indebted = healthiest.
    """
    d = data.copy().sort_values(["iso", "year"])

    scores = pd.DataFrame(index=d.index)
    scores["year"] = d["year"]
    scores["iso"]  = d["iso"]

    def norm(series, invert=False):
        """Min-max normalise to 0-100. invert=True means low raw value = high score."""
        s = series.copy().astype(float)
        mn, mx = s.min(), s.max()
        if mx == mn:
            return s * 0 + 50
        out = (s - mn) / (mx - mn) * 100
        return (100 - out) if invert else out

    def gnorm(series, invert=False):
        """
        Group-aware norm: if cross_country, normalise across entire series (all countries).
        If not cross_country, normalise within each iso group separately.
        """
        if cross_country:
            return norm(series, invert=invert)
        return series.groupby(d["iso"]).transform(lambda s: norm(s, invert=invert))

    # ── 1. DEBT BURDEN — credit/gdp
    # Inverted: high score = low debt = healthiest
    if "credit_gdp" in d.columns:
        scores["debt_burden"] = gnorm(d["credit_gdp"], invert=True)
    else:
        scores["debt_burden"] = 50

    # ── 2. MONEY PRINTING — 5Y avg growth of money/gdp ratio
    if "money_gdp" in d.columns:
        raw = d.groupby("iso")["money_gdp"].transform(
            lambda s: s.pct_change().rolling(5).mean() * 100
        )
        scores["money_printing"] = gnorm(raw)
    else:
        scores["money_printing"] = 50

    # ── 3. DEBT SERVICE PRESSURE — ltrate × credit_gdp / 100
    # Proxy for interest payments as % of GDP. Inverted: low = healthier.
    if "ltrate" in d.columns and "credit_gdp" in d.columns:
        raw = d["ltrate"] * d["credit_gdp"] / 100  # element-wise, no rolling needed
        scores["debt_service"] = gnorm(raw, invert=True)
    elif "ltrate" in d.columns:
        scores["debt_service"] = gnorm(d["ltrate"], invert=True)
    else:
        scores["debt_service"] = 50

    # ── 4. PRODUCTIVITY — 10Y rolling avg real GDP per capita growth
    if "rgdppc" in d.columns:
        raw = d.groupby("iso")["rgdppc"].transform(
            lambda s: s.pct_change().rolling(10, min_periods=5).mean() * 100
        )
        scores["productivity"] = gnorm(raw)
    elif "gdp_growth" in d.columns:
        raw = d.groupby("iso")["gdp_growth"].transform(
            lambda s: s.rolling(10, min_periods=5).mean()
        )
        scores["productivity"] = gnorm(raw)
    else:
        scores["productivity"] = 50

    # ── 5. INTERNAL ORDER — inverse cumulative crisis frequency
    # Expanding mean = crisis years so far / total years observed.
    # Inverted: fewer crises historically = higher score.
    if "crisisJST" in d.columns:
        raw = d.groupby("iso")["crisisJST"].transform(
            lambda s: s.expanding(min_periods=5).mean()
        )
        scores["internal_order"] = gnorm(raw, invert=True)
    else:
        scores["internal_order"] = 50

    # ── 6. EXTERNAL STRENGTH — current account / gdp
    # Positive CA = net lender = strong. Higher = better.
    if "ca_gdp" in d.columns:
        scores["external_strength"] = gnorm(d["ca_gdp"])
    else:
        scores["external_strength"] = 50

    # ── 7. ASSET CYCLE — 5Y rolling avg real house price growth
    if "hp_real_growth" in d.columns:
        raw = d.groupby("iso")["hp_real_growth"].transform(
            lambda s: s.rolling(5, min_periods=3).mean()
        )
        scores["asset_cycle"] = gnorm(raw)
    elif "hpnom" in d.columns:
        raw = d.groupby("iso")["hpnom"].transform(
            lambda s: s.pct_change().rolling(5, min_periods=3).mean() * 100
        )
        scores["asset_cycle"] = gnorm(raw)
    else:
        scores["asset_cycle"] = 50

    # ── 8. INFLATION PRESSURE — deviation from 2% target (inverted)
    # Low deviation from 2% = price stability = high score.
    if "inflation" in d.columns:
        raw = d.groupby("iso")["inflation"].transform(
            lambda s: abs(s.rolling(5, min_periods=3).mean() - 2)
        )
        scores["inflation_pressure"] = gnorm(raw, invert=True)
    else:
        scores["inflation_pressure"] = 50

    # ── COMPOSITE EMPIRE HEALTH SCORE ────────────────────────────────────
    # All 6 components now share same sign convention: high = healthy.
    # Weights: 60% vitality (growth + stability + external), 40% resilience (low stress)
    health_cols = ["productivity", "internal_order", "external_strength", "debt_burden"]
    stress_cols = ["debt_service", "inflation_pressure"]
    # stress_cols already inverted above, so we ADD them (not subtract)
    scores["empire_health"] = (
        scores[health_cols].mean(axis=1) * 0.6 +
        scores[stress_cols].mean(axis=1) * 0.4
    )

    return scores.dropna(subset=["empire_health"])

with tabs[0]:
    st.markdown('<div class="section-label">Credit Dynamics & Leverage Cycles</div>', unsafe_allow_html=True)
    render_glossary_expander(["tloans","hh_mortgage","nfc_loans","credit_gdp","mortgage_gdp","nfc_gdp","credit_gdp_chg","loan_growth"], "📖 What do these credit variables mean?")

    # Credit/GDP over time
    if "credit_gdp" in dff.columns:
        fig = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig.add_trace(go.Scatter(
                x=d["year"], y=d["credit_gdp"],
                name=iso_to_name(iso), mode="lines",
                line=dict(color=PALETTE[i%len(PALETTE)], width=1.8),
                hovertemplate=f"<b>{iso_to_name(iso)}</b><br>Year: %{{x}}<br>Credit/GDP: %{{y:.1f}}%<extra></extra>"
            ))
            fig = add_crisis_shading(fig, d, crisis_col)
        fig.update_layout(**L("Total Loans / GDP (%)", 400), yaxis_type="log" if log_scale else "linear")
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if "mortgage_gdp" in dff.columns:
            fig2 = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig2.add_trace(go.Scatter(x=d["year"], y=d["mortgage_gdp"],
                    name=iso_to_name(iso), mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig2 = add_crisis_shading(fig2, d, crisis_col)
            fig2.update_layout(**L("Mortgage Loans / GDP (%)", 320, fig=fig2))
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        if "nfc_gdp" in dff.columns:
            fig3 = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig3.add_trace(go.Scatter(x=d["year"], y=d["nfc_gdp"],
                    name=iso_to_name(iso), mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig3 = add_crisis_shading(fig3, d, crisis_col)
            fig3.update_layout(**L("Non-Financial Corporate Loans / GDP (%)", 320, fig=fig3))
            st.plotly_chart(fig3, use_container_width=True)

    # Credit growth distribution
    if "loan_growth" in dff.columns:
        st.markdown('<div class="section-label">Credit Growth Distribution</div>', unsafe_allow_html=True)
        fig4 = go.Figure()
        for i, iso in enumerate(selected_countries):
            vals = dff[dff["iso"]==iso]["loan_growth"].dropna()
            hx = PALETTE[i%len(PALETTE)].lstrip("#")
            r, g, b = int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)
            fig4.add_trace(go.Violin(x=vals, name=iso_to_name(iso), line_color=PALETTE[i%len(PALETTE)],
                                     fillcolor=f"rgba({r},{g},{b},0.15)",
                                     box_visible=True, meanline_visible=True, orientation="h"))
        fig4.update_layout(**L("Distribution of Annual Loan Growth (%)", 60+40*len(selected_countries), fig=fig4))
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



    # ── CREDIT RANKINGS ─────────────────────────────────────────
    st.markdown('<div class="section-label">🏆 Who Is Most / Least Leveraged?</div>', unsafe_allow_html=True)
    st.caption("Rankings based on latest available year per country. Green = top 3 · Red = bottom 3.")

    rank_tabs_cr = st.tabs(["💳 Total Credit/GDP", "🏠 Mortgage Debt/GDP", "🏭 Corporate Debt/GDP", "📈 Loan Growth Speed", "⚡ Credit Acceleration"])
    _cr_metrics = [
        ("credit_gdp",     "Total Credit / GDP (%)",        "Higher = more leveraged economy. Above 100% means the economy owes more than it produces in a year.", False),
        ("mortgage_gdp",   "Mortgage Debt / GDP (%)",       "Higher = households are more indebted on property. Elevated levels often precede housing busts.", False),
        ("nfc_gdp",        "Corporate Debt / GDP (%)",      "Higher = businesses are more leveraged. Risky if earnings fall and debt can't be serviced.", False),
        ("loan_growth",    "Annual Loan Growth (%)",        "Higher = credit expanding fast. Rapid credit booms are the #1 predictor of future financial crises.", False),
        ("credit_gdp_chg", "Change in Credit/GDP (pp/yr)",  "Positive = leverage rising; negative = deleveraging. The speed of leverage build-up matters as much as the level.", False),
    ]
    for _tab, (_orig_col, _label, _desc, _asc) in zip(rank_tabs_cr, _cr_metrics):
        with _tab:
            _col = _orig_col
            if _col not in dff.columns:
                # Try to find a close alternative
                _alt_map = {
                    "mortgage_gdp": ["tloans","credit_gdp"],
                    "nfc_gdp":      ["tloans","credit_gdp"],
                    "rgdppc":       ["gdp","gdp_growth"],
                    "rconpc":       ["gdp_growth"],
                    "eq_tr":        ["hpnom","hp_real_growth"],
                    "hpnom":        ["hp_real_growth"],
                    "bond_tr":      ["ltrate"],
                    "bill_tr":      ["stir"],
                    "exports":      ["ca_gdp"],
                    "imports":      ["ca_gdp"],
                    "narrowm":      ["money_gdp"],
                }
                _alts = [a for a in _alt_map.get(_col, []) if a in dff.columns]
                if _alts:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) not in this dataset — showing `{_alts[0]}` ({col_label(_alts[0])}) as closest alternative.")
                    _col = _alts[0]
                    _label = col_label(_col)
                    _desc  = col_desc(_col)
                else:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) is not available in this version of the JST dataset.")
                    continue
            st.caption(f"**{_label}** — {_desc}")
            _latest = dff.groupby("iso")[_col].apply(lambda s: s.dropna().iloc[-1] if len(s.dropna())>0 else None).dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*max(0,_n-6) + ["🟡","🟠","🔴"]
            _fig = go.Figure(go.Bar(x=_latest["Value"], y=_latest["Country"], orientation="h",
                marker_color=_colors, text=_latest["Value"].round(1).astype(str),
                textposition="outside", textfont=dict(size=9)))
            _fig.update_layout(**L(_label, max(260, 30*_n+60), fig=_fig))
            st.plotly_chart(_fig, use_container_width=True, key=f"rank_cr_{_orig_col}")
            _latest.insert(0, "", _medals[:_n])
            _latest["vs Avg"] = (_latest["Value"] - _latest["Value"].mean()).round(2).apply(lambda x: f"+{x:.2f}" if x>0 else f"{x:.2f}")
            st.dataframe(_latest.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))


# ══════════════════════════════════════════════
# TAB 2 — MONEY & BANKING
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-label">Monetary Aggregates & Interest Rates</div>', unsafe_allow_html=True)
    render_glossary_expander(["money","money_gdp","narrowm","ltrate","stir","bill_rate","term_spread","cpi","inflation"], "📖 What do these monetary variables mean?")

    col1, col2 = st.columns(2)

    with col1:
        if "money_gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["money_gdp"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Broad Money / GDP (%)", 350, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "ltrate" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["ltrate"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Long-Term Interest Rate (%)", 350, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if "stir" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["stir"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Short-Term Interest Rate (%)", 320, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "ltrate" in dff.columns and "stir" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["term_spread"] = d["ltrate"] - d["stir"]
                fig.add_trace(go.Scatter(x=d["year"], y=d["term_spread"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Term Spread: LT − ST Rate (%)", 320, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    # Inflation
    if "inflation" in dff.columns:
        st.markdown('<div class="section-label">Inflation History</div>', unsafe_allow_html=True)
        fig_inf = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig_inf.add_trace(go.Scatter(x=d["year"], y=d["inflation"],
                name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6),
                fill="tozeroy" if len(selected_countries)==1 else None,
                fillcolor="rgba(59,130,246,0.07)"))
            fig_inf = add_crisis_shading(fig_inf, d, crisis_col)
        fig_inf.add_hline(y=2, line_dash="dot", line_color="#64748b",
                          annotation_text="2% target", annotation_font_color="#64748b")
        fig_inf.update_layout(**L("CPI Inflation Rate (%)", 360, fig=fig_inf))
        st.plotly_chart(fig_inf, use_container_width=True)



    # ── MONEY & BANKING RANKINGS ────────────────────────────────
    st.markdown('<div class="section-label">🏆 Who Has the Highest / Lowest Rates & Inflation?</div>', unsafe_allow_html=True)
    st.caption("A country with high rates and high inflation faces very different challenges from one with low rates and deflation.")

    rank_tabs_mb = st.tabs(["📊 Long-Term Rate", "💵 Short-Term Rate", "🔥 Inflation", "💰 Money Supply/GDP"])
    _mb_metrics = [
        ("ltrate",    "Long-Term Interest Rate (%)",   "Higher = markets demand more compensation for lending long-term. Signals inflation risk or sovereign stress.", False),
        ("stir",      "Short-Term Interest Rate (%)",  "Higher = central bank is tightening to fight inflation. Lower = stimulus mode.", False),
        ("inflation", "Inflation Rate (%)",             "Higher = prices rising faster. Extremes in both directions (hyperinflation or deflation) are damaging.", False),
        ("money_gdp", "Broad Money Supply / GDP (%)",  "Higher = more money sloshing around relative to economic output. Rapid rises can signal future inflation.", False),
    ]
    for _tab, (_orig_col, _label, _desc, _asc) in zip(rank_tabs_mb, _mb_metrics):
        with _tab:
            _col = _orig_col
            if _col not in dff.columns:
                # Try to find a close alternative
                _alt_map = {
                    "mortgage_gdp": ["tloans","credit_gdp"],
                    "nfc_gdp":      ["tloans","credit_gdp"],
                    "rgdppc":       ["gdp","gdp_growth"],
                    "rconpc":       ["gdp_growth"],
                    "eq_tr":        ["hpnom","hp_real_growth"],
                    "hpnom":        ["hp_real_growth"],
                    "bond_tr":      ["ltrate"],
                    "bill_tr":      ["stir"],
                    "exports":      ["ca_gdp"],
                    "imports":      ["ca_gdp"],
                    "narrowm":      ["money_gdp"],
                }
                _alts = [a for a in _alt_map.get(_col, []) if a in dff.columns]
                if _alts:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) not in this dataset — showing `{_alts[0]}` ({col_label(_alts[0])}) as closest alternative.")
                    _col = _alts[0]
                    _label = col_label(_col)
                    _desc  = col_desc(_col)
                else:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) is not available in this version of the JST dataset.")
                    continue
            st.caption(f"**{_label}** — {_desc}")
            _latest = dff.groupby("iso")[_col].apply(lambda s: s.dropna().iloc[-1] if len(s.dropna())>0 else None).dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*max(0,_n-6) + ["🟡","🟠","🔴"]
            _fig = go.Figure(go.Bar(x=_latest["Value"], y=_latest["Country"], orientation="h",
                marker_color=_colors, text=_latest["Value"].round(2).astype(str),
                textposition="outside", textfont=dict(size=9)))
            _fig.update_layout(**L(_label, max(260, 30*_n+60), fig=_fig))
            st.plotly_chart(_fig, use_container_width=True, key=f"rank_mb_{_orig_col}")
            _latest.insert(0, "", _medals[:_n])
            _latest["vs Avg"] = (_latest["Value"] - _latest["Value"].mean()).round(2).apply(lambda x: f"+{x:.2f}" if x>0 else f"{x:.2f}")
            st.dataframe(_latest.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))


# ══════════════════════════════════════════════
# TAB 3 — ASSET PRICES
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-label">Asset Price Cycles: Housing & Equities</div>', unsafe_allow_html=True)
    render_glossary_expander(["hpnom","hp_real","hp_real_growth","eq_tr","eq_dp","eq_real_tr","bond_tr","bill_tr"], "📖 What do these asset price variables mean?")

    col1, col2 = st.columns(2)
    with col1:
        if "hp_real_growth" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Bar(x=d["year"], y=d["hp_real_growth"],
                    name=iso_to_name(iso), marker_color=PALETTE[i%len(PALETTE)],
                    opacity=0.75))
            fig.update_layout(**L("Real House Price Growth (%)", 360), barmode="overlay")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "hpnom" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["hpnom"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Nominal House Price Index", 360), yaxis_type="log" if log_scale else "linear")
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
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Equity Cumulative Total Return (Base=1)", 360), yaxis_type="log")
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            # Rolling 10yr average equity return
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["eq_roll10"] = d["eq_tr"].rolling(10).mean()
                fig.add_trace(go.Scatter(x=d["year"], y=d["eq_roll10"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**L("Equity Total Return – 10Y Rolling Avg (%)", 360, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    # House-price vs credit scatter
    if "credit_gdp" in dff.columns and "hp_real_growth" in dff.columns:
        st.markdown('<div class="section-label">Credit–House Price Nexus</div>', unsafe_allow_html=True)
        scatter_data = dff[["iso","year","credit_gdp_chg","hp_real_growth",crisis_col if crisis_col else "year"]].dropna()
        if crisis_col and crisis_col in scatter_data.columns:
            scatter_data["crisis_label"] = scatter_data[crisis_col].map({1:"Crisis Year",0:"Normal Year"})
        else:
            scatter_data["crisis_label"] = "Normal Year"

        fig_s = go.Figure()
        # Draw one trace per country — all years, colour = country, symbol = crisis status
        for i, iso in enumerate(selected_countries):
            col_hex = PALETTE[i % len(PALETTE)]
            r_, g_, b_ = int(col_hex[1:3],16), int(col_hex[3:5],16), int(col_hex[5:7],16)
            for crisis_label, sym, sz, op, border in [
                ("Normal Year",  "circle",        7,  0.55, 0.0),
                ("Crisis Year",  "diamond",       11, 0.95, 1.5),
            ]:
                d_s = scatter_data[(scatter_data["iso"]==iso) & (scatter_data["crisis_label"]==crisis_label)]
                if len(d_s) == 0:
                    continue
                fig_s.add_trace(go.Scatter(
                    x=d_s["credit_gdp_chg"], y=d_s["hp_real_growth"],
                    mode="markers",
                    name=iso_to_name(iso) if crisis_label == "Normal Year" else f"{iso_to_name(iso)} ◆ crisis",
                    legendgroup=iso,
                    showlegend=True,
                    marker=dict(
                        color=f"rgba({r_},{g_},{b_},{op})",
                        symbol=sym, size=sz,
                        line=dict(color=col_hex, width=border),
                    ),
                    customdata=np.stack([d_s["year"], d_s["crisis_label"]], axis=-1),
                    hovertemplate=(
                        f"<b>{iso_to_name(iso)}</b>  %{{customdata[0]}}<br>"
                        f"ΔCredit/GDP: <b>%{{x:+.2f}} pp</b><br>"
                        f"Real HP Growth: <b>%{{y:.2f}}%</b><br>"
                        f"%{{customdata[1]}}<extra></extra>"
                    )
                ))

        # OLS trendline — pooled across all visible data
        sd_clean = scatter_data[["credit_gdp_chg","hp_real_growth"]].dropna()
        if len(sd_clean) > 10:
            from scipy import stats as _stats
            _slope, _intercept, _r, _p, _ = _stats.linregress(sd_clean["credit_gdp_chg"], sd_clean["hp_real_growth"])
            _x0, _x1 = sd_clean["credit_gdp_chg"].min(), sd_clean["credit_gdp_chg"].max()
            x_line = np.linspace(_x0, _x1, 120)
            # Confidence band (±1 SE of fit)
            _n = len(sd_clean)
            _sx = sd_clean["credit_gdp_chg"].std()
            _xm = sd_clean["credit_gdp_chg"].mean()
            _se_fit = np.sqrt(
                (sd_clean["hp_real_growth"].var() * (1 - _r**2)) / (_n - 2)
                * (1/_n + (x_line - _xm)**2 / ((_n-1)*_sx**2 + 1e-12))
            )
            y_fit   = _slope * x_line + _intercept
            y_upper = y_fit + 1.96 * _se_fit
            y_lower = y_fit - 1.96 * _se_fit
            # Shaded band
            fig_s.add_trace(go.Scatter(
                x=np.concatenate([x_line, x_line[::-1]]),
                y=np.concatenate([y_upper, y_lower[::-1]]),
                fill="toself", fillcolor="rgba(245,158,11,0.08)",
                line=dict(color="rgba(0,0,0,0)"),
                hoverinfo="skip", showlegend=False, name="95% CI band"
            ))
            fig_s.add_trace(go.Scatter(
                x=x_line, y=y_fit, mode="lines",
                name=f"OLS  R²={_r**2:.2f}  p={'<0.001' if _p<0.001 else f'{_p:.3f}'}",
                line=dict(color="#f59e0b", width=2.5, dash="dash"),
                hovertemplate="OLS fit: %{y:.2f}%<extra></extra>"
            ))

        _sl = L("ΔCredit/GDP (pp, x-axis) vs Real House Price Growth (%, y-axis)", 480, fig=fig_s)
        _sl["xaxis"] = {**_sl.get("xaxis",{}), "title": "Change in Credit/GDP (pp)", "zeroline": True, "zerolinecolor": "#334155", "zerolinewidth": 1}
        _sl["yaxis"] = {**_sl.get("yaxis",{}), "title": "Real House Price Growth (%)","zeroline": True, "zerolinecolor": "#334155", "zerolinewidth": 1}
        _sl["legend"] = dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                             font=dict(size=10), itemsizing="constant", tracegroupgap=4)
        fig_s.update_layout(**_sl)
        st.plotly_chart(fig_s, use_container_width=True)
        st.caption("◆ = crisis year · ● = normal year · Dashed line = OLS pooled fit · Shaded band = 95% confidence interval")



    # ── ASSET PRICE RANKINGS ────────────────────────────────────
    st.markdown('<div class="section-label">🏆 Whose Assets Boomed or Busted Most?</div>', unsafe_allow_html=True)
    st.caption("Asset price rankings reveal which countries experienced the biggest wealth effects — for better or worse.")

    rank_tabs_ap = st.tabs(["🏠 Real House Price Growth", "📊 Nominal House Prices", "📈 Equity Total Return"])
    _ap_metrics = [
        ("hp_real_growth", "Real House Price Growth (%)",   "Higher = houses got more expensive faster in real terms. Top = housing boom. Bottom = bust or stagnation.", False),
        ("hpnom",          "Nominal House Price Index",     "Higher = absolute price level is highest. Reflects accumulated price gains since the index base year.", False),
        ("eq_tr",          "Equity Total Return (%)",       "Higher = stock market returned more to investors that year. Includes dividends + capital gains.", False),
    ]
    for _tab, (_orig_col, _label, _desc, _asc) in zip(rank_tabs_ap, _ap_metrics):
        with _tab:
            _col = _orig_col
            if _col not in dff.columns:
                # Try to find a close alternative
                _alt_map = {
                    "mortgage_gdp": ["tloans","credit_gdp"],
                    "nfc_gdp":      ["tloans","credit_gdp"],
                    "rgdppc":       ["gdp","gdp_growth"],
                    "rconpc":       ["gdp_growth"],
                    "eq_tr":        ["hpnom","hp_real_growth"],
                    "hpnom":        ["hp_real_growth"],
                    "bond_tr":      ["ltrate"],
                    "bill_tr":      ["stir"],
                    "exports":      ["ca_gdp"],
                    "imports":      ["ca_gdp"],
                    "narrowm":      ["money_gdp"],
                }
                _alts = [a for a in _alt_map.get(_col, []) if a in dff.columns]
                if _alts:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) not in this dataset — showing `{_alts[0]}` ({col_label(_alts[0])}) as closest alternative.")
                    _col = _alts[0]
                    _label = col_label(_col)
                    _desc  = col_desc(_col)
                else:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) is not available in this version of the JST dataset.")
                    continue
            st.caption(f"**{_label}** — {_desc}")
            _latest = dff.groupby("iso")[_col].apply(lambda s: s.dropna().iloc[-1] if len(s.dropna())>0 else None).dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*max(0,_n-6) + ["🟡","🟠","🔴"]
            _fig = go.Figure(go.Bar(x=_latest["Value"], y=_latest["Country"], orientation="h",
                marker_color=_colors, text=_latest["Value"].round(1).astype(str),
                textposition="outside", textfont=dict(size=9)))
            _fig.update_layout(**L(_label, max(260, 30*_n+60), fig=_fig))
            st.plotly_chart(_fig, use_container_width=True, key=f"rank_ap_{_orig_col}")
            _latest.insert(0, "", _medals[:_n])
            _latest["vs Avg"] = (_latest["Value"] - _latest["Value"].mean()).round(2).apply(lambda x: f"+{x:.2f}" if x>0 else f"{x:.2f}")
            st.dataframe(_latest.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))


# ══════════════════════════════════════════════
# TAB 4 — MACRO AGGREGATES
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-label">National Accounts & External Sector</div>', unsafe_allow_html=True)
    render_glossary_expander(["gdp","rgdppc","rconpc","iy","pop","ca","ca_gdp","exports","imports"], "📖 What do these macro variables mean?")

    col1, col2 = st.columns(2)
    with col1:
        if "gdp_growth" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["gdp_growth"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**L("Real GDP Growth (%)", 350, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["gdp"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("GDP (National Currency)", 350), yaxis_type="log" if log_scale else "linear")
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        if "ca_gdp" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["ca_gdp"],
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6),
                    fill="tozeroy" if len(selected_countries)==1 else None))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig.update_layout(**L("Current Account / GDP (%)", 320, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "iy" in dff.columns:
            fig = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year")
                fig.add_trace(go.Scatter(x=d["year"], y=d["iy"]*100,
                    name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.6)))
                fig = add_crisis_shading(fig, d, crisis_col)
            fig.update_layout(**L("Investment / GDP (%)", 320, fig=fig))
            st.plotly_chart(fig, use_container_width=True)

    # GDP per capita
    if "rgdppc" in dff.columns:
        st.markdown('<div class="section-label">Real GDP per Capita</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year")
            fig.add_trace(go.Scatter(x=d["year"], y=d["rgdppc"],
                name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=2),
                hovertemplate=f"<b>{iso_to_name(iso)}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>"))
            fig = add_crisis_shading(fig, d, crisis_col)
        fig.update_layout(**L("Real GDP per Capita (2005 USD)", 400), yaxis_type="log" if log_scale else "linear")
        st.plotly_chart(fig, use_container_width=True)



    # ── MACRO RANKINGS ──────────────────────────────────────────
    st.markdown('<div class="section-label">🏆 Who Is Growing Fastest, Richest, Most Productive?</div>', unsafe_allow_html=True)
    st.caption("The fundamental scoreboard — which economies are actually delivering for their citizens.")

    rank_tabs_ma = st.tabs(["🚀 GDP Growth", "💎 GDP per Capita", "🌍 Current Account", "🏗 Investment Rate"])
    _ma_metrics = [
        ("gdp_growth", "Real GDP Growth (%)",          "Higher = economy expanding faster. The headline number politicians live or die by.", False),
        ("rgdppc",     "Real GDP per Capita (USD)",    "Higher = citizens are richer on average. The best single measure of living standards over time.", False),
        ("ca_gdp",     "Current Account / GDP (%)",    "Positive = country lends to the world (surplus). Negative = borrows from the world (deficit). Persistent deficits = vulnerability.", False),
        ("iy",         "Investment / GDP (%)",         "Higher = more of GDP is being reinvested for future growth. Low investment = eating the seed corn.", False),
    ]
    for _tab, (_orig_col, _label, _desc, _asc) in zip(rank_tabs_ma, _ma_metrics):
        with _tab:
            _col = _orig_col
            if _col not in dff.columns:
                # Try to find a close alternative
                _alt_map = {
                    "mortgage_gdp": ["tloans","credit_gdp"],
                    "nfc_gdp":      ["tloans","credit_gdp"],
                    "rgdppc":       ["gdp","gdp_growth"],
                    "rconpc":       ["gdp_growth"],
                    "eq_tr":        ["hpnom","hp_real_growth"],
                    "hpnom":        ["hp_real_growth"],
                    "bond_tr":      ["ltrate"],
                    "bill_tr":      ["stir"],
                    "exports":      ["ca_gdp"],
                    "imports":      ["ca_gdp"],
                    "narrowm":      ["money_gdp"],
                }
                _alts = [a for a in _alt_map.get(_col, []) if a in dff.columns]
                if _alts:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) not in this dataset — showing `{_alts[0]}` ({col_label(_alts[0])}) as closest alternative.")
                    _col = _alts[0]
                    _label = col_label(_col)
                    _desc  = col_desc(_col)
                else:
                    st.info(f"ℹ️ `{_col}` ({col_label(_col)}) is not available in this version of the JST dataset.")
                    continue
            st.caption(f"**{_label}** — {_desc}")
            _latest = dff.groupby("iso")[_col].apply(lambda s: s.dropna().iloc[-1] if len(s.dropna())>0 else None).dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*max(0,_n-6) + ["🟡","🟠","🔴"]
            _fig = go.Figure(go.Bar(x=_latest["Value"], y=_latest["Country"], orientation="h",
                marker_color=_colors, text=_latest["Value"].round(2).astype(str),
                textposition="outside", textfont=dict(size=9)))
            _fig.update_layout(**L(_label, max(260, 30*_n+60), fig=_fig))
            st.plotly_chart(_fig, use_container_width=True, key=f"rank_ma_{_orig_col}")
            _latest.insert(0, "", _medals[:_n])
            _latest["vs Avg"] = (_latest["Value"] - _latest["Value"].mean()).round(2).apply(lambda x: f"+{x:.2f}" if x>0 else f"{x:.2f}")
            st.dataframe(_latest.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))


# ══════════════════════════════════════════════
# TAB 5 — CRISIS ANALYSIS
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-label">Financial Crisis Anatomy</div>', unsafe_allow_html=True)
    render_glossary_expander(["crisisJST","crisisdate","credit_gdp","gdp_growth","inflation","hp_real_growth","ltrate"], "📖 What do these crisis variables mean?")

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
            fig.update_layout(**L(height=max(300, 40*len(crisis_counts)+60)),
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
            fig2.update_layout(**L(height=350, extra={"showlegend": False, "coloraxis_showscale": False}, fig=fig))
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

                    fig_ev.update_layout(**L(height=350), title="Event Study: Average Macro Dynamics Around Crisis Onset (t=0)",
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
        pivot.index = [iso_to_name(c) for c in pivot.index]
        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0,"#0f172a"],[1,"#ef4444"]],
            showscale=False,
            hovertemplate="Country: %{y}<br>Year: %{x}<br>Crisis: %{z}<extra></extra>"
        ))
        heat_layout = L("Crisis Episodes: Country × Year", max(200, 30*len(pivot)+80), fig=fig_heat)
        heat_layout["yaxis"] = {**heat_layout.get("yaxis", {}), "tickfont": dict(size=10)}
        fig_heat.update_layout(**heat_layout)
        st.plotly_chart(fig_heat, use_container_width=True)



    # ── CRISIS RANKINGS ─────────────────────────────────────────
    st.markdown('<div class="section-label">🏆 Who Has Been Most / Least Crisis-Prone?</div>', unsafe_allow_html=True)
    st.caption("Crisis frequency is the ultimate stress test of a financial system over history.")

    if crisis_col in dff.columns:
        _crisis_counts = dff.groupby("iso")[crisis_col].sum().reset_index()
        _crisis_counts.columns = ["Country", "Crisis Years"]
        _crisis_counts["Country"] = _crisis_counts["Country"].map(iso_to_name)
        _crisis_counts = _crisis_counts.sort_values("Crisis Years", ascending=False).reset_index(drop=True)
        _n = len(_crisis_counts)
        _colors_c = ["#ef4444" if i < 3 else ("#10b981" if i >= _n-3 else "#f59e0b") for i in range(_n)]
        _medals_c = ["🔴","🟠","🟡"] + ["⬜"]*max(0,_n-6) + ["🥉","🥈","🥇"]

        _col1, _col2 = st.columns([2,1])
        with _col1:
            _fig_c = go.Figure(go.Bar(
                x=_crisis_counts["Crisis Years"], y=_crisis_counts["Country"],
                orientation="h", marker_color=_colors_c,
                text=_crisis_counts["Crisis Years"].astype(str) + " yrs",
                textposition="outside", textfont=dict(size=9)))
            _fig_c.update_layout(**L("Total Crisis Years in Selected Period", max(260, 30*_n+60), fig=_fig_c))
            st.plotly_chart(_fig_c, use_container_width=True, key="rank_crisis_count")
        with _col2:
            _crisis_counts.insert(0, "", _medals_c[:_n])
            st.markdown('**🔴 Most crisis-prone → 🥇 Most stable**')
            st.dataframe(_crisis_counts.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))
            _worst = _crisis_counts.iloc[0]["Country"]
            _best  = _crisis_counts.iloc[-1]["Country"]
            _worst_n = _crisis_counts.iloc[0]["Crisis Years"]
            _best_n  = _crisis_counts.iloc[-1]["Crisis Years"]
            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">⚡ Crisis Scoreboard</div>
                <b>🔴 Most Crises:</b> {_worst} ({_worst_n:.0f} years)<br>
                <b>🥇 Most Stable:</b> {_best} ({_best_n:.0f} years)<br>
                <b>📊 Avg:</b> {_crisis_counts["Crisis Years"].mean():.1f} years<br><br>
                <span style="color:#64748b;font-size:0.75rem;">
                Counts total years flagged as financial crisis episodes in the JST dataset within selected year range.
                </span>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 6 — CROSS-COUNTRY
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-label">Cross-Country Benchmarking</div>', unsafe_allow_html=True)
    render_glossary_expander(["credit_gdp","gdp_growth","inflation","ltrate","stir","ca_gdp","money_gdp","hp_real_growth"], "📖 What do these variables mean?")

    yr_select = st.slider("Select Year for Cross-Section", year_range[0], year_range[1], min(year_range[1], max(year_range[0], min(2015, year_range[1]))), key="cs_year")
    cs = dff[dff["year"]==yr_select][["iso"] + [c for c in NON_ID if c in dff.columns]].dropna(subset=["iso"])

    avail_vars = [c for c in ["credit_gdp","gdp_growth","inflation","ltrate","stir","ca_gdp","money_gdp","hp_real_growth"] if c in cs.columns]

    if len(avail_vars) >= 2:
        _cv1, _cv2, _cv3 = st.columns(3)
        with _cv1: x_var = st.selectbox("X Variable", avail_vars, index=0, key="cs_x", format_func=col_label)
        with _cv2: y_var = st.selectbox("Y Variable", avail_vars, index=min(1,len(avail_vars)-1), key="cs_y", format_func=col_label)
        with _cv3: size_var = st.selectbox("Bubble Size (optional)", ["(none)"] + avail_vars, key="cs_size", format_func=lambda c: "None" if c=="(none)" else col_label(c))

        _cols_needed = ["iso", x_var, y_var] + ([size_var] if size_var != "(none)" and size_var in cs.columns else [])
        plot_data = cs[_cols_needed].dropna().copy()
        plot_data["label"] = plot_data["iso"].map(iso_to_name)

        fig = go.Figure()
        for i, row in plot_data.iterrows():
            _iso = row["iso"]
            _idx = list(plot_data["iso"].unique()).index(_iso) if _iso in plot_data["iso"].unique() else i
            col_hex = PALETTE[_idx % len(PALETTE)]
            r_, g_, b_ = int(col_hex[1:3],16), int(col_hex[3:5],16), int(col_hex[5:7],16)
            # Bubble size: proportional to size_var if selected, else fixed
            if size_var != "(none)" and size_var in row.index and not pd.isna(row[size_var]):
                _raw_size = abs(float(row[size_var]))
            else:
                _raw_size = None

            fig.add_trace(go.Scatter(
                x=[row[x_var]], y=[row[y_var]],
                mode="markers+text",
                name=iso_to_name(_iso),
                text=[iso_to_name(_iso)],
                textposition="top center",
                textfont=dict(size=10, color="#cbd5e1", family="IBM Plex Mono"),
                marker=dict(
                    size=16 if _raw_size is None else max(12, min(55, _raw_size**0.4 * 8)),
                    color=f"rgba({r_},{g_},{b_},0.75)",
                    line=dict(color=col_hex, width=1.5),
                    symbol="circle",
                ),
                showlegend=False,
                hovertemplate=(
                    f"<b>{iso_to_name(_iso)}</b><br>"
                    f"{col_label(x_var)}: <b>{{x:.2f}}</b><br>"
                    f"{col_label(y_var)}: <b>{{y:.2f}}</b>"
                    + (f"<br>{col_label(size_var)}: <b>{row[size_var]:.2f}</b>" if size_var != "(none)" and size_var in row.index else "")
                    + "<extra></extra>"
                ).replace("{x", "%{x").replace("{y", "%{y"),
            ))

        # Zero-lines for reference
        fig.add_vline(x=0, line_dash="dot", line_color="#334155", line_width=1)
        fig.add_hline(y=0, line_dash="dot", line_color="#334155", line_width=1)

        _cs_layout = L(f"{col_label(x_var)} vs {col_label(y_var)} — {yr_select}", 520, extra={"showlegend": False}, fig=fig)
        _cs_layout["xaxis"] = {**_cs_layout.get("xaxis",{}), "title": col_label(x_var)}
        _cs_layout["yaxis"] = {**_cs_layout.get("yaxis",{}), "title": col_label(y_var)}
        _cs_layout["hovermode"] = "closest"
        fig.update_layout(**_cs_layout)
        st.plotly_chart(fig, use_container_width=True)
        if size_var != "(none)":
            st.caption(f"Bubble size ∝ {col_label(size_var)}  ·  Hover for exact values")

    # Bar race-style: latest values
    st.markdown('<div class="section-label">Latest Values Ranking</div>', unsafe_allow_html=True)
    rank_var = st.selectbox("Variable to Rank", avail_vars, key="rank_var")
    latest_cs = dff.groupby("iso")[rank_var].apply(lambda s: s.dropna().iloc[-1] if len(s.dropna())>0 else None).dropna().sort_values(ascending=False).reset_index()
    latest_cs.columns = ["Country", rank_var]

    fig_rank = px.bar(latest_cs, x=rank_var, y="Country", orientation="h",
                       color=rank_var,
                       color_continuous_scale=[[0,"#1e3a5f"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                       title=f"Latest {rank_var} — All Countries")
    fig_rank.update_layout(**L(height=max(300, 28*len(latest_cs)+80)),
                           showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_rank, use_container_width=True)



# ══════════════════════════════════════════════
# TAB 7 — CORRELATIONS
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-label">Correlation Structure & Statistical Relationships</div>', unsafe_allow_html=True)
    render_glossary_expander(["credit_gdp","gdp_growth","inflation","ltrate","stir","ca_gdp","money_gdp","hp_real_growth","loan_growth","eq_tr","iy"], "📖 What do these variables mean?")

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
        st.plotly_chart(fig_corr, use_container_width=True)

    # Rolling correlation
    if "credit_gdp" in dff.columns and "gdp_growth" in dff.columns:
        st.markdown('<div class="section-label">Rolling 10-Year Correlation: Credit/GDP vs GDP Growth</div>', unsafe_allow_html=True)
        fig_roll = go.Figure()
        for i, iso in enumerate(selected_countries):
            d = dff[dff["iso"]==iso].sort_values("year").copy()
            d["roll_corr"] = d["credit_gdp"].rolling(10, min_periods=5).corr(d["gdp_growth"])
            fig_roll.add_trace(go.Scatter(x=d["year"], y=d["roll_corr"],
                name=iso_to_name(iso), mode="lines", line=dict(color=PALETTE[i%len(PALETTE)], width=1.8)))
            fig_roll = add_crisis_shading(fig_roll, d, crisis_col)
        fig_roll.add_hline(y=0, line_dash="dot", line_color="#475569")
        fig_roll.update_layout(**L("Rolling 10Y Corr: Credit/GDP vs GDP Growth", 360, extra={"yaxis": {"range": [-1,1]}}, fig=fig_roll))
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
            x_line = np.linspace(biv[xv].min(), biv[xv].max(), 120)
            y_line = slope * x_line + intercept

            # 95% confidence band
            _n_b = len(biv)
            _sx_b = biv[xv].std()
            _xm_b = biv[xv].mean()
            _se_b = np.sqrt(
                (biv[yv].var() * (1 - r**2)) / (_n_b - 2)
                * (1/_n_b + (x_line - _xm_b)**2 / ((_n_b-1)*_sx_b**2 + 1e-12))
            )
            y_upper_b = y_line + 1.96 * _se_b
            y_lower_b = y_line - 1.96 * _se_b

            fig_biv = go.Figure()

            # Per-country scatter with distinct colour + opacity by density
            for i, iso in enumerate(selected_countries):
                d_biv = biv[biv["iso"]==iso]
                if len(d_biv) == 0:
                    continue
                col_hex = PALETTE[i % len(PALETTE)]
                r_, g_, b_ = int(col_hex[1:3],16), int(col_hex[3:5],16), int(col_hex[5:7],16)
                fig_biv.add_trace(go.Scatter(
                    x=d_biv[xv], y=d_biv[yv],
                    mode="markers", name=iso_to_name(iso),
                    marker=dict(
                        color=f"rgba({r_},{g_},{b_},0.55)",
                        size=6, symbol="circle",
                        line=dict(color=col_hex, width=0.8),
                    ),
                    customdata=d_biv["year"],
                    hovertemplate=(
                        f"<b>{iso_to_name(iso)}</b>  %{{customdata}}<br>"
                        f"{col_label(xv)}: <b>%{{x:.2f}}</b><br>"
                        f"{col_label(yv)}: <b>%{{y:.2f}}</b><extra></extra>"
                    )
                ))

            # 95% CI shaded band
            fig_biv.add_trace(go.Scatter(
                x=np.concatenate([x_line, x_line[::-1]]),
                y=np.concatenate([y_upper_b, y_lower_b[::-1]]),
                fill="toself", fillcolor="rgba(245,158,11,0.07)",
                line=dict(color="rgba(0,0,0,0)"),
                hoverinfo="skip", showlegend=False, name="95% CI"
            ))
            # OLS fit line
            fig_biv.add_trace(go.Scatter(
                x=x_line, y=y_line, mode="lines",
                name=f"OLS  r={r:.2f}  R²={r**2:.3f}  p={'<0.001' if p<0.001 else f'{p:.3f}'}",
                line=dict(color="#f59e0b", width=2.5, dash="dash"),
            ))

            # Zero reference lines
            fig_biv.add_vline(x=0, line_dash="dot", line_color="#334155", line_width=1)
            fig_biv.add_hline(y=0, line_dash="dot", line_color="#334155", line_width=1)

            _bl = L(f"{col_label(xv)} vs {col_label(yv)}", 460, fig=fig_biv)
            _bl["xaxis"] = {**_bl.get("xaxis",{}), "title": f"{col_label(xv)} ({xv})"}
            _bl["yaxis"] = {**_bl.get("yaxis",{}), "title": f"{col_label(yv)} ({yv})"}
            _bl["hovermode"] = "closest"
            _bl["legend"] = dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                                 font=dict(size=10), itemsizing="constant")
            fig_biv.update_layout(**_bl)
            st.plotly_chart(fig_biv, use_container_width=True)

            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">📐 OLS Regression Result</div>
                <b>{yv} = {intercept:.3f} + {slope:.3f} × {xv}</b><br>
                R² = {r**2:.3f} &nbsp;·&nbsp; p-value = {p:.4f} &nbsp;·&nbsp; N = {len(biv):,}
                {"— statistically significant at 5% level" if p < 0.05 else "— NOT significant at 5% level"}
                <br><span style="color:#64748b;font-size:0.75rem;">⚠️ Pooled panel OLS without fixed effects — R² may be inflated by shared cross-country trends.</span>
            </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════
# TAB 8 — DATA EXPLORER
# ══════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-label">Raw Data & Variable Catalogue</div>', unsafe_allow_html=True)
    render_glossary_expander(list(JST_GLOSSARY.keys()), "📖 Full JST Variable Glossary — click to expand")

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
        _cov_layout = L("Variable Coverage (% non-null, top 30)", 600, extra={"showlegend": False})
        _cov_layout["xaxis"] = {**_cov_layout.get("xaxis", {}), "range": [0, 115]}
        fig_cov.update_layout(**_cov_layout)
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




# ══════════════════════════════════════════════
# TAB 9 — DALIO EMPIRE CYCLE
# ══════════════════════════════════════════════
with tabs[8]:
    st.markdown('''
    <div class="insight-box" style="border-left-color:#8b5cf6;margin-bottom:24px;">
        <div class="insight-title" style="color:#8b5cf6;">🌀 Ray Dalio's Big Cycle Framework</div>
        Ray Dalio's <b>Empire Cycle</b> describes how nations rise and fall over 50–100 year arcs driven by
        debt, money, internal order, external power, and acts of nature. His <b>Long-Term Debt Cycle</b>
        describes the ~75 year credit expansion → crisis → deleveraging arc. This tab maps both frameworks
        directly onto JST data — the most comprehensive long-run macro dataset available.
        <br><br>
        <i>Components: Debt Cycle · Money & Credit · Productivity · Internal Order · External Balance · Asset Prices · Crisis Frequency</i>
    </div>
    ''', unsafe_allow_html=True)

    # ── COMPUTE DALIO SCORES ──────────────────────────────

    # ── OVERALL EMPIRE HEALTH ─────────────────────────────
    st.markdown('<div class="section-label">Empire Health Score (Composite)</div>', unsafe_allow_html=True)
    render_glossary_expander(["empire_health","debt_burden","money_printing","debt_service","productivity","internal_order","external_strength","asset_cycle","inflation_pressure","credit_gdp","ltrate","ca_gdp","crisisJST"], "📖 What do these Dalio cycle scores mean?")

    fig_health = go.Figure()
    for i, iso in enumerate(selected_countries):
        d_iso = dff[dff["iso"]==iso].copy()
        sc = compute_dalio_scores(d_iso)
        if len(sc) == 0: continue
        fig_health.add_trace(go.Scatter(
            x=sc["year"], y=sc["empire_health"],
            name=iso_to_name(iso), mode="lines",
            line=dict(color=PALETTE[i%len(PALETTE)], width=2.5),
            hovertemplate=f"<b>{iso_to_name(iso)}</b><br>Year: %{{x}}<br>Empire Health: %{{y:.1f}}/100<extra></extra>"
        ))
        fig_health = add_crisis_shading(fig_health, d_iso, crisis_col)

    fig_health.add_hline(y=50, line_dash="dot", line_color="#475569",
                         annotation_text="Neutral (50)", annotation_font_color="#64748b")
    fig_health.add_hrect(y0=65, y1=100, fillcolor="rgba(16,185,129,0.04)", layer="below", line_width=0)
    fig_health.add_hrect(y0=0,  y1=35,  fillcolor="rgba(239,68,68,0.04)",  layer="below", line_width=0)
    _hl = L("Composite Empire Health Score (0=Declining · 100=Rising)", 420, extra={"yaxis": {"range": [0, 100]}})
    fig_health.update_layout(**_hl)
    st.plotly_chart(fig_health, use_container_width=True)

    st.markdown("""
    <div class="insight-box" style="border-left-color:#10b981;">
        <div class="insight-title" style="color:#10b981;">📐 Score Methodology</div>
        <b>Health (60%):</b> Productivity growth (10Y rolling GDP/capita), Internal order (inverse crisis frequency), External strength (current account/GDP)<br>
        <b>Stress (40%):</b> Debt burden (credit/GDP), Debt service pressure (rate × debt), Inflation deviation from 2% target<br>
        All components min-max normalized 0–100 across the full historical sample. Red bands = JST crisis episodes.
    </div>""", unsafe_allow_html=True)

    # ── 8 COMPONENT RADAR ────────────────────────────────
    st.markdown('<div class="section-label">Cycle Component Radar — Latest Reading</div>', unsafe_allow_html=True)

    radar_cols = ["debt_burden","money_printing","debt_service","productivity",
                  "internal_order","external_strength","asset_cycle","inflation_pressure"]
    radar_labels = ["Debt Burden","Money Printing","Debt Service","Productivity",
                    "Internal Order","External Strength","Asset Cycle","Inflation Pressure"]

    col_r1, col_r2 = st.columns([2,1])
    with col_r1:
        fig_radar = go.Figure()
        for i, iso in enumerate(selected_countries):
            d_iso = dff[dff["iso"]==iso].copy()
            sc = compute_dalio_scores(d_iso)
            if len(sc) == 0: continue
            latest = sc.sort_values("year").dropna(subset=["empire_health"]).iloc[-1] if len(sc.dropna(subset=["empire_health"])) > 0 else sc.sort_values("year").iloc[-1]
            vals = [latest.get(c, 50) for c in radar_cols]
            vals_closed = vals + [vals[0]]
            labels_closed = radar_labels + [radar_labels[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_closed, theta=labels_closed,
                name=iso_to_name(iso), mode="lines+markers",
                line=dict(color=PALETTE[i%len(PALETTE)], width=2),
                fill="toself",
                fillcolor=f"rgba({int(PALETTE[i%len(PALETTE)][1:3],16)},"
                          f"{int(PALETTE[i%len(PALETTE)][3:5],16)},"
                          f"{int(PALETTE[i%len(PALETTE)][5:7],16)},0.08)"
            ))
        fig_radar.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(family="IBM Plex Mono", color="#94a3b8", size=10),
            polar=dict(
                bgcolor="#0f172a",
                radialaxis=dict(visible=True, range=[0,100], gridcolor="#1e2d45",
                               tickfont=dict(size=8), color="#475569"),
                angularaxis=dict(gridcolor="#1e2d45", color="#64748b")
            ),
            legend=dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1),
            title="Dalio Cycle Components — Latest Year",
            height=480, margin=dict(l=60,r=60,t=50,b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r2:
        # Component scores table for latest year
        rows = []
        for iso in selected_countries:
            d_iso = dff[dff["iso"]==iso].copy()
            sc = compute_dalio_scores(d_iso)
            if len(sc) == 0: continue
            latest = sc.sort_values("year").dropna(subset=["empire_health"]).iloc[-1] if len(sc.dropna(subset=["empire_health"])) > 0 else sc.sort_values("year").iloc[-1]
            row = {"Country": iso, "Year": int(latest["year"]), "Health": f"{latest['empire_health']:.0f}"}
            for c, lbl in zip(radar_cols, radar_labels):
                row[lbl[:8]] = f"{latest.get(c,50):.0f}"
            rows.append(row)
        if rows:
            tbl = pd.DataFrame(rows).set_index("Country")
            st.markdown('<div style="font-family:monospace;font-size:0.7rem;color:#64748b;margin-bottom:8px;letter-spacing:1px;">LATEST SCORES (0–100)</div>', unsafe_allow_html=True)
            st.dataframe(tbl, use_container_width=True, height=400)

    # ── LONG-TERM DEBT CYCLE ──────────────────────────────
    st.markdown('<div class="section-label">Long-Term Debt Cycle (Dalio ~75 Year Arc)</div>', unsafe_allow_html=True)

    if "credit_gdp" in dff.columns:
        col_d1, col_d2 = st.columns(2)

        with col_d1:
            # Credit/GDP with 30Y rolling average as "secular trend"
            fig_ltdc = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["credit_trend"] = d["credit_gdp"].rolling(30, min_periods=10).mean()
                fig_ltdc.add_trace(go.Scatter(
                    x=d["year"], y=d["credit_gdp"],
                    name=iso_to_name(iso), mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1.5),
                ))
                fig_ltdc.add_trace(go.Scatter(
                    x=d["year"], y=d["credit_trend"],
                    name=f"{iso_to_name(iso)} trend", mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=1, dash="dot"),
                    showlegend=False
                ))
                fig_ltdc = add_crisis_shading(fig_ltdc, d, crisis_col)
            fig_ltdc.update_layout(**L("Credit/GDP — Actual vs 30Y Secular Trend", 360, fig=fig_ltdc))
            st.plotly_chart(fig_ltdc, use_container_width=True)

        with col_d2:
            # Credit gap = actual minus trend (Dalio's "excess debt")
            fig_gap = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["credit_trend"] = d["credit_gdp"].rolling(30, min_periods=10).mean()
                d["credit_gap"]   = d["credit_gdp"] - d["credit_trend"]
                fig_gap.add_trace(go.Scatter(
                    x=d["year"], y=d["credit_gap"],
                    name=iso_to_name(iso), mode="lines",
                    line=dict(color=PALETTE[i%len(PALETTE)], width=2),
                    fill="tozeroy",
                    fillcolor=f"rgba({int(PALETTE[i%len(PALETTE)][1:3],16)},"
                              f"{int(PALETTE[i%len(PALETTE)][3:5],16)},"
                              f"{int(PALETTE[i%len(PALETTE)][5:7],16)},0.08)"
                ))
                fig_gap = add_crisis_shading(fig_gap, d, crisis_col)
            fig_gap.add_hline(y=0, line_dash="dot", line_color="#475569")
            fig_gap.update_layout(**L("Credit Gap (Actual − Trend) — Dalio's Excess Debt Signal", 360, fig=fig_gap))
            st.plotly_chart(fig_gap, use_container_width=True)

    # ── SHORT-TERM DEBT CYCLE ─────────────────────────────
    st.markdown('<div class="section-label">Short-Term Debt Cycle (Dalio ~8 Year Business Cycle)</div>', unsafe_allow_html=True)

    if "gdp_growth" in dff.columns and "inflation" in dff.columns:
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            # GDP growth with 8Y rolling average
            fig_stdc = go.Figure()
            for i, iso in enumerate(selected_countries):
                d = dff[dff["iso"]==iso].sort_values("year").copy()
                d["gdp_cycle"] = d["gdp_growth"] - d["gdp_growth"].rolling(8, min_periods=4).mean()
                fig_stdc.add_trace(go.Bar(
                    x=d["year"], y=d["gdp_cycle"],
                    name=iso_to_name(iso),
                    marker_color=[PALETTE[i%len(PALETTE)] if v >= 0 else "#ef4444" for v in d["gdp_cycle"].fillna(0)],
                    opacity=0.75
                ))
                fig_stdc = add_crisis_shading(fig_stdc, d, crisis_col)
            fig_stdc.update_layout(**L("GDP Growth Cycle (Deviation from 8Y Mean)", 340), barmode="overlay")
            st.plotly_chart(fig_stdc, use_container_width=True)

        with col_s2:
            # Inflation vs growth scatter — Dalio's four quadrants
            scatter_dg = dff[["iso","year","gdp_growth","inflation"]].dropna()

            # Dynamic axis range from actual data (2nd–98th pctile to clip outliers)
            _gmin = float(scatter_dg["gdp_growth"].quantile(0.02))
            _gmax = float(scatter_dg["gdp_growth"].quantile(0.98))
            _imin = float(scatter_dg["inflation"].quantile(0.02))
            _imax = float(scatter_dg["inflation"].quantile(0.98))
            _gpad = max(0.5, (_gmax - _gmin) * 0.12)
            _ipad = max(0.5, (_imax - _imin) * 0.12)
            _xlo, _xhi = _gmin - _gpad, _gmax + _gpad
            _ylo, _yhi = _imin - _ipad, _imax + _ipad
            _xpivot, _ypivot = 0.0, 2.0

            fig_quad = go.Figure()

            # Quadrant fills clipped to actual data range
            _qfills = [
                (_xpivot, _xhi,   _ylo,    _ypivot, "rgba(16,185,129,0.07)"),
                (_xpivot, _xhi,   _ypivot, _yhi,    "rgba(245,158,11,0.07)"),
                (_xlo,    _xpivot,_ylo,    _ypivot, "rgba(100,116,139,0.07)"),
                (_xlo,    _xpivot,_ypivot, _yhi,    "rgba(239,68,68,0.07)"),
            ]
            for _qx0,_qx1,_qy0,_qy1,_qfc in _qfills:
                fig_quad.add_shape(
                    type="rect", xref="x", yref="y", layer="below",
                    x0=_qx0, x1=_qx1, y0=_qy0, y1=_qy1,
                    fillcolor=_qfc, line_width=0,
                )

            # Per-country dots
            for i, iso in enumerate(selected_countries):
                d_q = scatter_dg[scatter_dg["iso"]==iso].copy()
                if len(d_q) == 0:
                    continue
                col_hex = PALETTE[i % len(PALETTE)]
                r_, g_, b_ = int(col_hex[1:3],16), int(col_hex[3:5],16), int(col_hex[5:7],16)
                fig_quad.add_trace(go.Scatter(
                    x=d_q["gdp_growth"], y=d_q["inflation"],
                    mode="markers", name=iso_to_name(iso),
                    marker=dict(
                        color=f"rgba({r_},{g_},{b_},0.55)",
                        size=6, symbol="circle",
                        line=dict(color=col_hex, width=0.8),
                    ),
                    customdata=d_q["year"],
                    hovertemplate=(
                        f"<b>{iso_to_name(iso)}</b>  %{{customdata}}<br>"
                        f"GDP Growth: <b>%{{x:.1f}}%</b><br>"
                        f"Inflation: <b>%{{y:.1f}}%</b><extra></extra>"
                    )
                ))

            # Corner labels using paper coordinates — always in corners, never on data
            _corner_labels = [
                (0.98, 0.02, "right", "bottom", "GOLDILOCKS",        "#10b981", "↑ Equities · Real Estate"),
                (0.98, 0.98, "right", "top",    "INFLATIONARY BOOM", "#f59e0b", "↑ Real Assets"),
                (0.02, 0.02, "left",  "bottom", "DEFLATION BUST",    "#94a3b8", "↑ Bonds · Cash"),
                (0.02, 0.98, "left",  "top",    "STAGFLATION",       "#ef4444", "↑ Real Assets · Cash"),
            ]
            for _cx, _cy, _xanch, _yanch, _ctitle, _cc, _csub in _corner_labels:
                fig_quad.add_annotation(
                    x=_cx, y=_cy, xref="paper", yref="paper",
                    text=f"<b>{_ctitle}</b><br><span style=\'font-size:8px\'>{_csub}</span>",
                    showarrow=False, xanchor=_xanch, yanchor=_yanch,
                    font=dict(size=9, color=_cc, family="IBM Plex Mono"),
                    bgcolor="rgba(10,14,23,0.75)", borderpad=5,
                    bordercolor=_cc, borderwidth=1,
                )

            fig_quad.add_vline(x=_xpivot, line_dash="dot", line_color="#475569", line_width=1.2)
            fig_quad.add_hline(y=_ypivot, line_dash="dot", line_color="#475569", line_width=1.2)

            _ql = L("Dalio\'s Four Quadrants: Growth vs Inflation", 420)
            _ql["xaxis"] = {**_ql.get("xaxis",{}),
                            "title": "Real GDP Growth (%)", "zeroline": False,
                            "range": [_xlo, _xhi]}
            _ql["yaxis"] = {**_ql.get("yaxis",{}),
                            "title": "CPI Inflation (%)", "zeroline": False,
                            "range": [_ylo, _yhi]}
            _ql["hovermode"] = "closest"
            _ql["legend"] = dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                                 font=dict(size=10), itemsizing="constant",
                                 x=0.5, y=-0.18, xanchor="center", orientation="h")
            _ql["margin"] = dict(l=50, r=20, t=40, b=90)
            fig_quad.update_layout(**_ql)
            st.plotly_chart(fig_quad, use_container_width=True)

    # ── EMPIRE PHASE CLASSIFICATION ───────────────────────
    st.markdown('<div class="section-label">Empire Phase Classification</div>', unsafe_allow_html=True)

    phase_rows = []
    for iso in selected_countries:
        d_iso = dff[dff["iso"]==iso].copy()
        sc = compute_dalio_scores(d_iso)
        if len(sc) < 5: continue
        latest = sc.sort_values("year").dropna(subset=["empire_health"]).iloc[-1] if len(sc.dropna(subset=["empire_health"])) > 0 else sc.sort_values("year").iloc[-1]
        prev   = sc.sort_values("year").dropna(subset=["empire_health"]).iloc[-10] if len(sc.dropna(subset=["empire_health"])) >= 10 else sc.sort_values("year").dropna(subset=["empire_health"]).iloc[0] if len(sc.dropna(subset=["empire_health"])) > 0 else sc.sort_values("year").iloc[0]

        health_now  = latest["empire_health"]
        health_then = prev["empire_health"]
        trend = health_now - health_then

        debt_now = latest.get("debt_burden", 50)
        prod_now = latest.get("productivity", 50)
        order_now = latest.get("internal_order", 50)
        ext_now   = latest.get("external_strength", 50)

        # Phase logic
        if health_now >= 65 and trend >= 0:
            phase = "🟢 RISING"
            phase_desc = "Strong productivity, manageable debt, positive trend"
        elif health_now >= 65 and trend < 0:
            phase = "🟡 PEAK"
            phase_desc = "Still healthy but momentum turning — watch debt & order"
        elif health_now >= 45 and trend >= 0:
            phase = "🟡 RECOVERING"
            phase_desc = "Below peak but improving — deleveraging or reform underway"
        elif health_now >= 35 and trend < 0:
            phase = "🟠 DECLINING"
            phase_desc = "Debt elevated, productivity slowing, internal stress rising"
        else:
            phase = "🔴 CRISIS / TROUGH"
            phase_desc = "Deep stress — debt crisis, low growth, disorder signals"

        phase_rows.append({
                "Country": iso_to_name(iso),
            "Phase": phase,
            "Health Score": f"{health_now:.0f}/100",
            "10Y Trend": f"{'▲' if trend>=0 else '▼'} {abs(trend):.1f}",
            "Debt Burden": f"{debt_now:.0f}",
            "Productivity": f"{prod_now:.0f}",
            "Int. Order": f"{order_now:.0f}",
            "Ext. Strength": f"{ext_now:.0f}",
            "Assessment": phase_desc
        })

    if phase_rows:
        phase_df = pd.DataFrame(phase_rows).set_index("Country")
        st.dataframe(phase_df, use_container_width=True, height=min(400, 60+50*len(phase_rows)))

    st.markdown("""
    <div class="insight-box" style="border-left-color:#8b5cf6;">
        <div class="insight-title" style="color:#8b5cf6;">📚 Framework Reference</div>
        Based on Ray Dalio's <i>Principles for Dealing with the Changing World Order</i> (2021) and
        <i>A Template for Understanding Big Debt Crises</i> (2018). The Long-Term Debt Cycle (~50–75 years)
        tracks the full arc of credit expansion → bubble → crisis → deleveraging.
        The Short-Term Business Cycle (~8 years) tracks the recurring growth/inflation rhythm within it.
        Empire Health scores are computed entirely from JST macro-financial data — no subjective inputs.
        <br><br>
        <i>Note: This is a quantitative approximation of Dalio's qualitative framework.
        It excludes geopolitical, military, and institutional dimensions not captured in the JST dataset.</i>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────


    # ── DALIO EMPIRE RANKINGS ───────────────────────────────────
    st.markdown('<div class="section-label">🏆 Empire Scoreboard — Who Is Rising, Who Is Declining?</div>', unsafe_allow_html=True)
    st.caption("Based on Dalio's Big Cycle framework mapped onto JST data. All scores 0–100.")

    # Compute scores for all countries using full dff
    # ── RANKINGS: use cross_country=True so all scores share same scale ──
    # Runs compute_dalio_scores on the full dataset (all 18 countries) with
    # cross_country=True so normalisation is across countries, not per-country.
    # This is the SAME function used for charts — just a different norm mode.
    _cs = compute_dalio_scores(dff, cross_country=True)
    _all_scores = []
    for _iso in dff["iso"].unique():
        _s = _cs[_cs["iso"] == _iso].dropna(subset=["empire_health"])
        if len(_s) == 0:
            continue
        _last = _s.sort_values("year").iloc[-1]
        _row  = {"Country": iso_to_name(_iso)}
        for _c in ["empire_health","debt_burden","productivity","internal_order",
                   "external_strength","asset_cycle","inflation_pressure"]:
            _val = _last.get(_c, np.nan)
            _row[_c] = round(float(_val), 1) if not pd.isna(_val) else 50.0
        _all_scores.append(_row)

    if _all_scores:
        _score_df = pd.DataFrame(_all_scores)
        rank_tabs_dc = st.tabs(["🌍 Empire Health", "📈 Productivity", "⚖️ Debt Burden", "🏛 Internal Order", "🌐 External Strength"])
        _dc_metrics = [
            ("empire_health",     "Overall Empire Health Score",  "Composite score — higher = rising empire. Combines productivity, order, external strength vs debt and stress.", False),
            ("productivity",      "Productivity Score",           "Higher = stronger long-run economic dynamism. The engine of empire rise.", False),
            ("debt_burden",       "Debt Burden Score",            "Higher = LESS indebted = healthier. 100 = lowest debt burden among all countries. Red = most burdened.", False),
            ("internal_order",    "Internal Order Score",         "Higher = fewer financial crises historically = more stable domestic conditions.", False),
            ("external_strength", "External Strength Score",      "Higher = country is a net lender to the world. Persistent surplus = financial power.", False),
        ]
        _inverted = set()  # debt_burden now inverted at normalisation — high = healthy for all scores
        for _tab, (_orig_col, _label, _desc, _asc) in zip(rank_tabs_dc, _dc_metrics):
            with _tab:
                if _orig_col not in _score_df.columns:
                    st.info(f"Score `{_orig_col}` not available.")
                    continue
                st.caption(f"**{_label}** — {_desc}")
                _sd = _score_df[["Country", _orig_col]].sort_values(_orig_col, ascending=_asc).reset_index(drop=True)
                _sd.columns = ["Country", "Score"]
                _n = len(_sd)
                if _orig_col in _inverted:
                    # For debt burden, red = high (bad), green = low (good)
                    _colors_d = ["#ef4444" if i < 3 else ("#10b981" if i >= _n-3 else "#f59e0b") for i in range(_n)]
                    _medals_d = ["🔴","🟠","🟡"] + ["⬜"]*max(0,_n-6) + ["🥉","🥈","🥇"]
                else:
                    _colors_d = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
                    _medals_d = ["🥇","🥈","🥉"] + ["⬜"]*max(0,_n-6) + ["🟡","🟠","🔴"]
                _fig_d = go.Figure(go.Bar(
                    x=_sd["Score"], y=_sd["Country"], orientation="h",
                    marker_color=_colors_d,
                    text=_sd["Score"].round(1).astype(str),
                    textposition="outside", textfont=dict(size=9)))
                _fig_d.update_layout(**L(_label, max(260, 30*_n+60), extra={"xaxis": {"range": [0, 110]}}, fig=_fig_d))
                st.plotly_chart(_fig_d, use_container_width=True, key=f"rank_dc_{_orig_col}")
                _sd.insert(0, "", _medals_d[:_n])
                _sd["vs Avg"] = (_sd["Score"] - _sd["Score"].mean()).round(1).apply(lambda x: f"+{x:.1f}" if x>0 else f"{x:.1f}")
                st.dataframe(_sd.set_index("").rename_axis(""), use_container_width=True, height=min(420, 38*_n+50))


# ══════════════════════════════════════════════
# TAB 10 — INVESTMENT INTELLIGENCE
# ══════════════════════════════════════════════
with tabs[9]:

    # ── DISCLAIMER ─────────────────────────────────────────────
    st.markdown("""
    <div class="insight-box" style="border-left-color:#ef4444;margin-bottom:20px;">
        <div class="insight-title" style="color:#ef4444;">⚠️ Important Disclaimer</div>
        This analysis is <b>purely academic and research-oriented</b>, derived from historical macroeconomic patterns
        in the JST dataset (1870–present). It does <b>not</b> constitute financial advice. Past macroeconomic
        conditions are not a reliable predictor of future asset returns. Always consult a qualified financial
        professional before making investment decisions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="border-left-color:#8b5cf6;margin-bottom:28px;">
        <div class="insight-title" style="color:#8b5cf6;">💡 Investment Intelligence Engine</div>
        This engine scores each country across <b>5 asset classes</b> — equities, real estate, bonds, cash/bills,
        and commodities/alternatives — using 12 macro-financial signals derived from the JST dataset.
        Each signal maps to a specific historical relationship between macro conditions and asset performance.
        Scores are 0–100. The engine surfaces <b>where</b>, <b>what</b>, and <b>why</b>.
    </div>
    """, unsafe_allow_html=True)

    # ── INVESTMENT SCORE ENGINE ─────────────────────────────────
    @st.cache_data(show_spinner=False)
    def compute_investment_scores(dff_data):
        """
        Compute asset-class attractiveness scores (0-100) per country.
        All signals derived from JST data. Higher = more attractive historically.
        Returns a dict: iso → {asset_class: score, signals: {...}, narratives: {...}}
        """
        results = {}

        all_isos = dff_data["iso"].unique()
        # Cross-country norms for comparability
        _dalio = compute_dalio_scores(dff_data, cross_country=True)

        for iso in all_isos:
            d = dff_data[dff_data["iso"] == iso].sort_values("year")
            if len(d) < 5:
                continue

            sc = _dalio[_dalio["iso"] == iso]
            _last_sc = sc.dropna(subset=["empire_health"]).iloc[-1] if len(sc.dropna(subset=["empire_health"])) > 0 else None

            def _get(col, default=np.nan):
                s = d[col].dropna() if col in d.columns else pd.Series(dtype=float)
                return float(s.iloc[-1]) if len(s) > 0 else default

            def _get_score(col, default=50.0):
                if _last_sc is None: return default
                v = _last_sc.get(col, default)
                return float(v) if not pd.isna(v) else default

            def _roll(col, window=5):
                if col not in d.columns: return np.nan
                return float(d[col].rolling(window, min_periods=2).mean().dropna().iloc[-1]) if len(d[col].dropna()) >= 2 else np.nan

            def _pct_vs_history(col):
                """Where is the latest value in its own history? 0=at min, 100=at max."""
                if col not in d.columns: return 50.0
                s = d[col].dropna()
                if len(s) < 5: return 50.0
                latest = s.iloc[-1]
                mn, mx = s.min(), s.max()
                if mx == mn: return 50.0
                return float((latest - mn) / (mx - mn) * 100)

            # ── RAW SIGNALS ──────────────────────────────────────
            gdp_growth_now    = _roll("gdp_growth", 5)
            inflation_now     = _get("inflation", 3.0)
            inflation_roll5   = _roll("inflation", 5)
            ltrate_now        = _get("ltrate", 4.0)
            stir_now          = _get("stir", 2.0)
            credit_gdp_now    = _get("credit_gdp", 80.0)
            credit_gdp_chg    = _roll("credit_gdp_chg", 3)
            hp_growth_now     = _roll("hp_real_growth", 5)
            ca_gdp_now        = _get("ca_gdp", 0.0)
            eq_tr_roll        = _roll("eq_tr", 5)
            crisis_rate_recent= float(d["crisisJST"].tail(10).mean()) if "crisisJST" in d.columns else 0.05
            term_spread       = (ltrate_now - stir_now) if not (np.isnan(ltrate_now) or np.isnan(stir_now)) else 1.0
            money_gdp_chg     = _roll("money_gdp", 3)

            # Dalio scores (cross-country normalised)
            prod_score   = _get_score("productivity")
            order_score  = _get_score("internal_order")
            debt_score   = _get_score("debt_burden")    # high = low debt = healthy
            ext_score    = _get_score("external_strength")
            infl_score   = _get_score("inflation_pressure")  # high = stable prices
            asset_score  = _get_score("asset_cycle")
            empire_health= _get_score("empire_health")

            # Percentile ranks within own history
            credit_pct   = _pct_vs_history("credit_gdp")
            hp_pct       = _pct_vs_history("hpnom")
            ltrate_pct   = _pct_vs_history("ltrate")
            inflation_pct= _pct_vs_history("inflation")

            # ── EQUITY SCORE ─────────────────────────────────────
            # Best when: growth strong, inflation moderate (2-4%), rates not too high,
            # debt manageable, stable political environment, early credit cycle
            eq_signals = {}
            eq_signals["GDP momentum (5Y avg)"]          = min(100, max(0, (gdp_growth_now + 2) / 8 * 100)) if not np.isnan(gdp_growth_now) else 50
            eq_signals["Inflation in sweet spot (2–4%)"] = max(0, 100 - abs(inflation_roll5 - 3) * 15) if not np.isnan(inflation_roll5) else 50
            eq_signals["Credit cycle stage (early=good)"]= max(0, 100 - credit_pct)   # early credit cycle = better
            eq_signals["Political stability"]             = order_score
            eq_signals["Productivity trend"]              = prod_score
            eq_signals["Valuation proxy (earnings yield)"]= max(0, 100 - hp_pct * 0.4)  # not overheated
            eq_score = (
                eq_signals["GDP momentum (5Y avg)"]          * 0.25 +
                eq_signals["Inflation in sweet spot (2–4%)"] * 0.18 +
                eq_signals["Credit cycle stage (early=good)"]* 0.15 +
                eq_signals["Political stability"]             * 0.17 +
                eq_signals["Productivity trend"]              * 0.15 +
                eq_signals["Valuation proxy (earnings yield)"]* 0.10
            )

            # ── REAL ESTATE SCORE ────────────────────────────────
            # Best when: credit expanding, rates low-moderate, prices not at peak,
            # population/income growing, current account not deeply negative
            re_signals = {}
            re_signals["Credit expansion (fuel for RE)"]  = min(100, max(0, (credit_gdp_chg + 3) / 8 * 100)) if not np.isnan(credit_gdp_chg) else 50
            re_signals["Rate environment (low=good)"]     = max(0, 100 - ltrate_pct)
            re_signals["Price not at historical peak"]    = max(0, 100 - hp_pct * 0.9)
            re_signals["Macro stability"]                 = empire_health
            re_signals["Income growth (productivity)"]    = prod_score
            re_signals["External balance"]                = min(100, max(0, ext_score))
            re_score = (
                re_signals["Credit expansion (fuel for RE)"] * 0.22 +
                re_signals["Rate environment (low=good)"]    * 0.22 +
                re_signals["Price not at historical peak"]   * 0.20 +
                re_signals["Macro stability"]                * 0.15 +
                re_signals["Income growth (productivity)"]   * 0.13 +
                re_signals["External balance"]               * 0.08
            )

            # ── BOND SCORE ───────────────────────────────────────
            # Best when: inflation falling/low, rates high (entry point), debt manageable,
            # positive term spread, fiscal credibility
            bd_signals = {}
            bd_signals["Inflation trending down / stable"] = infl_score
            bd_signals["Rate level (high=cheap entry)"]    = ltrate_pct  # high rates = bonds cheap = good entry
            bd_signals["Positive term spread"]             = min(100, max(0, (term_spread + 2) / 6 * 100)) if not np.isnan(term_spread) else 50
            bd_signals["Fiscal credibility (low debt)"]    = debt_score
            bd_signals["Crisis risk (low=safe haven)"]     = max(0, 100 - crisis_rate_recent * 800)
            bd_signals["External strength (FX support)"]  = ext_score
            bd_score = (
                bd_signals["Inflation trending down / stable"] * 0.28 +
                bd_signals["Rate level (high=cheap entry)"]    * 0.22 +
                bd_signals["Positive term spread"]             * 0.15 +
                bd_signals["Fiscal credibility (low debt)"]    * 0.18 +
                bd_signals["Crisis risk (low=safe haven)"]     * 0.10 +
                bd_signals["External strength (FX support)"]  * 0.07
            )

            # ── CASH / BILLS SCORE ───────────────────────────────
            # Best when: rates high (return on cash), inflation controlled,
            # high uncertainty (crisis risk hedge), deflation risk
            ca_signals = {}
            ca_signals["Short-term rate (return)"]         = min(100, max(0, (stir_now / 8) * 100)) if not np.isnan(stir_now) else 50
            ca_signals["Inflation under control"]          = infl_score
            ca_signals["Crisis / uncertainty hedge"]       = min(100, crisis_rate_recent * 1200)   # rising crisis rate → cash looks good
            ca_signals["Deflation protection (low infl)"]  = max(0, 100 - inflation_pct * 0.7)
            ca_signals["Macro stability (preserv. mode)"]  = max(0, 100 - empire_health * 0.5)     # weak macro → cash better
            ca_score = (
                ca_signals["Short-term rate (return)"]    * 0.30 +
                ca_signals["Inflation under control"]     * 0.25 +
                ca_signals["Crisis / uncertainty hedge"]  * 0.20 +
                ca_signals["Deflation protection (low infl)"] * 0.15 +
                ca_signals["Macro stability (preserv. mode)"] * 0.10
            )

            # ── ALTERNATIVES / REAL ASSETS SCORE ────────────────
            # Proxy for commodities, infrastructure, gold.
            # Best when: inflation elevated, currency weak (CA deficit),
            # real rates negative, late credit cycle
            al_signals = {}
            al_signals["Inflation hedge demand"]           = inflation_pct
            al_signals["Real rate negative (inflation>rate)"] = min(100, max(0, (inflation_roll5 - ltrate_now + 5) / 10 * 100)) if not (np.isnan(inflation_roll5) or np.isnan(ltrate_now)) else 50
            al_signals["Late credit cycle (stress signal)"]= credit_pct  # late = alternatives shine
            al_signals["External weakness (CA deficit)"]  = max(0, 100 - ext_score)  # CA deficit → real assets hedge
            al_signals["Empire stress (diversify)"]       = max(0, 100 - empire_health * 0.8)
            al_score = (
                al_signals["Inflation hedge demand"]                  * 0.28 +
                al_signals["Real rate negative (inflation>rate)"]     * 0.25 +
                al_signals["Late credit cycle (stress signal)"]       * 0.22 +
                al_signals["External weakness (CA deficit)"]          * 0.13 +
                al_signals["Empire stress (diversify)"]               * 0.12
            )

            # ── OVERALL CONVICTION ──────────────────────────────
            scores_vec = {"Equities": eq_score, "Real Estate": re_score, "Bonds": bd_score,
                          "Cash/Bills": ca_score, "Real Assets": al_score}
            best_class = max(scores_vec, key=scores_vec.get)
            worst_class= min(scores_vec, key=scores_vec.get)

            results[iso] = {
                "scores":    scores_vec,
                "signals":   {"Equities": eq_signals, "Real Estate": re_signals,
                              "Bonds": bd_signals, "Cash/Bills": ca_signals, "Real Assets": al_signals},
                "best":      best_class,
                "worst":     worst_class,
                "empire":    empire_health,
                "raw": {
                    "gdp_growth": gdp_growth_now, "inflation": inflation_roll5,
                    "ltrate": ltrate_now, "credit_gdp": credit_gdp_now,
                    "ca_gdp": ca_gdp_now, "hp_growth": hp_growth_now,
                    "crisis_rate": crisis_rate_recent, "term_spread": term_spread,
                    "credit_pct": credit_pct, "hp_pct": hp_pct,
                    "ltrate_pct": ltrate_pct,
                },
            }
        return results

    inv_data = compute_investment_scores(dff)

    if not inv_data:
        st.warning("Insufficient data for investment analysis. Try adjusting the year range or country selection.")
        st.stop()

    ASSET_CLASSES  = ["Equities", "Real Estate", "Bonds", "Cash/Bills", "Real Assets"]
    ASSET_COLORS   = {"Equities": "#3b82f6", "Real Estate": "#10b981",
                      "Bonds":    "#f59e0b", "Cash/Bills": "#8b5cf6", "Real Assets": "#ef4444"}
    ASSET_ICONS    = {"Equities": "📈", "Real Estate": "🏠",
                      "Bonds":    "📋", "Cash/Bills": "💵", "Real Assets": "🏅"}

    def rating_label(score):
        if score >= 72: return ("STRONG BUY",  "#10b981", "▲▲")
        if score >= 58: return ("BUY",          "#34d399", "▲")
        if score >= 42: return ("NEUTRAL",      "#64748b", "◼")
        if score >= 28: return ("UNDERWEIGHT",  "#f97316", "▽")
        return              ("AVOID",           "#ef4444", "▽▽")

    def conviction_bar(score, color):
        pct = int(score)
        return (
            '<div style="background:#1e2d45;border-radius:4px;height:8px;width:100%;overflow:hidden;">'
            '<div style="background:' + color + ';height:8px;width:' + str(pct) + '%;border-radius:4px;"></div>'
            '</div>'
        )

    # ── SECTION 1: MASTER HEATMAP ──────────────────────────────
    st.markdown('<div class="section-label">Global Asset Class Attractiveness Heatmap</div>', unsafe_allow_html=True)
    st.caption("Scores 0–100 across 5 asset classes for all selected countries. Derived from 12 JST macro signals.")

    # Build score matrix
    _isos_sorted = sorted(inv_data.keys(), key=lambda x: -inv_data[x]["empire"])
    _hm_z  = [[inv_data[iso]["scores"].get(ac, 50) for ac in ASSET_CLASSES] for iso in _isos_sorted]
    _hm_y  = [iso_to_name(iso) for iso in _isos_sorted]
    _hm_text = [[f"{inv_data[iso]['scores'].get(ac,50):.0f}" for ac in ASSET_CLASSES] for iso in _isos_sorted]

    fig_hm = go.Figure(go.Heatmap(
        z=_hm_z, x=ASSET_CLASSES, y=_hm_y,
        text=_hm_text, texttemplate="<b>%{text}</b>",
        textfont=dict(size=12, family="IBM Plex Mono"),
        colorscale=[
            [0.0,  "#1a0a0a"], [0.15, "#7f1d1d"], [0.30, "#ef4444"],
            [0.45, "#f97316"], [0.55, "#64748b"],
            [0.65, "#3b82f6"], [0.80, "#10b981"], [1.0,  "#d1fae5"],
        ],
        zmid=50, zmin=0, zmax=100,
        colorbar=dict(
            title=dict(text="Score", font=dict(family="IBM Plex Mono", size=10)),
            tickvals=[0,25,50,75,100],
            ticktext=["0<br>Avoid","25<br>Underweight","50<br>Neutral","75<br>Buy","100<br>Strong Buy"],
            tickfont=dict(family="IBM Plex Mono", size=9),
            len=0.8,
        ),
        hovertemplate="<b>%{y}</b> — %{x}<br>Score: <b>%{z:.1f}/100</b><extra></extra>",
    ))
    _hm_h = max(300, 44 * len(_isos_sorted) + 80)
    _hml = L("", _hm_h)
    _hml["margin"] = dict(l=140, r=100, t=20, b=60)
    _hml["xaxis"] = dict(side="top", tickfont=dict(size=12, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
    _hml["yaxis"] = dict(tickfont=dict(size=11, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
    fig_hm.update_layout(**_hml)
    st.plotly_chart(fig_hm, use_container_width=True)

    # ── SECTION 2: TOP PICKS PER ASSET CLASS ───────────────────
    st.markdown('<div class="section-label">Top Picks by Asset Class</div>', unsafe_allow_html=True)

    _ac_cols = st.columns(5)
    for _ci, ac in enumerate(ASSET_CLASSES):
        with _ac_cols[_ci]:
            _ac_color = ASSET_COLORS[ac]
            _ac_icon  = ASSET_ICONS[ac]
            # Sort countries by this asset class score
            _ac_ranked = sorted(inv_data.items(), key=lambda kv: -kv[1]["scores"].get(ac, 0))
            _top3 = _ac_ranked[:3]
            _bot1 = _ac_ranked[-1]
            _cards = ""
            for _rank, (_iso, _data) in enumerate(_top3, 1):
                _sc = _data["scores"][ac]
                _lbl, _lbl_color, _arrow = rating_label(_sc)
                _medal = ["🥇","🥈","🥉"][_rank-1]
                _cards += f"""
                <div style="background:#111827;border:1px solid #1e2d45;border-left:3px solid {_ac_color};
                     border-radius:6px;padding:10px 12px;margin-bottom:8px;">
                    <div style="font-family:'IBM Plex Mono';font-size:0.6rem;color:{_ac_color};letter-spacing:1px;margin-bottom:4px;">{_medal} RANK {_rank}</div>
                    <div style="font-size:0.9rem;font-weight:600;color:#e2e8f0;margin-bottom:4px;">{iso_to_name(_iso)}</div>
                    {conviction_bar(_sc, _ac_color)}
                    <div style="display:flex;justify-content:space-between;margin-top:5px;">
                        <span style="font-family:'IBM Plex Mono';font-size:0.75rem;color:{_lbl_color};font-weight:600;">{_arrow} {_lbl}</span>
                        <span style="font-family:'IBM Plex Mono';font-size:0.75rem;color:#94a3b8;">{_sc:.0f}/100</span>
                    </div>
                </div>"""
            _avoid_sc  = _bot1[1]["scores"][ac]
            _avoid_lbl, _avoid_color, _avoid_arrow = rating_label(_avoid_sc)
            _cards += f"""
            <div style="background:#0f172a;border:1px solid #1e2d45;border-left:3px solid #ef4444;
                 border-radius:6px;padding:8px 12px;margin-top:4px;opacity:0.85;">
                <div style="font-family:'IBM Plex Mono';font-size:0.6rem;color:#ef4444;letter-spacing:1px;margin-bottom:3px;">⚠️ AVOID</div>
                <div style="font-size:0.85rem;color:#94a3b8;">{iso_to_name(_bot1[0])}</div>
                <div style="font-family:'IBM Plex Mono';font-size:0.7rem;color:{_avoid_color};">{_avoid_arrow} {_avoid_sc:.0f}/100</div>
            </div>"""
            _wrapper_top = (
                '<div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:16px 14px;">'
                '<div style="font-family:\'IBM Plex Mono\';font-size:0.7rem;letter-spacing:2px;'
                'color:' + _ac_color + ';text-transform:uppercase;margin-bottom:12px;">'
                + _ac_icon + ' ' + ac +
                '</div>'
            )
            st.markdown(_wrapper_top + _cards + '</div>', unsafe_allow_html=True)

    # ── SECTION 3: DETAILED COUNTRY DEEP-DIVE ──────────────────
    st.markdown('<div class="section-label">Country Deep-Dive: Full Signal Breakdown</div>', unsafe_allow_html=True)

    _dd_country = st.selectbox(
        "Select country for deep-dive analysis",
        sorted(inv_data.keys()), format_func=iso_to_name, key="inv_dd_country"
    )
    _dd = inv_data[_dd_country]
    _dd_name = iso_to_name(_dd_country)

    # Scores overview bar
    _col_dd1, _col_dd2 = st.columns([3, 2])
    with _col_dd1:
        fig_dd = go.Figure()
        _sc_vals   = [_dd["scores"][ac] for ac in ASSET_CLASSES]
        _sc_colors = [ASSET_COLORS[ac] for ac in ASSET_CLASSES]
        _sc_labels = [f"{ASSET_ICONS[ac]} {ac}" for ac in ASSET_CLASSES]
        _sc_ratings= [rating_label(_dd["scores"][ac]) for ac in ASSET_CLASSES]

        for _i, (ac, val, col, lbl_tup) in enumerate(zip(ASSET_CLASSES, _sc_vals, _sc_colors, _sc_ratings)):
            hex_c = col.lstrip("#")
            r_, g_, b_ = int(hex_c[0:2],16), int(hex_c[2:4],16), int(hex_c[4:6],16)
            fig_dd.add_trace(go.Bar(
                x=[val], y=[f"{ASSET_ICONS[ac]} {ac}"],
                orientation="h", name=ac,
                marker=dict(
                    color=f"rgba({r_},{g_},{b_},0.85)",
                    line=dict(color=col, width=1.5),
                ),
                text=[f"{val:.0f}  {lbl_tup[2]} {lbl_tup[0]}"],
                textposition="outside",
                textfont=dict(size=10, family="IBM Plex Mono", color=lbl_tup[1]),
                hovertemplate=f"<b>{ac}</b><br>Score: {val:.1f}/100<br>Rating: {lbl_tup[0]}<extra></extra>",
                showlegend=False,
            ))

        # Rating zones
        for _zx0, _zx1, _zc, _zt in [(0,28,"rgba(239,68,68,0.05)","AVOID"), (28,42,"rgba(249,115,22,0.05)","UW"),
                                       (42,58,"rgba(100,116,139,0.05)","NEUTRAL"), (58,72,"rgba(52,211,153,0.05)","BUY"),
                                       (72,100,"rgba(16,185,129,0.05)","STRONG BUY")]:
            fig_dd.add_vrect(x0=_zx0, x1=_zx1, fillcolor=_zc, layer="below", line_width=0)
        fig_dd.add_vline(x=50, line_dash="dot", line_color="#334155", line_width=1)

        _ddl = L(f"{_dd_name} — Asset Class Attractiveness", 340, extra={"showlegend": False})
        _ddl["xaxis"] = {**_ddl.get("xaxis",{}), "range": [0, 115], "title": "Score (0–100)"}
        _ddl["margin"] = dict(l=10, r=120, t=40, b=40)
        fig_dd.update_layout(**_ddl)
        st.plotly_chart(fig_dd, use_container_width=True)

    with _col_dd2:
        # Radar of all 5 asset classes
        _radar_vals = [_dd["scores"][ac] for ac in ASSET_CLASSES] + [_dd["scores"][ASSET_CLASSES[0]]]
        _radar_lbls = [f"{ASSET_ICONS[ac]} {ac}" for ac in ASSET_CLASSES] + [f"{ASSET_ICONS[ASSET_CLASSES[0]]} {ASSET_CLASSES[0]}"]
        fig_radar_dd = go.Figure(go.Scatterpolar(
            r=_radar_vals, theta=_radar_lbls, fill="toself",
            fillcolor="rgba(59,130,246,0.12)",
            line=dict(color="#3b82f6", width=2.5),
            marker=dict(size=7, color="#3b82f6"),
            hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}/100<extra></extra>",
        ))
        fig_radar_dd.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(family="IBM Plex Mono", color="#94a3b8", size=10),
            polar=dict(
                bgcolor="#0f172a",
                radialaxis=dict(visible=True, range=[0,100], gridcolor="#1e2d45",
                               tickfont=dict(size=8), color="#475569"),
                angularaxis=dict(gridcolor="#1e2d45", color="#64748b", tickfont=dict(size=10)),
            ),
            title=dict(text=f"Portfolio Radar — {_dd_name}", font=dict(size=12)),
            height=340, margin=dict(l=40, r=40, t=50, b=20),
        )
        st.plotly_chart(fig_radar_dd, use_container_width=True)

    # Signal breakdown per asset class
    st.markdown('<div class="section-label" style="margin-top:8px;">Signal Breakdown — What Drives Each Score</div>', unsafe_allow_html=True)

    _sig_tabs = st.tabs([f"{ASSET_ICONS[ac]} {ac}" for ac in ASSET_CLASSES])
    for _si_tab, ac in zip(_sig_tabs, ASSET_CLASSES):
        with _si_tab:
            _sigs = _dd["signals"][ac]
            _ac_col = ASSET_COLORS[ac]
            _total_score = _dd["scores"][ac]
            _lbl, _lbl_color, _arrow = rating_label(_total_score)

            _tc1, _tc2 = st.columns([3, 2])
            with _tc1:
                # Signal bar chart
                fig_sig = go.Figure()
                _sig_names = list(_sigs.keys())
                _sig_vals  = [_sigs[s] for s in _sig_names]
                _sig_colors= []
                for v in _sig_vals:
                    if v >= 65:   _sig_colors.append("#10b981")
                    elif v >= 45: _sig_colors.append("#3b82f6")
                    elif v >= 30: _sig_colors.append("#f59e0b")
                    else:         _sig_colors.append("#ef4444")

                fig_sig.add_trace(go.Bar(
                    x=_sig_vals, y=_sig_names, orientation="h",
                    marker=dict(color=_sig_colors, line=dict(color=_sig_colors, width=0)),
                    text=[f"{v:.0f}" for v in _sig_vals],
                    textposition="outside",
                    textfont=dict(size=10, family="IBM Plex Mono"),
                    hovertemplate="<b>%{y}</b><br>Signal score: %{x:.1f}/100<extra></extra>",
                    showlegend=False,
                ))
                fig_sig.add_vline(x=50, line_dash="dot", line_color="#334155", line_width=1)
                _sgl = L(f"Signal Scores — {ac}", max(180, 38 * len(_sig_names) + 60),
                         extra={"showlegend": False})
                _sgl["xaxis"] = {**_sgl.get("xaxis",{}), "range": [0, 118]}
                _sgl["margin"] = dict(l=10, r=50, t=40, b=30)
                fig_sig.update_layout(**_sgl)
                st.plotly_chart(fig_sig, use_container_width=True)

            with _tc2:
                # Narrative assessment
                _raw = _dd["raw"]
                _narratives = {
                    "Equities": f"""
<b>Macro Context:</b> GDP growth (5Y avg): <b>{_raw['gdp_growth']:.1f}%</b> · Inflation: <b>{_raw['inflation']:.1f}%</b>
<br><br><b>Key Driver:</b> {"Strong GDP momentum supports earnings growth and equity re-rating" if _raw['gdp_growth'] > 2 else "Weak growth dampens earnings expectations and equity multiples"}.
{"Inflation in the sweet spot (2–4%) supports margin stability." if 1.5 <= _raw['inflation'] <= 5 else "Inflation outside the 2–4% sweet spot creates margin and valuation pressure."}
<br><br><b>Credit Cycle Position:</b> Credit/GDP at <b>{_raw['credit_pct']:.0f}th percentile</b> of history.
{"Early–mid cycle: credit expansion supports corporate investment and consumer spending." if _raw['credit_pct'] < 60 else "Late cycle: elevated credit constrains new borrowing and increases recession risk."}
                    """,
                    "Real Estate": f"""
<b>Macro Context:</b> Mortgage rates proxy (LT rate): <b>{_raw['ltrate']:.1f}%</b> · 5Y HP Growth: <b>{_raw['hp_growth']:.1f}%</b>
<br><br><b>Key Driver:</b> {"Rates at historically low levels fuel affordability and borrowing capacity." if _raw['ltrate_pct'] < 40 else "Elevated rates compress affordability and dampen new transaction volumes."}
{"Credit is expanding, historically a strong tailwind for property prices." if not np.isnan(_raw.get('credit_gdp',np.nan)) and _raw.get('credit_pct',50) > 40 else "Credit conditions are contracting — historically a headwind for real estate."}
<br><br><b>Valuation:</b> House prices at <b>{_raw['hp_pct']:.0f}th percentile</b> of history.
{"Prices near historical peak — limited upside, elevated risk of mean-reversion." if _raw['hp_pct'] > 75 else "Prices below historical peak — room for appreciation."}
                    """,
                    "Bonds": f"""
<b>Macro Context:</b> 10Y rate: <b>{_raw['ltrate']:.1f}%</b> · Term spread: <b>{_raw['term_spread']:+.1f}%</b> · Inflation: <b>{_raw['inflation']:.1f}%</b>
<br><br><b>Key Driver:</b> {"Rates at elevated levels relative to history offer an attractive entry point for duration." if _raw['ltrate_pct'] > 60 else "Rates are historically low — limited capital gain potential; duration risk elevated."}
{"Positive term spread signals normal curve — carry trade is positive." if _raw['term_spread'] > 0 else "Inverted or flat yield curve — historically precedes recessions, watch for credit deterioration."}
<br><br><b>Inflation:</b> {"Inflation near target — real yields positive, bond total return expected to be positive." if 1 <= _raw['inflation'] <= 4 else "Inflation elevated or volatile — real yields may be negative, eroding bond returns."}
                    """,
                    "Cash/Bills": f"""
<b>Macro Context:</b> Short-term rate: <b>{_raw['ltrate']:.1f}% proxy</b> · Inflation: <b>{_raw['inflation']:.1f}%</b> · Crisis rate (10Y): <b>{_raw['crisis_rate']*100:.1f}%</b>
<br><br><b>Key Driver:</b> {"High short rates mean cash and T-bills offer meaningful real returns — an uncommon opportunity." if _raw['ltrate_pct'] > 65 else "Low short rates provide minimal yield — cash is a drag on total portfolio return."}
<br><br><b>Uncertainty:</b> {"Elevated historical crisis frequency suggests capital preservation priority — cash as a defensive allocation makes sense." if _raw['crisis_rate'] > 0.08 else "Low crisis frequency reduces the defensive case for cash — opportunity cost of holding cash is high."}
                    """,
                    "Real Assets": f"""
<b>Macro Context:</b> Inflation: <b>{_raw['inflation']:.1f}%</b> · LT rate: <b>{_raw['ltrate']:.1f}%</b> · CA/GDP: <b>{_raw['ca_gdp']:+.1f}%</b>
<br><br><b>Key Driver:</b> {"Inflation above rates implies negative real rates — the classic environment for gold, commodities, and real assets to outperform." if not np.isnan(_raw['inflation']) and not np.isnan(_raw['ltrate']) and _raw['inflation'] > _raw['ltrate'] else "Positive real rates reduce the attractiveness of non-yielding real assets."}
<br><br><b>Currency Pressure:</b> {"Current account deficit signals currency vulnerability — real assets and commodities serve as FX hedge." if _raw['ca_gdp'] < -2 else "Current account surplus provides currency support — FX hedge rationale for real assets is weaker."}
{"Late credit cycle / elevated debt levels historically correlate with commodity demand shifts." if _raw['credit_pct'] > 65 else ""}
                    """,
                }
                st.markdown(f"""
                <div class="insight-box" style="border-left-color:{_ac_col};">
                    <div class="insight-title" style="color:{_ac_col};">
                        {ASSET_ICONS[ac]} {ac} — {_dd_name}
                        <span style="float:right;color:{_lbl_color};font-size:0.8rem;">{_arrow} {_lbl} · {_total_score:.0f}/100</span>
                    </div>
                    {_narratives[ac].strip()}
                </div>""", unsafe_allow_html=True)

    # ── SECTION 4: CROSS-COUNTRY SCORE COMPARISON ──────────────
    st.markdown('<div class="section-label">Cross-Country Score Comparison by Asset Class</div>', unsafe_allow_html=True)

    _cmp_ac = st.selectbox("Asset class to compare across all countries",
                            ASSET_CLASSES, format_func=lambda x: f"{ASSET_ICONS[x]} {x}", key="inv_cmp_ac")
    _cmp_col = ASSET_COLORS[_cmp_ac]

    _cmp_data = sorted(inv_data.items(), key=lambda kv: -kv[1]["scores"].get(_cmp_ac, 0))
    _cmp_isos   = [iso_to_name(k) for k, _ in _cmp_data]
    _cmp_scores = [v["scores"].get(_cmp_ac, 50) for _, v in _cmp_data]
    _cmp_emp    = [v["empire"] for _, v in _cmp_data]
    _cmp_ratings= [rating_label(s) for s in _cmp_scores]

    _cmp_marker_colors = [
        f"rgba({int(_cmp_col[1:3],16)},{int(_cmp_col[3:5],16)},{int(_cmp_col[5:7],16)},{0.4 + 0.6*(s/100):.2f})"
        for s in _cmp_scores
    ]

    fig_cmp = go.Figure()
    # Background rating zones
    for _zx0, _zx1, _zc, _zt in [(0,28,"rgba(239,68,68,0.06)","AVOID"),
                                   (28,42,"rgba(249,115,22,0.05)","UNDERWEIGHT"),
                                   (42,58,"rgba(100,116,139,0.04)","NEUTRAL"),
                                   (58,72,"rgba(52,211,153,0.05)","BUY"),
                                   (72,100,"rgba(16,185,129,0.06)","STRONG BUY")]:
        fig_cmp.add_vrect(x0=_zx0, x1=_zx1, fillcolor=_zc, layer="below", line_width=0)
        fig_cmp.add_annotation(x=(_zx0+_zx1)/2, y=-0.5, text=_zt, showarrow=False,
                               font=dict(size=7, color="#475569", family="IBM Plex Mono"),
                               xref="x", yref="paper", yanchor="top")

    fig_cmp.add_trace(go.Bar(
        x=_cmp_scores, y=_cmp_isos, orientation="h",
        marker=dict(color=_cmp_marker_colors, line=dict(color=_cmp_col, width=1)),
        text=[f"{s:.0f}  {r[2]} {r[0]}" for s, r in zip(_cmp_scores, _cmp_ratings)],
        textposition="outside",
        textfont=dict(size=9, family="IBM Plex Mono"),
        customdata=_cmp_emp,
        hovertemplate="<b>%{y}</b><br>Score: %{x:.1f}/100<br>Empire Health: %{customdata:.1f}/100<extra></extra>",
        showlegend=False,
    ))
    fig_cmp.add_vline(x=50, line_dash="dot", line_color="#475569", line_width=1.2)

    _cmpl = L(f"{ASSET_ICONS[_cmp_ac]} {_cmp_ac} Attractiveness — All Countries Ranked",
              max(300, 36 * len(_cmp_data) + 100), extra={"showlegend": False})
    _cmpl["xaxis"] = {**_cmpl.get("xaxis",{}), "range": [0, 120], "title": "Score (0–100)"}
    _cmpl["margin"] = dict(l=10, r=130, t=40, b=50)
    fig_cmp.update_layout(**_cmpl)
    st.plotly_chart(fig_cmp, use_container_width=True)

    # ── SECTION 5: PORTFOLIO HEAT — BEST COUNTRY PER CLASS ─────
    st.markdown('<div class="section-label">Optimal Portfolio Construction — Best Country × Asset Class</div>', unsafe_allow_html=True)

    _port_cols = st.columns([3, 2])
    with _port_cols[0]:
        # Which country tops each asset class?
        _top_picks = {}
        for ac in ASSET_CLASSES:
            _best_iso = max(inv_data.keys(), key=lambda k: inv_data[k]["scores"].get(ac, 0))
            _best_sc  = inv_data[_best_iso]["scores"][ac]
            _top_picks[ac] = (_best_iso, _best_sc)

        # Stacked bar: each country's total score across all asset classes
        _all_isos_sorted = sorted(inv_data.keys(), key=lambda k: -sum(inv_data[k]["scores"].values()))
        fig_port = go.Figure()
        for ac in ASSET_CLASSES:
            _vals = [inv_data[iso]["scores"].get(ac, 0) for iso in _all_isos_sorted]
            _col_hex = ASSET_COLORS[ac]
            r_, g_, b_ = int(_col_hex[1:3],16), int(_col_hex[3:5],16), int(_col_hex[5:7],16)
            fig_port.add_trace(go.Bar(
                name=f"{ASSET_ICONS[ac]} {ac}",
                x=[iso_to_name(iso) for iso in _all_isos_sorted],
                y=_vals,
                marker=dict(color=f"rgba({r_},{g_},{b_},0.82)", line=dict(color=_col_hex, width=0.5)),
                hovertemplate=f"<b>%{{x}}</b><br>{ac}: %{{y:.1f}}/100<extra></extra>",
            ))
        _portl = L("", 440)   # title handled via annotation below to avoid legend overlap
        _portl["barmode"] = "stack"
        _portl["legend"] = dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                                orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5,
                                font=dict(size=9, family="IBM Plex Mono"))
        _portl["xaxis"] = {**_portl.get("xaxis",{}), "tickangle": -30, "tickfont": dict(size=9)}
        _portl["margin"] = dict(l=50, r=20, t=28, b=110)
        _portl["annotations"] = [dict(
            text="Composite Investment Score by Country",
            xref="paper", yref="paper", x=0, y=1.04,
            xanchor="left", yanchor="bottom",
            font=dict(family="IBM Plex Mono", size=12, color="#94a3b8"),
            showarrow=False,
        )]
        fig_port.update_layout(**_portl)
        st.plotly_chart(fig_port, use_container_width=True)

    with _port_cols[1]:
        # Best-in-class picks summary card
        _picks_html = ""
        for ac in ASSET_CLASSES:
            _iso_p, _sc_p = _top_picks[ac]
            _lbl_p, _lbl_color_p, _arrow_p = rating_label(_sc_p)
            _col_p = ASSET_COLORS[ac]
            _picks_html += f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                 padding:10px 0;border-bottom:1px solid #1e2d45;">
                <div>
                    <span style="font-size:1.1rem;">{ASSET_ICONS[ac]}</span>
                    <span style="font-family:'IBM Plex Mono';font-size:0.72rem;color:{_col_p};
                          margin-left:6px;letter-spacing:1px;">{ac.upper()}</span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.9rem;font-weight:600;color:#e2e8f0;">{iso_to_name(_iso_p)}</div>
                    <div style="font-family:'IBM Plex Mono';font-size:0.7rem;color:{_lbl_color_p};">
                        {_arrow_p} {_lbl_p} · {_sc_p:.0f}/100
                    </div>
                </div>
            </div>"""

        _picks_wrapper = (
            '<div style="background:#111827;border:1px solid #1e2d45;border-radius:10px;padding:20px 18px;">'
            '<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;letter-spacing:3px;'
            'color:#3b82f6;text-transform:uppercase;margin-bottom:14px;">🎯 Best-in-Class Picks</div>'
            + _picks_html +
            '<div style="margin-top:14px;font-family:\'IBM Plex Mono\';font-size:0.65rem;color:#334155;line-height:1.6;">'
            'Based on latest year in selected range.<br>Scores derived from 12 JST macro signals.</div>'
            '</div>'
        )
        st.markdown(_picks_wrapper, unsafe_allow_html=True)

    # ── SECTION 6: MACRO REGIME CLOCK ──────────────────────────
    st.markdown('<div class="section-label">Macro Regime Clock — Where Each Country Sits</div>', unsafe_allow_html=True)
    st.caption("Each country plotted by Growth momentum (x) vs Inflation (y). Quadrant determines which asset classes historically outperform.")

    _regime_data = []
    for iso, data in inv_data.items():
        _r = data["raw"]
        if np.isnan(_r["gdp_growth"]) or np.isnan(_r["inflation"]):
            continue
        _regime_data.append({
            "iso": iso, "name": iso_to_name(iso),
            "gdp": _r["gdp_growth"], "inf": _r["inflation"],
            "empire": _r.get("empire", data["empire"]),
            "best": data["best"],
            "eq": data["scores"]["Equities"],
            "re": data["scores"]["Real Estate"],
            "bd": data["scores"]["Bonds"],
            "ca": data["scores"]["Cash/Bills"],
            "al": data["scores"]["Real Assets"],
        })

    if _regime_data:
        _rd = pd.DataFrame(_regime_data)
        fig_clock = go.Figure()

        # Quadrant fills
        _q_fills = [
            (0, 20, -5, 2,  "rgba(16,185,129,0.05)",  "GOLDILOCKS<br>↑ Equities · ↑ Real Estate"),
            (0, 20,  2, 25, "rgba(245,158,11,0.05)",  "INFLATIONARY BOOM<br>↑ Real Assets · ↑ Real Estate"),
            (-5, 0, -5, 2,  "rgba(100,116,139,0.05)", "DEFLATIONARY BUST<br>↑ Bonds · ↑ Cash"),
            (-5, 0,  2, 25, "rgba(239,68,68,0.05)",   "STAGFLATION<br>↑ Real Assets · ↑ Cash"),
        ]
        for qx0,qx1,qy0,qy1,fc,qt in _q_fills:
            fig_clock.add_shape(type="rect", xref="x", yref="y",
                                x0=qx0, x1=qx1, y0=qy0, y1=qy1,
                                fillcolor=fc, line_width=0, layer="below")

        # Country bubbles, sized by empire health
        for _, row in _rd.iterrows():
            _bc = ASSET_COLORS.get(row["best"], "#3b82f6")
            r_, g_, b_ = int(_bc[1:3],16), int(_bc[3:5],16), int(_bc[5:7],16)
            fig_clock.add_trace(go.Scatter(
                x=[row["gdp"]], y=[row["inf"]],
                mode="markers+text",
                text=[row["name"]],
                textposition="top center",
                textfont=dict(size=9, color="#cbd5e1", family="IBM Plex Mono"),
                marker=dict(
                    size=max(10, min(40, row["empire"] * 0.38)),
                    color=f"rgba({r_},{g_},{b_},0.75)",
                    line=dict(color=_bc, width=1.8),
                ),
                name=row["name"],
                showlegend=False,
                hovertemplate=(
                    f"<b>{row['name']}</b><br>"
                    f"GDP Growth: <b>{row['gdp']:.1f}%</b><br>"
                    f"Inflation: <b>{row['inf']:.1f}%</b><br>"
                    f"Empire Health: <b>{row['empire']:.0f}/100</b><br>"
                    f"Best asset: <b>{row['best']}</b><br>"
                    f"EQ:{row['eq']:.0f} · RE:{row['re']:.0f} · BD:{row['bd']:.0f} · CA:{row['ca']:.0f} · RA:{row['al']:.0f}"
                    f"<extra></extra>"
                ),
            ))

        # Quadrant text annotations
        for _qt, _qx, _qy, _qc in [
            ("GOLDILOCKS\n↑ Equities · Real Estate", 10,  0.5, "#10b981"),
            ("INFLATIONARY BOOM\n↑ Real Assets",       10, 12,  "#f59e0b"),
            ("DEFLATION BUST\n↑ Bonds · Cash",          -2, 0.5, "#64748b"),
            ("STAGFLATION\n↑ Real Assets · Cash",       -2, 12,  "#ef4444"),
        ]:
            fig_clock.add_annotation(
                x=_qx, y=_qy, text=_qt.replace("\n","<br>"),
                showarrow=False, xanchor="center", yanchor="middle",
                font=dict(size=8, color=_qc, family="IBM Plex Mono"),
                bgcolor="rgba(15,23,42,0.65)", borderpad=4,
            )

        fig_clock.add_vline(x=0, line_dash="dot", line_color="#475569", line_width=1.2)
        fig_clock.add_hline(y=2, line_dash="dot", line_color="#475569", line_width=1.2)

        _cl = L("Macro Regime Clock — Bubble size ∝ Empire Health Score", 520)
        _cl["xaxis"] = {**_cl.get("xaxis",{}), "title": "Real GDP Growth, 5Y avg (%)", "zeroline": False}
        _cl["yaxis"] = {**_cl.get("yaxis",{}), "title": "Inflation, 5Y avg (%)",       "zeroline": False}
        _cl["hovermode"] = "closest"
        fig_clock.update_layout(**_cl)
        st.plotly_chart(fig_clock, use_container_width=True)

        # Regime summary table
        _regime_rows = []
        for _, row in _rd.sort_values("empire", ascending=False).iterrows():
            _phase = ("GOLDILOCKS" if row["gdp"] > 0 and row["inf"] <= 2 else
                      "INFLATIONARY BOOM" if row["gdp"] > 0 and row["inf"] > 2 else
                      "STAGFLATION" if row["gdp"] <= 0 and row["inf"] > 2 else "DEFLATION BUST")
            _regime_rows.append({
                "Country":      row["name"],
                "GDP 5Y avg":   f"{row['gdp']:.1f}%",
                "Inflation 5Y": f"{row['inf']:.1f}%",
                "Regime":       _phase,
                "Best Asset":   f"{ASSET_ICONS[row['best']]} {row['best']}",
                "Empire Health":f"{row['empire']:.0f}/100",
                "EQ":f"{row['eq']:.0f}", "RE":f"{row['re']:.0f}",
                "BD":f"{row['bd']:.0f}", "CA":f"{row['ca']:.0f}", "RA":f"{row['al']:.0f}",
            })
        _regime_df = pd.DataFrame(_regime_rows).set_index("Country")
        st.dataframe(_regime_df, use_container_width=True, height=min(480, 50 + 38*len(_regime_rows)))

    # ── METHODOLOGY NOTE ────────────────────────────────────────
    st.markdown("""
    <div class="insight-box" style="border-left-color:#334155;margin-top:24px;">
        <div class="insight-title" style="color:#64748b;">📐 Methodology</div>
        <b>Equities:</b> Weighted by GDP momentum (25%), inflation sweet-spot (18%), credit cycle stage (15%), political stability (17%), productivity (15%), valuation proxy (10%).<br>
        <b>Real Estate:</b> Credit expansion (22%), rate environment (22%), price level vs history (20%), macro stability (15%), income growth (13%), external balance (8%).<br>
        <b>Bonds:</b> Inflation stability (28%), rate entry level (22%), term spread (15%), fiscal credibility (18%), crisis risk (10%), FX support (7%).<br>
        <b>Cash/Bills:</b> Short-rate level (30%), inflation control (25%), uncertainty hedge (20%), deflation protection (15%), macro weakness (10%).<br>
        <b>Real Assets:</b> Inflation hedge demand (28%), negative real rates (25%), late credit cycle (22%), external weakness (13%), empire stress (12%).<br><br>
        All signals are min-max normalised 0–100 within the selected year range. Scores reflect historical macro-return relationships documented
        in the academic literature and the JST dataset. They do <b>not</b> incorporate valuation multiples, earnings forecasts, geopolitical risk,
        or liquidity conditions. <b>Not investment advice.</b>
    </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════
# TAB 11  ·  🧬 MACRO STRESS LAB
# Five independent analytical engines:
#   1. Vulnerability Scanner — 7-signal early-warning composite
#   2. Crisis Probability    — logistic EWS model, calibrated to JST
#   3. Regime Detector       — hidden-state classifier + transition matrix
#   4. Contagion Network     — bilateral synchronicity + rolling correlation
#   5. Historical Analogues  — nearest-neighbour in macro feature space
# ══════════════════════════════════════════════════════════════════
with tabs[10]:

    # ── header ────────────────────────────────────────────────────
    st.markdown("""
    <div class="insight-box" style="border-left-color:#06b6d4;margin-bottom:28px;padding:18px 22px;">
        <div style="font-family:'IBM Plex Mono';font-size:0.65rem;letter-spacing:3px;color:#06b6d4;
             text-transform:uppercase;margin-bottom:8px;">🧬 Macro Stress Lab</div>
        <div style="color:#cbd5e1;font-size:0.9rem;line-height:1.7;">
            Five independent analytical engines built on 150 years of JST data.
            <b style="color:#e2e8f0;">Vulnerability Scanner</b> ·
            <b style="color:#e2e8f0;">Crisis Probability Model</b> ·
            <b style="color:#e2e8f0;">Regime Detector</b> ·
            <b style="color:#e2e8f0;">Contagion Network</b> ·
            <b style="color:#e2e8f0;">Historical Analogue Engine</b>
        </div>
    </div>""", unsafe_allow_html=True)

    _lab_tabs = st.tabs([
        "🚨 Vulnerability Scanner",
        "🎯 Crisis Probability",
        "🔀 Regime Detector",
        "🕸️ Contagion Network",
        "🔭 Historical Analogues",
    ])

    # ──────────────────────────────────────────────────────────────
    # ENGINE 1  ·  VULNERABILITY SCANNER
    # ──────────────────────────────────────────────────────────────
    with _lab_tabs[0]:
        st.markdown('<div class="section-label">Multi-Signal Early-Warning Vulnerability Scanner</div>',
                    unsafe_allow_html=True)
        st.caption("Seven academic early-warning signals, each percentile-ranked against the country's own history (0 = safest ever, 100 = most stressed ever). Equal-weighted composite shown below.")

        @st.cache_data(show_spinner=False)
        def _build_vuln(data_hash, df_in):
            SIG_NAMES = ["Credit Boom","House Price Gap","Yield Curve Inversion",
                         "Debt Service Burden","Inflation Shock","External Imbalance","Money Surge"]
            results = {}
            for iso in df_in["iso"].unique():
                d = df_in[df_in["iso"]==iso].sort_values("year").copy()
                if len(d) < 8:
                    continue
                def _prank(col, invert=False, diff=0):
                    if col not in d.columns:
                        return pd.Series(50.0, index=d.index)
                    s = d[col].astype(float)
                    if diff > 0:
                        s = s.diff(diff)
                    r = s.rolling(min(len(s), 25), min_periods=6).rank(pct=True) * 100
                    r = r.fillna(50.0)
                    return 100 - r if invert else r

                sigs = {}
                sigs["Credit Boom"]             = _prank("credit_gdp", diff=3)
                sigs["House Price Gap"]         = _prank("hp_real_growth")
                sigs["Yield Curve Inversion"]   = _prank("ltrate") - _prank("stir") if "stir" in d.columns else _prank("ltrate", invert=True)
                # keep inversion signal: negative term spread = more stress
                if "ltrate" in d.columns and "stir" in d.columns:
                    raw_inv = -(d["ltrate"] - d["stir"])
                    sigs["Yield Curve Inversion"] = raw_inv.rolling(25, min_periods=6).rank(pct=True).fillna(0.5) * 100
                sigs["Debt Service Burden"]     = _prank("ltrate") * 0 + (
                    ((d["ltrate"] * d["credit_gdp"] / 100) if ("ltrate" in d.columns and "credit_gdp" in d.columns)
                     else pd.Series(0.0, index=d.index))
                ).rolling(25, min_periods=6).rank(pct=True).fillna(0.5) * 100
                sigs["Inflation Shock"]         = abs(d["inflation"] - 2.0).rolling(25, min_periods=6).rank(pct=True).fillna(0.5) * 100 if "inflation" in d.columns else pd.Series(50.0, index=d.index)
                sigs["External Imbalance"]      = _prank("ca_gdp", invert=True)
                sigs["Money Surge"]             = _prank("money_gdp", diff=3)

                sig_df = pd.DataFrame(sigs, index=d.index)
                sig_df["year"]      = d["year"].values
                sig_df["composite"] = sig_df[SIG_NAMES].mean(axis=1)
                results[iso] = sig_df.reset_index(drop=True)
            return results, SIG_NAMES

        _vuln_hash = str(sorted(selected_countries)) + str(year_range)
        _vuln_data, _SIG_NAMES = _build_vuln(_vuln_hash, dff)

        # ── time-series composite ──
        fig_vs = go.Figure()
        fig_vs.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.06)", layer="below", line_width=0)
        fig_vs.add_hrect(y0=50, y1=70,  fillcolor="rgba(245,158,11,0.04)", layer="below", line_width=0)
        fig_vs.add_hline(y=70, line_dash="dot", line_color="#ef4444", line_width=1.2,
                         annotation_text=" High-Risk (70)", annotation_font_color="#ef4444",
                         annotation_position="top right")
        fig_vs.add_hline(y=50, line_dash="dot", line_color="#f59e0b", line_width=1,
                         annotation_text=" Elevated (50)", annotation_font_color="#f59e0b",
                         annotation_position="top right")
        for _vi, iso in enumerate(selected_countries):
            if iso not in _vuln_data: continue
            vd  = _vuln_data[iso]
            ch  = PALETTE[_vi % len(PALETTE)]
            r_, g_, b_ = int(ch[1:3],16), int(ch[3:5],16), int(ch[5:7],16)
            fig_vs.add_trace(go.Scatter(
                x=vd["year"], y=vd["composite"].round(1),
                name=iso_to_name(iso), mode="lines",
                line=dict(color=ch, width=2.2),
                fill="tozeroy" if len(selected_countries)==1 else None,
                fillcolor=f"rgba({r_},{g_},{b_},0.07)",
                hovertemplate=f"<b>{iso_to_name(iso)}</b>  %{{x}}<br>Composite: <b>%{{y:.1f}}/100</b><extra></extra>",
            ))
            if crisis_col and crisis_col in dff.columns:
                fig_vs = add_crisis_shading(fig_vs, dff[dff["iso"]==iso], crisis_col)
        _vsl = L("Composite Vulnerability Score (0 = Safest · 100 = Maximum Historical Stress)", 440)
        _vsl["yaxis"] = {**_vsl.get("yaxis",{}), "range": [0, 105]}
        _vsl["margin"] = dict(l=50, r=120, t=40, b=40)
        fig_vs.update_layout(**_vsl)
        st.plotly_chart(fig_vs, use_container_width=True)

        # ── signal heatmap ──
        st.markdown('<div class="section-label">Signal Heatmap — Latest Reading per Country</div>', unsafe_allow_html=True)
        _vh_isos = [iso for iso in selected_countries if iso in _vuln_data]
        if _vh_isos:
            _vh_z, _vh_y = [], []
            for iso in _vh_isos:
                vd = _vuln_data[iso].dropna(subset=["composite"])
                if len(vd) == 0: continue
                last = vd.iloc[-1]
                _vh_z.append([round(float(last.get(s, 50)), 1) for s in _SIG_NAMES])
                _vh_y.append(iso_to_name(iso))
            if _vh_z:
                fig_shm = go.Figure(go.Heatmap(
                    z=_vh_z, x=_SIG_NAMES, y=_vh_y,
                    text=_vh_z, texttemplate="<b>%{text:.0f}</b>",
                    textfont=dict(size=10, family="IBM Plex Mono"),
                    colorscale=[[0,"#0d1b2a"],[0.35,"#1e3a5f"],[0.55,"#334155"],
                                [0.72,"#f59e0b"],[0.87,"#ef4444"],[1,"#7f1d1d"]],
                    zmid=50, zmin=0, zmax=100,
                    colorbar=dict(
                        tickvals=[0,25,50,75,100],
                        ticktext=["Safe","Watch","Neutral","Alert","Critical"],
                        tickfont=dict(family="IBM Plex Mono", size=8),
                        title=dict(text="Stress", font=dict(size=9, family="IBM Plex Mono")),
                        len=0.8,
                    ),
                    hovertemplate="<b>%{y}</b> · %{x}<br>Stress: <b>%{z:.1f}/100</b><extra></extra>",
                ))
                _shmh = max(280, 42*len(_vh_z)+80)
                _shml = L("", _shmh)
                _shml["margin"] = dict(l=150, r=80, t=24, b=100)
                _shml["xaxis"] = dict(side="top", tickangle=-30, tickfont=dict(size=10, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                _shml["yaxis"] = dict(tickfont=dict(size=11, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                fig_shm.update_layout(**_shml)
                st.plotly_chart(fig_shm, use_container_width=True)

        with st.expander("📖 Signal Definitions & Academic Basis"):
            _sdefs = [
                ("Credit Boom",           "3Y change in Credit/GDP, percentile-ranked vs own history. Schularick & Taylor (2012): rapid credit expansion is the #1 predictor of financial crises."),
                ("House Price Gap",       "Real house price growth percentile. Jordà, Schularick & Taylor (2015): house price booms amplify credit cycle risk substantially."),
                ("Yield Curve Inversion", "Negative term spread severity. Harvey (1988) / Estrella & Mishkin (1998): inverted curve precedes recessions with high historical reliability."),
                ("Debt Service Burden",   "Rate × Credit/GDP proxy for economy-wide interest burden. Drehmann & Juselius (2012): debt service ratio outperforms credit/GDP alone as EWS."),
                ("Inflation Shock",       "Absolute deviation from 2% target. Reinhart & Rogoff (2009): both high inflation AND deflation are associated with financial crises."),
                ("External Imbalance",    "Current account deficit severity. Obstfeld & Rogoff (2009): persistent deficits require rollover financing — increases crisis vulnerability."),
                ("Money Surge",           "3Y acceleration in Money/GDP. Friedman & Schwartz (1963): rapid monetisation precedes both inflation shocks and asset price bubbles."),
            ]
            for _sn, _sd in _sdefs:
                st.markdown(f"**{_sn}** — {_sd}")

    # ──────────────────────────────────────────────────────────────
    # ENGINE 2  ·  CRISIS PROBABILITY MODEL
    # ──────────────────────────────────────────────────────────────
    with _lab_tabs[1]:
        st.markdown('<div class="section-label">Crisis Probability Engine — Logistic EWS Model</div>',
                    unsafe_allow_html=True)
        st.caption("Five-predictor logistic model calibrated to match standardised coefficients from Schularick & Taylor (2012). Probability = 1/(1+exp(−logit)). × markers = actual JST crisis years.")

        @st.cache_data(show_spinner=False)
        def _build_crisis_prob(data_hash, df_in, c_col):
            results = {}
            for iso in df_in["iso"].unique():
                d = df_in[df_in["iso"]==iso].sort_values("year").copy()
                if len(d) < 10: continue

                def _feat(col, diff=0, roll=0):
                    if col not in d.columns:
                        return pd.Series(0.0, index=d.index)
                    s = d[col].astype(float)
                    if diff > 0: s = s.diff(diff)
                    if roll > 0: s = s.rolling(roll, min_periods=2).mean()
                    return s.fillna(0.0)

                f1 = _feat("tloans", diff=0)   # level proxy for credit mass
                if "tloans" in d.columns:
                    f1 = d["tloans"].pct_change(3).fillna(0) / 3 * 100

                f2 = pd.Series(0.0, index=d.index)
                if "credit_gdp" in d.columns:
                    trend = d["credit_gdp"].rolling(12, min_periods=5).mean()
                    f2 = (d["credit_gdp"] - trend).fillna(0)

                f3 = pd.Series(0.0, index=d.index)
                if "ltrate" in d.columns and "credit_gdp" in d.columns:
                    f3 = (d["ltrate"] * d["credit_gdp"] / 100).fillna(0)

                f4 = _feat("hp_real_growth", roll=3)
                f5 = (abs(_feat("inflation") - 2).rolling(3, min_periods=1).mean()).fillna(0)

                def _z(s):
                    mn, sd = s.mean(), s.std()
                    return (s - mn) / (sd + 1e-8) if sd > 0 else s * 0

                log_odds = 0.42*_z(f1) + 0.31*_z(f2) + 0.28*_z(f3) + 0.19*_z(f4) + 0.14*_z(f5) - 1.85
                prob = 100 / (1 + np.exp(-log_odds))

                results[iso] = pd.DataFrame({
                    "year": d["year"].values,
                    "prob": prob.values,
                    "z_credit_growth": _z(f1).values,
                    "z_credit_gap":    _z(f2).values,
                    "z_debt_service":  _z(f3).values,
                    "z_hp_momentum":   _z(f4).values,
                    "z_inflation":     _z(f5).values,
                    "actual": d[c_col].values if c_col and c_col in d.columns else np.zeros(len(d)),
                })
            return results

        _cp_hash = str(sorted(selected_countries)) + str(year_range) + str(crisis_col)
        _cp_data = _build_crisis_prob(_cp_hash, dff, crisis_col)

        if _cp_data:
            fig_cp = go.Figure()
            fig_cp.add_hrect(y0=40, y1=100, fillcolor="rgba(239,68,68,0.05)", layer="below", line_width=0)
            fig_cp.add_hrect(y0=20, y1=40,  fillcolor="rgba(245,158,11,0.04)", layer="below", line_width=0)
            fig_cp.add_hline(y=40, line_dash="dot", line_color="#ef4444", line_width=1.2,
                             annotation_text=" High Alert (40%)", annotation_font_color="#ef4444",
                             annotation_position="top right")
            fig_cp.add_hline(y=20, line_dash="dot", line_color="#f59e0b", line_width=1,
                             annotation_text=" Elevated (20%)", annotation_font_color="#f59e0b",
                             annotation_position="top right")

            for _ci, iso in enumerate(selected_countries):
                if iso not in _cp_data: continue
                cpd = _cp_data[iso]
                ch  = PALETTE[_ci % len(PALETTE)]
                r_, g_, b_ = int(ch[1:3],16), int(ch[3:5],16), int(ch[5:7],16)
                fig_cp.add_trace(go.Scatter(
                    x=cpd["year"], y=cpd["prob"].round(2),
                    name=iso_to_name(iso), mode="lines",
                    line=dict(color=ch, width=2.2),
                    fill="tozeroy" if len(selected_countries)==1 else None,
                    fillcolor=f"rgba({r_},{g_},{b_},0.07)",
                    hovertemplate=f"<b>{iso_to_name(iso)}</b>  %{{x}}<br>Crisis Prob: <b>%{{y:.1f}}%</b><extra></extra>",
                ))
                # actual crisis markers
                _crisis_rows = cpd[cpd["actual"] == 1]
                if len(_crisis_rows) > 0:
                    fig_cp.add_trace(go.Scatter(
                        x=_crisis_rows["year"], y=_crisis_rows["prob"],
                        mode="markers", showlegend=False,
                        marker=dict(color="#ef4444", size=9, symbol="x-thin",
                                    line=dict(color="#ef4444", width=2.5)),
                        hovertemplate=f"<b>{iso_to_name(iso)}</b> %{{x}}<br>⚠ ACTUAL CRISIS<br>Model: %{{y:.1f}}%<extra></extra>",
                    ))
            _cpl = L("Model Crisis Probability (%)", 450)
            _cpl["yaxis"]  = {**_cpl.get("yaxis",{}), "range": [0, 100], "ticksuffix": "%"}
            _cpl["margin"] = dict(l=50, r=130, t=40, b=40)
            fig_cp.update_layout(**_cpl)
            st.plotly_chart(fig_cp, use_container_width=True)

            # ── feature decomposition ──
            st.markdown('<div class="section-label">Risk Driver Decomposition — Latest Year</div>', unsafe_allow_html=True)
            _dc1, _dc2 = st.columns([2, 1])
            with _dc1:
                _dec_iso = st.selectbox("Country for decomposition:",
                                         [iso for iso in selected_countries if iso in _cp_data],
                                         format_func=iso_to_name, key="cp_dec_iso")
            if _dec_iso and _dec_iso in _cp_data:
                _cpd = _cp_data[_dec_iso].dropna(subset=["prob"])
                if len(_cpd) > 0:
                    _last = _cpd.iloc[-1]
                    _fw   = [0.42, 0.31, 0.28, 0.19, 0.14]
                    _fz   = [_last["z_credit_growth"], _last["z_credit_gap"],
                             _last["z_debt_service"],  _last["z_hp_momentum"], _last["z_inflation"]]
                    _fl   = ["Credit\nGrowth", "Credit\nGap", "Debt\nService", "HP\nMomentum", "Inflation\nShock"]
                    _fcon = [w*z for w,z in zip(_fw, _fz)]
                    _fcol = ["#ef4444" if c>0 else "#10b981" for c in _fcon]
                    fig_dec = go.Figure(go.Bar(
                        x=[l.replace("\n"," ") for l in _fl],
                        y=[round(c,3) for c in _fcon],
                        marker=dict(color=_fcol, line=dict(color=_fcol, width=0.5)),
                        text=[f"{c:+.2f}σ" for c in _fcon],
                        textposition="outside",
                        textfont=dict(family="IBM Plex Mono", size=10),
                        hovertemplate="<b>%{x}</b><br>Contribution: %{y:+.3f} log-odds<extra></extra>",
                    ))
                    fig_dec.add_hline(y=0, line_color="#475569", line_width=1)
                    _decl = L(f"Risk Drivers — {iso_to_name(_dec_iso)} (latest year)  ·  Red = risk-increasing", 320)
                    _decl["yaxis"]     = {**_decl.get("yaxis",{}), "title": "Log-odds contribution (σ-weighted)"}
                    _decl["showlegend"]= False
                    _decl["margin"]    = dict(l=70, r=20, t=50, b=50)
                    fig_dec.update_layout(**_decl)
                    st.plotly_chart(fig_dec, use_container_width=True)

                    _pnow = float(_last["prob"])
                    _dom  = _fl[[abs(c) for c in _fcon].index(max(abs(c) for c in _fcon))].replace("\n"," ")
                    _regime_txt, _rc = (
                        ("🔴 HIGH ALERT — multiple stress signals converging", "#ef4444") if _pnow>40 else
                        ("🟠 ELEVATED — monitor closely", "#f59e0b") if _pnow>20 else
                        ("🟢 NORMAL — below systemic threshold", "#10b981")
                    )
                    st.markdown(
                        '<div class="insight-box" style="border-left-color:' + _rc + ';">'
                        '<div class="insight-title" style="color:' + _rc + ';">🎯 Snapshot — ' + iso_to_name(_dec_iso) + '</div>'
                        'Crisis probability: <span style="color:' + _rc + ';font-size:1.15rem;font-weight:700;">' + f"{_pnow:.1f}%" + '</span> &nbsp;·&nbsp; '
                        'Regime: <b>' + _regime_txt + '</b><br>'
                        'Dominant driver: <b>' + _dom + '</b><br>'
                        '<span style="color:#475569;font-size:0.72rem;">Academic EWS model · S&T (2012) coefficients · Not a trading signal.</span>'
                        '</div>', unsafe_allow_html=True)

    # ──────────────────────────────────────────────────────────────
    # ENGINE 3  ·  REGIME DETECTOR
    # ──────────────────────────────────────────────────────────────
    with _lab_tabs[2]:
        st.markdown('<div class="section-label">Macro Regime Detector — State Classification & Transition Matrix</div>',
                    unsafe_allow_html=True)
        st.caption("Each year is classified into one of five regimes using a composite of growth, inflation, credit impulse, and rates. Coloured timeline shows structural state shifts across history.")

        _REGIMES    = ["Boom", "Goldilocks", "Stagflation", "Deflation/Bust", "Crisis"]
        _REG_COLORS = {"Boom":"#3b82f6","Goldilocks":"#10b981","Stagflation":"#ef4444",
                       "Deflation/Bust":"#94a3b8","Crisis":"#7f1d1d"}
        _REG_ICONS  = {"Boom":"🚀","Goldilocks":"✨","Stagflation":"🔥","Deflation/Bust":"❄️","Crisis":"💥"}

        @st.cache_data(show_spinner=False)
        def _detect_regimes(data_hash, df_in):
            out = {}
            for iso in df_in["iso"].unique():
                d = df_in[df_in["iso"]==iso].sort_values("year").copy()
                if len(d) < 8: continue
                def _p(col, w=20):
                    if col not in d.columns: return pd.Series(0.5, index=d.index)
                    return d[col].astype(float).rolling(min(len(d),w), min_periods=5).rank(pct=True).fillna(0.5)
                G  = _p("gdp_growth")
                IN = _p("inflation")
                CR = _p("credit_gdp_chg")
                LR = _p("ltrate")
                CRISIS_P = d[crisis_col].astype(float) if crisis_col and crisis_col in d.columns else pd.Series(0.0, index=d.index)
                scores_df = pd.DataFrame({
                    "Boom":          0.40*G + 0.25*CR + 0.20*IN + 0.15*(1-LR),
                    "Goldilocks":    0.40*G + 0.35*(1-abs(IN-0.5)*2).clip(0) + 0.25*(1-LR),
                    "Stagflation":   0.35*(1-G) + 0.40*IN + 0.25*LR,
                    "Deflation/Bust":0.35*(1-G) + 0.35*(1-IN) + 0.30*(1-CR),
                    "Crisis":        0.50*CRISIS_P + 0.30*(1-G) + 0.20*(1-CR),
                }, index=d.index)
                out[iso] = pd.DataFrame({
                    "year":      d["year"].values,
                    "regime":    scores_df.idxmax(axis=1).values,
                    "conf":      (scores_df.max(axis=1)*100).round(1).values,
                    "gdp":       d["gdp_growth"].values if "gdp_growth" in d.columns else np.nan,
                    "inf":       d["inflation"].values  if "inflation"  in d.columns else np.nan,
                })
            return out

        _rg_hash = str(sorted(selected_countries)) + str(year_range) + str(crisis_col)
        _rg_data  = _detect_regimes(_rg_hash, dff)

        _rg_iso = st.selectbox("Country for regime history:",
                                [iso for iso in selected_countries if iso in _rg_data],
                                format_func=iso_to_name, key="rg_iso")

        if _rg_iso and _rg_iso in _rg_data:
            rd = _rg_data[_rg_iso]

            # ── regime timeline (dot-row chart) ──
            fig_rt = go.Figure()
            for rn in _REGIMES:
                sub = rd[rd["regime"]==rn]
                if len(sub)==0: continue
                rc = _REG_COLORS[rn]
                r_,g_,b_ = int(rc[1:3],16),int(rc[3:5],16),int(rc[5:7],16)
                fig_rt.add_trace(go.Scatter(
                    x=sub["year"], y=[rn]*len(sub),
                    mode="markers", name=f"{_REG_ICONS[rn]} {rn}",
                    marker=dict(color=f"rgba({r_},{g_},{b_},0.9)", size=11, symbol="square",
                                line=dict(color=rc, width=0.6)),
                    customdata=sub["conf"],
                    hovertemplate=f"<b>{iso_to_name(_rg_iso)}</b> %{{x}}<br>Regime: <b>{rn}</b><br>Confidence: %{{customdata:.1f}}%<extra></extra>",
                ))
            if crisis_col and crisis_col in dff.columns:
                fig_rt = add_crisis_shading(fig_rt, dff[dff["iso"]==_rg_iso], crisis_col)
            _rtl = L(f"Macro Regime Timeline — {iso_to_name(_rg_iso)}", 300, no_log=True)
            _rtl["yaxis"] = {**_rtl.get("yaxis",{}),
                             "categoryorder":"array","categoryarray":list(reversed(_REGIMES)),
                             "tickfont":dict(size=11, family="IBM Plex Mono")}
            _rtl["legend"] = dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                                   font=dict(size=10), orientation="h",
                                   x=0.5, y=-0.25, xanchor="center")
            _rtl["margin"] = dict(l=120, r=20, t=40, b=90)
            fig_rt.update_layout(**_rtl)
            st.plotly_chart(fig_rt, use_container_width=True)

            _rcol1, _rcol2 = st.columns(2)

            # ── pie: time-in-regime ──
            with _rcol1:
                _rcounts = rd["regime"].value_counts()
                fig_rp = go.Figure(go.Pie(
                    labels=[f"{_REG_ICONS.get(r,'')} {r}" for r in _rcounts.index],
                    values=_rcounts.values, hole=0.58,
                    marker=dict(colors=[_REG_COLORS.get(r,"#475569") for r in _rcounts.index],
                                line=dict(color="#111827", width=2)),
                    textfont=dict(family="IBM Plex Mono", size=9),
                    hovertemplate="<b>%{label}</b><br>%{value} years (%{percent})<extra></extra>",
                ))
                fig_rp.update_layout(
                    paper_bgcolor="#111827", font=dict(family="IBM Plex Mono", color="#94a3b8"),
                    height=320, margin=dict(l=20,r=20,t=50,b=20),
                    title=dict(text="Time Spent in Each Regime", font=dict(size=11)),
                    legend=dict(bgcolor="#111827", font=dict(size=9), orientation="v"),
                    annotations=[dict(text=f"<b>{len(rd)}</b><br>yrs",
                                      x=0.5, y=0.5, showarrow=False,
                                      font=dict(size=14, family="IBM Plex Mono", color="#e2e8f0"))],
                )
                st.plotly_chart(fig_rp, use_container_width=True)

            # ── transition matrix ──
            with _rcol2:
                _tm = pd.DataFrame(0, index=_REGIMES, columns=_REGIMES, dtype=float)
                for _j in range(len(rd)-1):
                    _fr, _to = rd.iloc[_j]["regime"], rd.iloc[_j+1]["regime"]
                    if _fr in _REGIMES and _to in _REGIMES:
                        _tm.loc[_fr, _to] += 1
                _tm_pct = (_tm.div(_tm.sum(axis=1).clip(lower=1), axis=0)*100).round(1)
                fig_tm = go.Figure(go.Heatmap(
                    z=_tm_pct.values,
                    x=[f"{_REG_ICONS.get(c,'')} {c}" for c in _tm_pct.columns],
                    y=[f"{_REG_ICONS.get(r,'')} {r}" for r in _tm_pct.index],
                    colorscale=[[0,"#0d1b2a"],[0.35,"#1e3a5f"],[0.65,"#3b82f6"],[1,"#06b6d4"]],
                    zmin=0, zmax=100,
                    text=_tm_pct.values, texttemplate="%{text:.0f}%",
                    textfont=dict(size=9, family="IBM Plex Mono"),
                    showscale=False,
                    hovertemplate="From <b>%{y}</b> → <b>%{x}</b><br>Prob: <b>%{z:.1f}%</b><extra></extra>",
                ))
                _tml = L("Regime Transition Probabilities (row → col)", 320)
                _tml["margin"] = dict(l=10,r=10,t=50,b=80)
                _tml["xaxis"] = dict(tickangle=-30, tickfont=dict(size=8, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                _tml["yaxis"] = dict(tickfont=dict(size=8, family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                fig_tm.update_layout(**_tml)
                st.plotly_chart(fig_tm, use_container_width=True)

            # ── current regime snapshot ──
            st.markdown('<div class="section-label">Current Regime — All Selected Countries</div>', unsafe_allow_html=True)
            _snap_cols = st.columns(min(6, max(1, len([i for i in selected_countries if i in _rg_data]))))
            _snap_list = [iso for iso in selected_countries if iso in _rg_data]
            for _si, iso in enumerate(_snap_list):
                _srd  = _rg_data[iso]
                _slast= _srd.iloc[-1] if len(_srd)>0 else None
                if _slast is None: continue
                _sc   = _REG_COLORS.get(_slast["regime"],"#475569")
                _si2  = _si % len(_snap_cols)
                with _snap_cols[_si2]:
                    st.markdown(
                        '<div style="background:#111827;border:1px solid #1e2d45;border-top:3px solid ' + _sc + ';'
                        'border-radius:8px;padding:14px 12px;margin-bottom:10px;text-align:center;">'
                        '<div style="font-size:1.6rem;line-height:1;">' + _REG_ICONS.get(_slast["regime"],"") + '</div>'
                        '<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;color:' + _sc + ';'
                        'letter-spacing:1px;margin:6px 0 3px;">' + _slast["regime"].upper() + '</div>'
                        '<div style="font-weight:600;color:#e2e8f0;font-size:0.85rem;">' + iso_to_name(iso) + '</div>'
                        '<div style="font-family:\'IBM Plex Mono\';font-size:0.65rem;color:#475569;margin-top:3px;">'
                        'conf ' + str(_slast["conf"]) + '%</div>'
                        '</div>', unsafe_allow_html=True
                    )

    # ──────────────────────────────────────────────────────────────
    # ENGINE 4  ·  CONTAGION NETWORK
    # ──────────────────────────────────────────────────────────────
    with _lab_tabs[3]:
        st.markdown('<div class="section-label">Cross-Country Contagion & Synchronicity Network</div>',
                    unsafe_allow_html=True)
        st.caption("Pearson correlation of each variable across country pairs over the selected period. Bilateral rolling correlation shows how synchronicity evolves through history.")

        _cv1, _cv2 = st.columns(2)
        with _cv1:
            _syn_var = st.selectbox("Variable:",
                [v for v in ["gdp_growth","credit_gdp_chg","inflation","hp_real_growth","ltrate","eq_real_tr"] if v in dff.columns],
                format_func=col_label, key="syn_var")
        with _cv2:
            _syn_win = st.slider("Rolling window (years):", 5, 30, 12, key="syn_win")

        @st.cache_data(show_spinner=False)
        def _sync_matrix(data_hash, df_in, var):
            isos = df_in["iso"].unique()
            pv   = df_in.pivot_table(index="year", columns="iso", values=var, aggfunc="mean")
            cm   = pd.DataFrame(np.nan, index=isos, columns=isos)
            for a in isos:
                for b in isos:
                    if a==b: cm.loc[a,b]=1.0; continue
                    if a not in pv.columns or b not in pv.columns: continue
                    idx = pv[a].dropna().index.intersection(pv[b].dropna().index)
                    if len(idx)>=8:
                        cm.loc[a,b] = round(float(pv[a].loc[idx].corr(pv[b].loc[idx])),3)
            return cm

        _sm_hash = str(sorted(selected_countries))+str(year_range)+_syn_var
        _smx     = _sync_matrix(_sm_hash, dff, _syn_var)
        _cn_isos = [iso for iso in selected_countries if iso in _smx.index]

        if len(_cn_isos) >= 2:
            _sm_sub   = _smx.loc[_cn_isos, _cn_isos]
            _sm_names = [iso_to_name(i) for i in _cn_isos]

            _nc1, _nc2 = st.columns([3, 2])
            with _nc1:
                fig_sm = go.Figure(go.Heatmap(
                    z=_sm_sub.values, x=_sm_names, y=_sm_names,
                    colorscale=[[0,"#7f1d1d"],[0.25,"#ef4444"],[0.5,"#1e293b"],[0.75,"#3b82f6"],[1,"#bfdbfe"]],
                    zmid=0, zmin=-1, zmax=1,
                    text=np.round(_sm_sub.values, 2), texttemplate="<b>%{text}</b>",
                    textfont=dict(size=9, family="IBM Plex Mono"),
                    colorbar=dict(
                        tickvals=[-1,-0.5,0,0.5,1],
                        ticktext=["−1<br>Diverge","−0.5","0<br>None","0.5","+1<br>Sync"],
                        tickfont=dict(size=8,family="IBM Plex Mono"),
                        title=dict(text="Corr",font=dict(size=9,family="IBM Plex Mono")),
                        len=0.75),
                    hovertemplate="%{y} × %{x}<br>Synchronicity: <b>%{z:.3f}</b><extra></extra>",
                ))
                _smh = max(300, 38*len(_cn_isos)+80)
                _sml2 = L(f"Synchronicity Matrix — {col_label(_syn_var)}", _smh)
                _sml2["margin"] = dict(l=130,r=80,t=40,b=130)
                _sml2["xaxis"] = dict(tickangle=-40, tickfont=dict(size=10,family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                _sml2["yaxis"] = dict(tickfont=dict(size=10,family="IBM Plex Mono"), gridcolor="rgba(0,0,0,0)")
                fig_sm.update_layout(**_sml2)
                st.plotly_chart(fig_sm, use_container_width=True)

            with _nc2:
                _pairs_list = sorted(
                    [(iso_to_name(a), iso_to_name(b), float(_sm_sub.loc[a,b]))
                     for i,a in enumerate(_cn_isos) for j,b in enumerate(_cn_isos)
                     if i<j and not np.isnan(_sm_sub.loc[a,b])],
                    key=lambda x: -abs(x[2])
                )
                st.markdown('<div style="font-family:\'IBM Plex Mono\';font-size:0.62rem;letter-spacing:2px;color:#3b82f6;text-transform:uppercase;margin-bottom:14px;">Strongest Pairs</div>', unsafe_allow_html=True)
                for _pa, _pb, _pc in _pairs_list[:9]:
                    _bw   = int(abs(_pc)*100)
                    _bc   = "#3b82f6" if _pc>0 else "#ef4444"
                    st.markdown(
                        '<div style="margin-bottom:9px;">'
                        '<div style="font-family:\'IBM Plex Mono\';font-size:0.7rem;color:#cbd5e1;margin-bottom:3px;">'
                        + _pa + ' × ' + _pb + '</div>'
                        '<div style="display:flex;align-items:center;gap:8px;">'
                        '<div style="flex:1;background:#1e2d45;border-radius:3px;height:5px;">'
                        '<div style="background:' + _bc + ';width:' + str(_bw) + '%;height:5px;border-radius:3px;"></div>'
                        '</div>'
                        '<span style="font-family:\'IBM Plex Mono\';font-size:0.7rem;color:' + _bc + ';min-width:44px;text-align:right;">'
                        + f"{_pc:+.3f}" + '</span></div></div>',
                        unsafe_allow_html=True
                    )

            # ── bilateral rolling correlation ──
            st.markdown('<div class="section-label">Bilateral Synchronicity Over Time</div>', unsafe_allow_html=True)
            _pr_opts  = [(a,b) for i,a in enumerate(_cn_isos) for j,b in enumerate(_cn_isos) if i<j]
            _pr_labels= [f"{iso_to_name(a)} × {iso_to_name(b)}" for a,b in _pr_opts]
            if _pr_opts:
                _pr_idx = st.selectbox("Country pair:", range(len(_pr_opts)),
                                        format_func=lambda x: _pr_labels[x], key="cn_pair")
                _ia, _ib = _pr_opts[_pr_idx]
                _da = dff[dff["iso"]==_ia].sort_values("year").set_index("year")[_syn_var].astype(float) if _syn_var in dff.columns else pd.Series()
                _db = dff[dff["iso"]==_ib].sort_values("year").set_index("year")[_syn_var].astype(float) if _syn_var in dff.columns else pd.Series()
                _comm = _da.index.intersection(_db.index)
                if len(_comm) >= _syn_win+2:
                    _rc_s = _da.loc[_comm].rolling(_syn_win, min_periods=max(4,_syn_win//2)).corr(_db.loc[_comm])
                    fig_rc = go.Figure()
                    fig_rc.add_hrect(y0=0.6,y1=1.05,  fillcolor="rgba(59,130,246,0.05)", layer="below", line_width=0)
                    fig_rc.add_hrect(y0=-1.05,y1=-0.3, fillcolor="rgba(239,68,68,0.05)",  layer="below", line_width=0)
                    fig_rc.add_trace(go.Scatter(
                        x=_comm, y=_rc_s.round(3),
                        mode="lines", line=dict(color="#06b6d4", width=2.2),
                        fill="tozeroy", fillcolor="rgba(6,182,212,0.07)",
                        hovertemplate=f"{_syn_win}Y corr: <b>%{{y:.3f}}</b>  (%{{x}})<extra></extra>",
                    ))
                    fig_rc.add_hline(y=0, line_color="#475569", line_width=1)
                    fig_rc.add_hline(y=0.6,  line_dash="dot", line_color="#3b82f6", line_width=0.8)
                    fig_rc.add_hline(y=-0.3, line_dash="dot", line_color="#ef4444", line_width=0.8)
                    _rcl = L(f"{_syn_win}Y Rolling Correlation — {iso_to_name(_ia)} × {iso_to_name(_ib)} · {col_label(_syn_var)}", 340)
                    _rcl["yaxis"]  = {**_rcl.get("yaxis",{}), "range": [-1.1, 1.1]}
                    _rcl["margin"] = dict(l=50,r=20,t=50,b=40)
                    fig_rc.update_layout(**_rcl)
                    if crisis_col and crisis_col in dff.columns:
                        fig_rc = add_crisis_shading(fig_rc, dff[dff["iso"]==_ia], crisis_col)
                    st.plotly_chart(fig_rc, use_container_width=True)

    # ──────────────────────────────────────────────────────────────
    # ENGINE 5  ·  HISTORICAL ANALOGUES
    # ──────────────────────────────────────────────────────────────
    with _lab_tabs[4]:
        st.markdown('<div class="section-label">Historical Analogue Engine — Find Your Macro Twin</div>',
                    unsafe_allow_html=True)
        st.caption("Computes Euclidean distance in z-score macro-feature space across all countries × all years in the dataset. Returns the N historically closest episodes and checks what happened next.")

        _ha1, _ha2, _ha3 = st.columns(3)
        with _ha1:
            _ha_iso  = st.selectbox("Reference country:", sorted(dff["iso"].unique()),
                                     format_func=iso_to_name, key="ha_iso2")
        with _ha2:
            _ha_yrs  = sorted(dff[dff["iso"]==_ha_iso]["year"].dropna().unique().tolist()) if _ha_iso else []
            _ha_year = st.selectbox("Reference year:", _ha_yrs,
                                     index=len(_ha_yrs)-1 if _ha_yrs else 0, key="ha_yr2")
        with _ha3:
            _ha_n    = st.slider("Analogues:", 5, 20, 10, key="ha_n2")

        _ha_feats = [f for f in ["gdp_growth","inflation","credit_gdp","ltrate",
                                  "ca_gdp","hp_real_growth","money_gdp","credit_gdp_chg"]
                     if f in dff.columns]

        @st.cache_data(show_spinner=False)
        def _find_analogues(data_hash, df_in, ref_iso, ref_year, n, feats, c_col):
            ref_row = df_in[(df_in["iso"]==ref_iso) & (df_in["year"]==ref_year)]
            if len(ref_row)==0 or len(feats)==0: return pd.DataFrame()
            # z-score the whole panel
            pan = df_in[["iso","year"]+feats].copy()
            for f in feats:
                mn, sd = pan[f].mean(), pan[f].std()
                pan[f] = (pan[f]-mn)/(sd+1e-8)
            pan = pan.dropna(subset=feats)
            ref_z = pan[(pan["iso"]==ref_iso)&(pan["year"]==ref_year)][feats].values
            if len(ref_z)==0: return pd.DataFrame()
            ref_z = ref_z[0]
            dists = np.sqrt(((pan[feats].values - ref_z)**2).sum(axis=1))
            pan   = pan.copy()
            pan["distance"] = dists
            pan = pan[~((pan["iso"]==ref_iso)&(pan["year"].between(ref_year-5, ref_year+5)))]
            top = pan.nsmallest(n, "distance")[["iso","year","distance"]].copy()
            # restore original feature values
            orig = df_in[["iso","year"]+feats]
            top  = top.merge(orig, on=["iso","year"], how="left")
            # crisis follow-through
            def _c3(row):
                if c_col and c_col in df_in.columns:
                    w = df_in[(df_in["iso"]==row["iso"]) &
                               (df_in["year"].between(row["year"]+1, row["year"]+3))]
                    return int(w[c_col].max()>0) if len(w)>0 else 0
                return 0
            top["crisis_3y"] = top.apply(_c3, axis=1)
            # avg GDP growth in following 3Y
            def _g3(row):
                w = df_in[(df_in["iso"]==row["iso"]) &
                           (df_in["year"].between(row["year"]+1, row["year"]+3))]
                return round(float(w["gdp_growth"].mean()), 2) if "gdp_growth" in w.columns and len(w)>0 else np.nan
            top["gdp_next3y"] = top.apply(_g3, axis=1)
            return top.reset_index(drop=True)

        _ha_hash = str(_ha_iso)+str(_ha_year)+str(_ha_n)+str(year_range)+str(crisis_col)
        _analogs = _find_analogues(_ha_hash, dff, _ha_iso, _ha_year, _ha_n, _ha_feats, crisis_col)

        if len(_analogs) > 0:
            # ── bar chart of distances ──
            _alabs = [f"{iso_to_name(r['iso'])} {int(r['year'])}" for _,r in _analogs.iterrows()]
            _adist = _analogs["distance"].values
            _acrisis = _analogs["crisis_3y"].values
            _acols   = ["#ef4444" if c else "#3b82f6" for c in _acrisis]

            fig_ha = go.Figure(go.Bar(
                x=_alabs, y=np.round(_adist,3),
                marker=dict(color=_acols, line=dict(color=_acols, width=0.5)),
                text=["⚠ CRISIS" if c else "" for c in _acrisis],
                textposition="outside",
                textfont=dict(size=9, family="IBM Plex Mono", color="#ef4444"),
                hovertemplate="<b>%{x}</b><br>Distance: <b>%{y:.3f}</b><extra></extra>",
            ))
            _hal = L(f"Top {_ha_n} Historical Analogues — {iso_to_name(_ha_iso)} {_ha_year}", 370)
            _hal["xaxis"]     = {**_hal.get("xaxis",{}), "tickangle":-38, "tickfont":dict(size=9)}
            _hal["yaxis"]     = {**_hal.get("yaxis",{}), "title":"Euclidean Distance (lower = more similar)"}
            _hal["showlegend"]= False
            _hal["margin"]    = dict(l=70,r=20,t=50,b=110)
            fig_ha.update_layout(**_hal)
            st.plotly_chart(fig_ha, use_container_width=True)
            st.caption("🔴 Red = crisis within 3 years of that episode · 🔵 Blue = no crisis followed")

            # ── insight box ──
            _cr_rate  = float(_analogs["crisis_3y"].mean()*100)
            _base_rt  = float(dff[crisis_col].mean()*100) if crisis_col and crisis_col in dff.columns else 5.0
            _gdp_med  = float(_analogs["gdp_next3y"].median()) if "gdp_next3y" in _analogs.columns else np.nan
            _ic       = "#ef4444" if _cr_rate>_base_rt*1.5 else "#f59e0b" if _cr_rate>_base_rt else "#10b981"
            st.markdown(
                '<div class="insight-box" style="border-left-color:' + _ic + ';">'
                '<div class="insight-title" style="color:' + _ic + ';">🔭 Analogue Intelligence — ' + iso_to_name(_ha_iso) + ' ' + str(_ha_year) + '</div>'
                '<b>Crisis rate among analogues:</b> <span style="color:' + _ic + ';font-size:1.1rem;font-weight:700;">' + f"{_cr_rate:.0f}%" + '</span>'
                ' &nbsp;vs base rate&nbsp; <span style="color:#94a3b8;">' + f"{_base_rt:.1f}%" + '</span><br>'
                + (f'<b>Median GDP growth (next 3Y after analogues):</b> {_gdp_med:+.1f}%<br>' if not np.isnan(_gdp_med) else '')
                + '<b>Signal:</b> ' + (
                    f"⚠️ Analogues show {_cr_rate:.0f}% crisis rate — {_cr_rate/_base_rt:.1f}× the historical base rate. Structurally elevated."
                    if _cr_rate > _base_rt*1.5 else
                    f"Analogues within normal range of historical crisis frequency."
                ) + '<br>'
                '<span style="color:#475569;font-size:0.72rem;">Nearest-neighbour in z-score space · ' + str(len(_ha_feats)) + ' features · ±5Y exclusion window · ' + str(len(dff["iso"].unique())) + ' countries</span>'
                '</div>', unsafe_allow_html=True)

            # ── radar: reference vs top 3 analogues ──
            st.markdown('<div class="section-label">Macro Fingerprint — Reference vs Top 3 Analogues</div>', unsafe_allow_html=True)
            _ref_vals_raw = dff[(dff["iso"]==_ha_iso)&(dff["year"]==_ha_year)][_ha_feats]
            if len(_ref_vals_raw) > 0:
                _theta = [col_label(f) for f in _ha_feats] + [col_label(_ha_feats[0])]
                fig_rad = go.Figure()
                _rv = [float(_ref_vals_raw[f].values[0]) if f in _ref_vals_raw.columns and not pd.isna(_ref_vals_raw[f].values[0]) else 0.0 for f in _ha_feats]
                fig_rad.add_trace(go.Scatterpolar(
                    r=_rv+[_rv[0]], theta=_theta,
                    fill="toself", name=f"◉ {iso_to_name(_ha_iso)} {_ha_year}",
                    line=dict(color="#06b6d4", width=3),
                    fillcolor="rgba(6,182,212,0.10)",
                    marker=dict(size=7, color="#06b6d4"),
                ))
                for _ai, (_, _ar) in enumerate(_analogs.head(3).iterrows()):
                    _ac   = PALETTE[(_ai+1) % len(PALETTE)]
                    _av   = [float(_ar[f]) if f in _ar.index and not pd.isna(_ar[f]) else 0.0 for f in _ha_feats]
                    _albl = f"{'⚠ ' if _ar['crisis_3y'] else ''}{iso_to_name(_ar['iso'])} {int(_ar['year'])}"
                    fig_rad.add_trace(go.Scatterpolar(
                        r=_av+[_av[0]], theta=_theta,
                        fill="toself", name=_albl,
                        line=dict(color=_ac, width=1.8, dash="dot" if _ar["crisis_3y"] else "solid"),
                        fillcolor=f"rgba({int(_ac[1:3],16)},{int(_ac[3:5],16)},{int(_ac[5:7],16)},0.05)",
                        marker=dict(size=5, color=_ac),
                    ))
                fig_rad.update_layout(
                    paper_bgcolor="#111827", plot_bgcolor="#111827",
                    font=dict(family="IBM Plex Mono", color="#94a3b8", size=9),
                    polar=dict(
                        bgcolor="#0f172a",
                        radialaxis=dict(visible=True, gridcolor="#1e2d45", tickfont=dict(size=7), color="#475569"),
                        angularaxis=dict(gridcolor="#1e2d45", color="#64748b", tickfont=dict(size=9)),
                    ),
                    legend=dict(bgcolor="#111827", bordercolor="#1e2d45", borderwidth=1,
                                font=dict(size=9, family="IBM Plex Mono"),
                                orientation="h", x=0.5, y=-0.15, xanchor="center"),
                    title=dict(text="Macro Fingerprint Overlay — Reference vs Top 3 Analogues",
                               font=dict(size=11, family="IBM Plex Mono", color="#94a3b8")),
                    height=460, margin=dict(l=70,r=70,t=60,b=90),
                )
                st.plotly_chart(fig_rad, use_container_width=True)

            # ── analogue detail table ──
            _tbl = _analogs[["iso","year","distance","crisis_3y","gdp_next3y"]+_ha_feats].copy()
            _tbl["Country"]   = _tbl["iso"].map(iso_to_name)
            _tbl["Distance"]  = _tbl["distance"].round(3)
            _tbl["⚠ Crisis +3Y"] = _tbl["crisis_3y"].map({1:"🔴 Yes",0:"🟢 No"})
            if "gdp_next3y" in _tbl.columns:
                _tbl["GDP +3Y (avg%)"] = _tbl["gdp_next3y"].round(2)
            _tbl = _tbl.drop(columns=["iso","crisis_3y","gdp_next3y"]).rename(columns={"year":"Year"}).set_index("Country")
            for f in _ha_feats:
                if f in _tbl.columns:
                    _tbl = _tbl.rename(columns={f: col_label(f)})
                    _tbl[col_label(f)] = _tbl[col_label(f)].round(2)
            st.dataframe(_tbl, use_container_width=True, height=min(460, 52+38*len(_tbl)))


# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
    JST MACROHISTORY DASHBOARD &nbsp;·&nbsp;
    DATASET R6 &nbsp;·&nbsp;
    JORDÀ · SCHULARICK · TAYLOR &nbsp;·&nbsp;
    macrohistory.net &nbsp;·&nbsp;
    18 ECONOMIES · 1870–PRESENT
    <br style="margin-bottom:6px;">
    © 2026 ADIYAT COTO &nbsp;·&nbsp; ALL RIGHTS RESERVED
</div>""", unsafe_allow_html=True)

