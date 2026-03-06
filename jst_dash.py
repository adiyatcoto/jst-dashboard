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
def compute_dalio_scores(data):
    """
    Compute normalized 0-100 scores for each Dalio cycle component.
    Higher = more advanced / stressed in that dimension.
    """
    d = data.copy().sort_values("year")

    scores = pd.DataFrame(index=d.index)
    scores["year"] = d["year"]
    scores["iso"]  = d["iso"]

    def norm(series, invert=False):
        s = series.copy().astype(float)
        mn, mx = s.min(), s.max()
        if mx == mn: return s * 0 + 50
        out = (s - mn) / (mx - mn) * 100
        return 100 - out if invert else out

    # 1. DEBT BURDEN — credit/gdp, higher = more burdened
    if "credit_gdp" in d.columns:
        scores["debt_burden"] = norm(d["credit_gdp"])
    else:
        scores["debt_burden"] = 50

    # 2. MONEY PRINTING — money/gdp growth, higher = more printing
    if "money_gdp" in d.columns:
        scores["money_printing"] = norm(d["money_gdp"].pct_change().rolling(5).mean() * 100)
    else:
        scores["money_printing"] = 50

    # 3. DEBT SERVICE PRESSURE — ltrate × credit_gdp proxy
    if "ltrate" in d.columns and "credit_gdp" in d.columns:
        scores["debt_service"] = norm(d["ltrate"] * d["credit_gdp"] / 100)
    elif "ltrate" in d.columns:
        scores["debt_service"] = norm(d["ltrate"])
    else:
        scores["debt_service"] = 50

    # 4. PRODUCTIVITY / GROWTH — real gdp per capita growth, higher = more productive
    if "rgdppc" in d.columns:
        scores["productivity"] = norm(d["rgdppc"].pct_change().rolling(10).mean() * 100)
    elif "gdp_growth" in d.columns:
        scores["productivity"] = norm(d["gdp_growth"].rolling(10).mean())
    else:
        scores["productivity"] = 50

    # 5. INTERNAL ORDER — cumulative crisis rate up to each year
    # Using expanding (cumulative) mean so each year reflects full historical record to that point.
    # This gives differentiated scores: a country with many crises over its history
    # will score lower than one that rarely had crises — even in peaceful recent years.
    if "crisisJST" in d.columns:
        # expanding mean = crisis years so far / total years so far
        cumulative_crisis_rate = d["crisisJST"].expanding(min_periods=5).mean()
        scores["internal_order"] = norm(cumulative_crisis_rate, invert=True)
    else:
        scores["internal_order"] = 50

    # 6. EXTERNAL COMPETITIVENESS — current account/gdp, positive = strong
    if "ca_gdp" in d.columns:
        scores["external_strength"] = norm(d["ca_gdp"])
    else:
        scores["external_strength"] = 50

    # 7. ASSET PRICE CYCLE — real house price growth momentum
    if "hp_real_growth" in d.columns:
        scores["asset_cycle"] = norm(d["hp_real_growth"].rolling(5).mean())
    elif "hpnom" in d.columns:
        scores["asset_cycle"] = norm(d["hpnom"].pct_change().rolling(5).mean() * 100)
    else:
        scores["asset_cycle"] = 50

    # 8. INFLATION PRESSURE — rolling avg inflation vs 2% target deviation
    if "inflation" in d.columns:
        scores["inflation_pressure"] = norm(abs(d["inflation"].rolling(5).mean() - 2))
    else:
        scores["inflation_pressure"] = 50

    # COMPOSITE EMPIRE HEALTH SCORE
    # High productivity + internal order + external strength + low debt burden = healthy empire
    health_cols = ["productivity", "internal_order", "external_strength"]
    stress_cols = ["debt_burden", "debt_service", "inflation_pressure"]
    scores["empire_health"] = (
        scores[health_cols].mean(axis=1) * 0.6 +
        (100 - scores[stress_cols].mean(axis=1)) * 0.4
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
            _latest = dff.groupby("iso")[_col].last().dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*(_n-6) + ["🟡","🟠","🔴"]
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
            _latest = dff.groupby("iso")[_col].last().dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*(_n-6) + ["🟡","🟠","🔴"]
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
                    mode="markers", name=f"{iso_to_name(iso)} ({label})",
                    marker=dict(color=PALETTE[i%len(PALETTE)], symbol=sym, size=5, opacity=0.7),
                    customdata=d_s["year"],
                    hovertemplate=f"<b>{iso_to_name(iso)}</b> %{{customdata}}<br>ΔCredit/GDP: %{{x:.2f}}pp<br>Real HP Growth: %{{y:.2f}}%<extra></extra>"
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
        fig_s.update_layout(**L("Credit Expansion vs Real House Price Growth", 420, fig=fig_s))
        st.plotly_chart(fig_s, use_container_width=True)



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
            _latest = dff.groupby("iso")[_col].last().dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*(_n-6) + ["🟡","🟠","🔴"]
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
            _latest = dff.groupby("iso")[_col].last().dropna().sort_values(ascending=_asc).reset_index()
            _latest.columns = ["Country", "Value"]
            _latest["Country"] = _latest["Country"].map(iso_to_name)
            _n = len(_latest)
            _colors = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
            _medals = ["🥇","🥈","🥉"] + ["⬜"]*(_n-6) + ["🟡","🟠","🔴"]
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
        _medals_c = ["🔴","🟠","🟡"] + ["⬜"]*(_n-6) + ["🥉","🥈","🥇"]

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
                             text=plot_data["iso"].map(iso_to_name), color="iso", color_discrete_sequence=PALETTE,
                             title=f"Cross-Country: {x_var} vs {y_var} ({yr_select})",
                             size_max=50)
        else:
            fig = px.scatter(plot_data, x=x_var, y=y_var,
                             text=plot_data["iso"].map(iso_to_name), color="iso", color_discrete_sequence=PALETTE,
                             title=f"Cross-Country: {x_var} vs {y_var} ({yr_select})")

        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(**L(height=500, extra={"showlegend": False}, fig=fig))
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
    fig_rank.update_layout(**L(height=max(300, 28*len(latest_cs)+80)),
                           showlegend=False, coloraxis_showscale=False)



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
            d["roll_corr"] = d["credit_gdp"].rolling(10).corr(d["gdp_growth"])
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
            x_line = np.linspace(biv[xv].min(), biv[xv].max(), 100)
            y_line = slope * x_line + intercept

            fig_biv = go.Figure()
            for i, iso in enumerate(selected_countries):
                d_biv = biv[biv["iso"]==iso]
                fig_biv.add_trace(go.Scatter(x=d_biv[xv], y=d_biv[yv],
                    mode="markers", name=iso_to_name(iso),
                    marker=dict(color=PALETTE[i%len(PALETTE)], size=5, opacity=0.7),
                    customdata=d_biv["year"],
                    hovertemplate=f"<b>{iso_to_name(iso)}</b> %{{customdata}}<br>{xv}: %{{x:.2f}}<br>{yv}: %{{y:.2f}}<extra></extra>"))
            fig_biv.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
                name=f"OLS (r={r:.2f}, p={p:.3f})",
                line=dict(color="#f59e0b", width=2, dash="dash")))
            fig_biv.update_layout(**L(f"{xv} vs {yv} — OLS: β={slope:.3f}, R²={r**2:.3f}", 420, fig=fig_biv))
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
            fig_quad = go.Figure()
            for i, iso in enumerate(selected_countries):
                d_q = scatter_dg[scatter_dg["iso"]==iso]
                fig_quad.add_trace(go.Scatter(
                    x=d_q["gdp_growth"], y=d_q["inflation"],
                    mode="markers", name=iso_to_name(iso),
                    marker=dict(color=PALETTE[i%len(PALETTE)], size=4, opacity=0.6),
                    customdata=d_q["year"],
                    hovertemplate=f"<b>{iso_to_name(iso)}</b> %{{customdata}}<br>GDP: %{{x:.1f}}%<br>CPI: %{{y:.1f}}%<extra></extra>"
                ))
            # Quadrant lines
            fig_quad.add_vline(x=0, line_dash="dot", line_color="#475569")
            fig_quad.add_hline(y=2, line_dash="dot", line_color="#475569")
            # Quadrant labels
            for txt, x, y in [
                    ("GOLDILOCKS (high growth, low inflation)", 4, 0.5),
                    ("INFLATIONARY BOOM (high growth, high inflation)", 4, 6),
                    ("DEFLATIONARY BUST (low growth, low inflation)", -3, 0.5),
                    ("STAGFLATION (low growth, high inflation)", -3, 6)]:
                fig_quad.add_annotation(x=x, y=y, text=txt, showarrow=False,
                    font=dict(size=7, color="#475569", family="IBM Plex Mono"),
                    align="center")
            _ql = L("Dalio's Four Quadrants: Growth vs Inflation", 340)
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
    _all_scores = []
    for _iso in df["iso"].unique():
        _d = df[df["iso"]==_iso].copy()
        _sc = compute_dalio_scores(_d).sort_values("year")
        if len(_sc) == 0: continue
        _row = {"Country": iso_to_name(_iso)}
        for _c in ["empire_health","debt_burden","productivity","internal_order","external_strength","asset_cycle","inflation_pressure"]:
            # Use last non-null value for this score column — handles Japan NaN, Ireland sparse data
            _series = _sc[_c].dropna() if _c in _sc.columns else pd.Series(dtype=float)
            if len(_series) == 0:
                _row[_c] = 50.0  # neutral fallback
            else:
                _row[_c] = round(float(_series.iloc[-1]), 1)
        # Skip countries where empire_health is still NaN after best-effort
        if pd.isna(_row.get("empire_health", float("nan"))):
            continue
        _all_scores.append(_row)

    if _all_scores:
        _score_df = pd.DataFrame(_all_scores)
        rank_tabs_dc = st.tabs(["🌍 Empire Health", "📈 Productivity", "⚖️ Debt Burden", "🏛 Internal Order", "🌐 External Strength"])
        _dc_metrics = [
            ("empire_health",     "Overall Empire Health Score",  "Composite score — higher = rising empire. Combines productivity, order, external strength vs debt and stress.", False),
            ("productivity",      "Productivity Score",           "Higher = stronger long-run economic dynamism. The engine of empire rise.", False),
            ("debt_burden",       "Debt Burden Score",            "Higher = MORE indebted. In this ranking, LOW score = healthier (less burdened). Red = most burdened.", True),
            ("internal_order",    "Internal Order Score",         "Higher = fewer financial crises historically = more stable domestic conditions.", False),
            ("external_strength", "External Strength Score",      "Higher = country is a net lender to the world. Persistent surplus = financial power.", False),
        ]
        _inverted = {"debt_burden"}  # lower is better for these
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
                    _medals_d = ["🔴","🟠","🟡"] + ["⬜"]*(_n-6) + ["🥉","🥈","🥇"]
                else:
                    _colors_d = ["#10b981" if i < 3 else ("#ef4444" if i >= _n-3 else "#3b82f6") for i in range(_n)]
                    _medals_d = ["🥇","🥈","🥉"] + ["⬜"]*(_n-6) + ["🟡","🟠","🔴"]
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
