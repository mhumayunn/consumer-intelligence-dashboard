
import os
import math
from datetime import datetime
from typing import Dict, Optional, Tuple

import gspread
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.oauth2.service_account import Credentials
from PIL import Image
import streamlit.components.v1 as components
import calendar
from pathlib import Path


# =========================================================
# CONFIG
# =========================================================
SPREADSHEET_NAME = "PlayStore Sentiment-Automated"

LOCAL_CREDS_FILE = (
    Path(__file__).resolve().parent
    / "sentiment-automation-caadd9710134.json"
)

APP_DISPLAY = {
    "tamasha": "Tamasha",
    "tapmad": "Tapmad",
    "myco": "Myco",
}

RISK_BUCKETS = {
    "Live Sports Streaming & Latency": "Reliability Risk",
    "Peak-Event Server Reliability": "Reliability Risk",
    "Payments & Auto-Renew/Charges": "Trust / Revenue Risk",
    "Login/OTP & Access": "Access Risk",
    "Content Availability & Rights": "Content Risk",
    "Casting/TV & Device Compatibility": "Device Experience Risk",
    "Ads & Interruptions": "Monetization Friction",
    "Overall Experience": "Generic Sentiment",
}

PRIMARY_COLORS = {
    "tamasha": "#28282A",
    "tapmad": "#4B4951",
    "myco": "#ADABAE",
}

SENTIMENT_COLORS = {
    "Positive": "#6F7F6A",
    "Neutral": "#ADABAE",
    "Negative": "#8A3A3A",
}

PRIORITY_COLORS = {
    "P1": "#28282A",
    "P2": "#4B4951",
    "P3": "#ADABAE",
}


# =========================================================
# PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="Play Store Product Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_css() -> None:
    st.markdown(
        """
        <style>

        /* =========================
           GLOBAL PALETTE
        ========================= */

        :root {
            --charcoal: #28282A;
            --charcoal-soft: #4B4951;
            --mid-grey: #ADABAE;
            --light-grey: #C5C3C6;
            --surface-grey: #D4D4D4;
            --cream: #EDE2CC;
            --white-soft: #F6F3EE;
            --text-main: #28282A;
            --text-muted: #4B4951;
            --border-soft: rgba(40, 40, 42, 0.14);
            --shadow-soft: rgba(40, 40, 42, 0.10);
        }

        /* =========================
           APP BACKGROUND
        ========================= */

        .stApp {
            background: linear-gradient(180deg, #EDE2CC 0%, #D4D4D4 100%);
            color: var(--text-main);
        }

        .main .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1450px;
        }

        /* =========================
           CARDS
        ========================= */

        .hero-card,
        .glass-card,
        .insight-card,
        .kpi-card,
        .data-card {
            background: rgba(246, 243, 238, 0.92);
            border: 1px solid var(--border-soft);
            border-radius: 18px;
            box-shadow: 0 10px 28px var(--shadow-soft);
        }

        .hero-card {
            padding: 26px 30px;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #28282A 0%, #4B4951 100%);
            border: 1px solid rgba(237, 226, 204, 0.20);
        }

        .glass-card {
            padding: 18px 20px;
            min-height: 160px;
            transition: all 0.22s ease;
        }

        .glass-card:hover,
        .insight-card:hover,
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow:
                0 14px 40px rgba(0,0,0,0.12),
                inset 0 1px 0 rgba(255,255,255,0.4);
        }

        .insight-card {
            padding: 18px 20px;
            min-height: 165px;
            transition: all 0.22s ease;
        }

        .kpi-card {
            padding: 18px;
            min-height: 165px;

            position: relative;
            overflow: hidden;

            background: rgba(255,255,255,0.22);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);

            border: 1px solid rgba(255,255,255,0.28);

            box-shadow:
                0 8px 30px rgba(0,0,0,0.08),
                inset 0 1px 0 rgba(255,255,255,0.35);

            border-radius: 20px;

            transition: all 0.25s ease;
        }

        .kpi-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 15%;
            width: 70%;
            height: 1px;

            background: linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.8),
                transparent
            );
        }

        .kpi-card.small {
            min-height: 190px;
            height: 190px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .kpi-card.small .kpi-value {
            font-size: 3.0rem; 
            line-height: 1.05;
            font-weight: 800;
            word-break: break-word;
        }

        .kpi-card.small .kpi-sub {
            font-size: 0.82rem;
        }

        /* =========================
           TYPOGRAPHY
        ========================= */

        .eyebrow {
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-size: 0.76rem;
            color: rgba(237, 226, 204, 0.78);
            margin-bottom: 8px;
            font-weight: 700;
        }

        .hero-title {
            font-size: 2.1rem;
            line-height: 1.1;
            font-weight: 850;
            margin-bottom: 8px;
            color: #F6F3EE;
        }

        .hero-subtitle {
            font-size: 1rem;
            color: rgba(246, 243, 238, 0.82);
            margin-bottom: 0;
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 850;
            color: var(--charcoal);
            margin-bottom: 6px;
        }

        .section-title::after {
            content: "";
            display: block;
            width: 180px;
            height: 3px;
            margin-top: 7px;
            border-radius: 999px;
            background: linear-gradient(90deg, #28282A, #ADABAE, #EDE2CC);
        }

        .section-subtitle {
            color: var(--charcoal-soft);
            font-size: 0.94rem;
            margin-bottom: 14px;
        }

        .kpi-label {
            color: var(--charcoal-soft);
            font-size: 0.84rem;
            margin-bottom: 10px;
            font-weight: 700;
            min-height: 22px;
        }

        .kpi-value {
            font-size: 3rem;
            font-weight: 950;
            color: var(--charcoal);
            line-height: 1.05;
            margin-bottom: 8px;
            word-break: break-word;
        }

        .kpi-value-small {
            font-size: 1.25rem;
            font-weight: 800;
            color: var(--charcoal);
            line-height: 1.2;
            margin-bottom: 6px;
            word-break: break-word;
        }

        .insight-title {
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            color: var(--charcoal-soft);
            margin-bottom: 6px;
            text-transform: uppercase;
            font-weight: 800;
        }

        .insight-body {
            font-size: 0.95rem;
            font-weight: 650;
            color: var(--charcoal);
            line-height: 1.45;
            margin-bottom: 6px;
        }

        .insight-sub {
            font-size: 0.82rem;
            color: var(--charcoal-soft);
        }

        /* =========================
           KPI DELTAS
        ========================= */

        .kpi-delta-up {
            color: #3F6F55;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .kpi-delta-down {
            color: #8A3A3A;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .kpi-delta-flat {
            color: var(--charcoal-soft);
            font-weight: 800;
            font-size: 0.9rem;
        }

        /* =========================
           PILLS
        ========================= */

        .pill {
            display: inline-block;
            background: rgba(237, 226, 204, 0.70);
            border: 1px solid rgba(40, 40, 42, 0.16);
            border-radius: 999px;
            padding: 6px 12px;
            margin-right: 8px;
            font-size: 0.8rem;
            color: var(--charcoal);
            font-weight: 700;
        }

        /* =========================
           SIDEBAR
        ========================= */

        div[data-testid="stSidebar"] {
            background: #F6F3EE;
            border-right: 1px solid rgba(40, 40, 42, 0.12);
        }

        div[data-testid="stSidebar"] * {
            color: var(--charcoal) !important;
        }

        /* =========================
           TABS
        ========================= */

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(40, 40, 42, 0.08);
            padding: 6px;
            border-radius: 14px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 10px 16px;
            color: var(--charcoal-soft);
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background: var(--charcoal) !important;
            color: #F6F3EE !important;
            box-shadow: 0 4px 14px rgba(40, 40, 42, 0.20);
        }

        .stTabs [aria-selected="true"] p {
            color: #F6F3EE !important;
        }

        .dual-chart-card {
            background: rgba(255, 255, 255, 0.24);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.30);
            border-radius: 22px;
            padding: 22px;
            box-shadow:
                0 12px 36px rgba(40, 40, 42, 0.10),
                inset 0 1px 0 rgba(255, 255, 255, 0.38);
        }

        .inner-chart-panel {
            background: rgba(246, 243, 238, 0.44);
            border: 1px solid rgba(40, 40, 42, 0.09);
            border-radius: 18px;
            padding: 16px 18px 10px 18px;
            min-height: 390px;
        }

        .inner-chart-title {
            font-size: 1.15rem;
            font-weight: 850;
            color: #28282A;
            margin-bottom: 8px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.22);
            border-radius: 22px;
            padding: 10px;
        }

        /* =========================
           TABLES
        ========================= */

        .data-card {
            padding: 12px 12px 6px 12px;
            margin-top: 6px;
        }

        .dataframe thead tr th {
            background: #4B4951 !important;
            color: #F6F3EE !important;
            font-weight: 800 !important;
            border-bottom: 1px solid rgba(40, 40, 42, 0.20) !important;
        }

        .dataframe tbody tr {
            background-color: #F6F3EE;
        }

        .dataframe tbody tr:nth-child(even) {
            background-color: #EDE2CC;
        }

        .dataframe tbody tr:hover {
            background-color: #D4D4D4 !important;
        }

        table {
            color: var(--charcoal) !important;
        }

        thead tr th {
            color: #F6F3EE !important;
        }

        tbody tr td {
            color: var(--charcoal) !important;
        }

        [data-testid="stDataFrame"] {
            color: var(--charcoal) !important;
        }

        [data-testid="stDataFrame"] td {
            color: var(--charcoal) !important;
        }

        [data-testid="stDataFrame"] th {
            color: #F6F3EE !important;
        }

        .snapshot-table tbody td {
            padding: 14px 16px;
            border-bottom: 1px solid rgba(40, 40, 42, 0.12);
            color: var(--charcoal);
            font-weight: 550;
        }

        .snapshot-table td.app-name {
            font-weight: 800;
            color: var(--charcoal);
        }

        .snapshot-table thead th {
            background: #4B4951;
            color: #F6F3EE;
        }

        /* =========================
        ACTION BOARD DATAFRAME THEME
        ========================= */

        .action-board-wrapper [data-testid="stDataFrame"] {
            background: #F6F3EE !important;
            color: #28282A !important;
            border-radius: 14px !important;
            overflow: hidden !important;
        }

        .action-board-wrapper [data-testid="stDataFrame"] div {
            color: #28282A !important;
        }

        .action-board-wrapper [data-testid="stDataFrame"] [role="columnheader"] {
            background: #4B4951 !important;
            color: #F6F3EE !important;
            font-weight: 800 !important;
        }

        .action-board-wrapper [data-testid="stDataFrame"] [role="gridcell"] {
            background: #F6F3EE !important;
            color: #28282A !important;
        }

        .action-board-wrapper [data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
            background: #EDE2CC !important;
        }

        /* =========================
           PLOTLY CHART TEXT FIXES
        ========================= */

        .js-plotly-plot .plotly .xtick text,
        .js-plotly-plot .plotly .ytick text,
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly .legendtext,
        .js-plotly-plot .plotly .infolayer text {
            fill: #28282A !important;
            color: #28282A !important;
        }

        .js-plotly-plot .plotly .gridlayer path {
            stroke: rgba(40, 40, 42, 0.12) !important;
        }

        /*===========================
            PRIORITY CALLS
        ============================= */

        .priority-card {
            min-height: 150px;
            padding: 18px 20px;
            border-radius: 20px;
            background: rgba(255,255,255,0.22);
            border: 1px solid rgba(255,255,255,0.28);
            box-shadow: 0 8px 30px rgba(40,40,42,0.08);
            display: flex;
            gap: 14px;
            align-items: flex-start;
        }

        .priority-index {
            min-width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #28282A;
            color: #F6F3EE;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 850;
        }

        .priority-title {
            font-size: 0.98rem;
            font-weight: 850;
            color: #28282A;
            margin-bottom: 8px;
            line-height: 1.25;
        }

        .priority-sub {
            font-size: 0.86rem;
            color: #4B4951;
            line-height: 1.42;
        }

        /* =========================
           STREAMLIT BUTTONS / INPUTS
        ========================= */

        .stButton > button {
            background: #28282A;
            color: #F6F3EE;
            border: 1px solid #28282A;
            border-radius: 10px;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: #4B4951;
            border: 1px solid #4B4951;
            color: #F6F3EE;
        }

        div[data-baseweb="select"] > div {
            background-color: #F6F3EE;
            border-color: rgba(40, 40, 42, 0.18);
            color: #28282A;
        }

        input {
            color: #28282A !important;
        }

        /* =========================
           MISC
        ========================= */

        .section-spacer {
            height: 28px;
        }

        hr {
            border-color: rgba(40, 40, 42, 0.12);
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# =========================================================
# DATA ACCESS
# =========================================================
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Local development: use the ignored JSON credentials file
    if LOCAL_CREDS_FILE.exists():
        creds = Credentials.from_service_account_file(
            str(LOCAL_CREDS_FILE),
            scopes=scopes,
        )

    # Streamlit Cloud: use credentials stored in Streamlit Secrets
    else:
        try:
            service_account_info = dict(
                st.secrets["gcp_service_account"]
            )
        except Exception as error:
            raise RuntimeError(
                "Google credentials were not found. "
                "For local use, place "
                "'sentiment-automation-caadd9710134.json' "
                "in the same folder as Dashboard.py. "
                "For Streamlit Cloud, add the credentials "
                "under [gcp_service_account] in Streamlit Secrets."
            ) from error

        creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes,
        )

    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def get_sheet(spreadsheet_name: str):
    client = get_gspread_client()
    return client.open(spreadsheet_name)


@st.cache_data(ttl=300, show_spinner=False)
def read_worksheet(
    spreadsheet_name: str,
    worksheet_name: str,
) -> pd.DataFrame:
    sh = get_sheet(spreadsheet_name)
    ws = sh.worksheet(worksheet_name)
    records = ws.get_all_records()
    return pd.DataFrame(records)


@st.cache_data(ttl=300, show_spinner=False)
def list_worksheets(spreadsheet_name: str):
    sh = get_sheet(spreadsheet_name)
    return [ws.title for ws in sh.worksheets()]


@st.cache_data(ttl=300, show_spinner=False)
def get_latest_month(spreadsheet_name: str) -> str:
    meta = read_worksheet(spreadsheet_name, "meta")

    if meta.empty:
        raise ValueError("Meta sheet is empty.")

    latest = meta.loc[
        meta["key"] == "latest_month",
        "value",
    ]

    if latest.empty:
        raise ValueError(
            "latest_month not found in meta sheet."
        )

    return str(latest.iloc[0])


@st.cache_data(ttl=300, show_spinner=False)
def available_month_keys(spreadsheet_name: str):
    titles = list_worksheets(spreadsheet_name)
    months = set()

    for title in titles:
        if title.startswith("summary_"):
            months.add(
                title.replace("summary_", "")
            )

    return sorted(months, reverse=True)


# =========================================================
# HELPERS
# =========================================================
def normalize_app_name(x: str) -> str:
    if x is None:
        return ""
    key = str(x).strip().lower()
    return APP_DISPLAY.get(key, str(x).title())


def to_numeric_safe(df: pd.DataFrame, cols):
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def parse_month_label(month_key: str) -> str:
    yyyy, mm = month_key.split("_")
    dt = datetime(int(yyyy), int(mm), 1)
    return dt.strftime("%B %Y")


def previous_month_key(month_key: str, all_months: list[str]) -> Optional[str]:
    try:
        idx = all_months.index(month_key)
        return all_months[idx + 1] if idx + 1 < len(all_months) else None
    except ValueError:
        return None


def load_month_bundle(month_key: str) -> Dict[str, pd.DataFrame]:
    bundle = {
        "summary": read_worksheet(SPREADSHEET_NAME, f"summary_{month_key}"),
        "weekly": read_worksheet(SPREADSHEET_NAME, f"weekly_{month_key}"),
        "daily": read_worksheet(SPREADSHEET_NAME, f"daily_ratings_{month_key}"),
        "tamasha_aspects": read_worksheet(SPREADSHEET_NAME, f"tamasha_aspects_{month_key}"),
        "tamasha_tagged": read_worksheet(SPREADSHEET_NAME, f"tamasha_tagged_reviews_{month_key}"),
        "tamasha_insights": read_worksheet(SPREADSHEET_NAME, f"tamasha_insights_{month_key}"),
    }
    return bundle


def preprocess_bundle(bundle: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    out = bundle.copy()

    out["summary"] = to_numeric_safe(
        out["summary"],
        [
            "total_reviews", "avg_rating", "positive_pct", "negative_pct", "neutral_pct",
            "five_star", "four_star", "three_star", "two_star", "one_star"
        ],
    )
    if "app" in out["summary"].columns:
        out["summary"]["app_display"] = out["summary"]["app"].apply(normalize_app_name)

    out["weekly"] = to_numeric_safe(out["weekly"], ["reviews", "avg_sentiment"])
    if "app" in out["weekly"].columns:
        out["weekly"]["app_display"] = out["weekly"]["app"].apply(normalize_app_name)

    out["daily"] = to_numeric_safe(out["daily"], ["avg_rating", "n_reviews"])
    if "date" in out["daily"].columns:
        out["daily"]["date"] = pd.to_datetime(out["daily"]["date"], errors="coerce")
    if "source" in out["daily"].columns:
        out["daily"]["source_display"] = out["daily"]["source"].apply(normalize_app_name)

    out["tamasha_aspects"] = to_numeric_safe(
        out["tamasha_aspects"],
        ["mentions", "Positive", "Neutral", "Negative", "Unknown", "pos_%", "neu_%", "neg_%"],
    )
    if "Aspect" in out["tamasha_aspects"].columns:
        out["tamasha_aspects"]["risk_bucket"] = out["tamasha_aspects"]["Aspect"].map(RISK_BUCKETS).fillna("Other")

    out["tamasha_tagged"] = to_numeric_safe(out["tamasha_tagged"], ["rating"])
    if "date" in out["tamasha_tagged"].columns:
        out["tamasha_tagged"]["date"] = pd.to_datetime(out["tamasha_tagged"]["date"], errors="coerce")

    out["tamasha_insights"] = to_numeric_safe(
        out["tamasha_insights"],
        ["monthly_avg_rating", "total_reviews", "aspect_coverage_pct"],
    )

    return out


def build_delta(current: Optional[float], previous: Optional[float], suffix: str = "") -> Tuple[str, str]:
    if current is None or pd.isna(current) or previous is None or pd.isna(previous):
        return "—", "flat"
    delta = current - previous
    if abs(delta) < 1e-9:
        return f"0.00{suffix}", "flat"
    sign = "+" if delta > 0 else ""
    return f"{sign}{delta:.2f}{suffix}", "up" if delta > 0 else "down"


def delta_class(direction: str) -> str:
    return {
        "up": "kpi-delta-up",
        "down": "kpi-delta-down",
        "flat": "kpi-delta-flat",
    }.get(direction, "kpi-delta-flat")


def card(title: str, value: str, delta: str = "", direction: str = "flat", accent: str = "default", size: str = "normal") -> None:
    accent_map = {
    "default": "#28282A",
    "positive": "#6F7F6A",
    "negative": "#8A3A3A",
    "warning": "#9A7A3F",
    "brand": "#28282A",
}

    value_color = accent_map.get(accent, "#F7FAFF")
    value_class = "kpi-value-small" if size == "small" else "kpi-value"

    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>{title}</div>
            <div class='{value_class}' style='color:{value_color};'>{value}</div>
            <div class='{delta_class(direction)}'>{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(title: str, body: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class='insight-card'>
            <div class='insight-title'>{title}</div>
            <div class='insight-body'>{body}</div>
            <div class='insight-sub'>{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def rank_apps(summary_df: pd.DataFrame, metric: str, ascending: bool = False) -> pd.DataFrame:
    temp = summary_df[["app", "app_display", metric]].copy()
    temp = temp.sort_values(metric, ascending=ascending).reset_index(drop=True)
    temp["rank"] = np.arange(1, len(temp) + 1)
    return temp


def compute_category_metrics(summary_df: pd.DataFrame) -> pd.DataFrame:
    df = summary_df.copy()
    total_reviews = df["total_reviews"].sum()
    total_pos = (df["total_reviews"] * df["positive_pct"] / 100).sum()
    total_neg = (df["total_reviews"] * df["negative_pct"] / 100).sum()

    df["review_share_pct"] = np.where(total_reviews > 0, df["total_reviews"] / total_reviews * 100, np.nan)
    df["pos_review_count"] = df["total_reviews"] * df["positive_pct"] / 100
    df["neg_review_count"] = df["total_reviews"] * df["negative_pct"] / 100
    df["positive_share_of_category_pct"] = np.where(total_pos > 0, df["pos_review_count"] / total_pos * 100, np.nan)
    df["negative_share_of_category_pct"] = np.where(total_neg > 0, df["neg_review_count"] / total_neg * 100, np.nan)
    return df


def build_risk_scores(aspects_df: pd.DataFrame) -> pd.DataFrame:
    if aspects_df.empty:
        return pd.DataFrame(columns=["risk_bucket", "mentions", "Negative", "neg_rate", "weighted_risk"])

    df = aspects_df.copy()
    df["neg_rate"] = np.where(df["mentions"] > 0, df["Negative"] / df["mentions"] * 100, 0)
    grouped = (
        df.groupby("risk_bucket", as_index=False)
          .agg({"mentions": "sum", "Negative": "sum"})
    )
    grouped["neg_rate"] = np.where(grouped["mentions"] > 0, grouped["Negative"] / grouped["mentions"] * 100, 0)
    grouped["weighted_risk"] = grouped["mentions"] * grouped["neg_rate"]
    grouped = grouped.sort_values(["weighted_risk", "Negative"], ascending=False)
    return grouped


def compute_priority_matrix(aspects_df: pd.DataFrame) -> pd.DataFrame:
    if aspects_df.empty:
        return aspects_df
    df = aspects_df.copy()
    df["negative_rate"] = np.where(df["mentions"] > 0, df["Negative"] / df["mentions"] * 100, 0)
    df["priority_score"] = (df["mentions"] * 0.55) + (df["negative_rate"] * 0.45)
    df["priority_bucket"] = np.select(
        [
            (df["mentions"] >= df["mentions"].median()) & (df["negative_rate"] >= df["negative_rate"].median()),
            (df["negative_rate"] >= df["negative_rate"].quantile(0.7)),
            (df["mentions"] >= df["mentions"].quantile(0.7)),
        ],
        ["P1", "P2", "P2"],
        default="P3",
    )
    return df.sort_values(["priority_score", "Negative"], ascending=False)


def build_action_board(priority_df: pd.DataFrame) -> pd.DataFrame:
    if priority_df.empty:
        return pd.DataFrame()

    owner_map = {
        "Live Sports Streaming & Latency": "Streaming / Platform Engineering",
        "Peak-Event Server Reliability": "Infra / Backend",
        "Payments & Auto-Renew/Charges": "Payments / Growth / CX",
        "Login/OTP & Access": "Identity / CRM / App Engineering",
        "Content Availability & Rights": "Content / Partnerships / Product",
        "Casting/TV & Device Compatibility": "TV / Device Experience Team",
        "Ads & Interruptions": "Ads / Monetization / Product",
        "Overall Experience": "Cross-functional",
    }

    impact_map = {
        "Live Sports Streaming & Latency": "Core value proposition risk during live events",
        "Peak-Event Server Reliability": "Retention and event-time failure risk",
        "Payments & Auto-Renew/Charges": "Trust, churn, and revenue dispute risk",
        "Login/OTP & Access": "Acquisition and re-entry friction",
        "Content Availability & Rights": "Expectation mismatch and perceived catalog weakness",
        "Casting/TV & Device Compatibility": "Lean-back viewing friction",
        "Ads & Interruptions": "Monetization friction and session disruption",
        "Overall Experience": "Broad perception signal; lower action specificity",
    }

    rec_map = {
        "Live Sports Streaming & Latency": "Prioritize playback stabilization during peak traffic; audit buffering hotspots.",
        "Peak-Event Server Reliability": "Stress-test match-time backend capacity and monitor failure spikes.",
        "Payments & Auto-Renew/Charges": "Audit billing transparency, auto-renew messaging, and refund handling.",
        "Login/OTP & Access": "Reduce OTP friction and investigate sign-in failure loops.",
        "Content Availability & Rights": "Clarify catalog availability and rights messaging inside the app.",
        "Casting/TV & Device Compatibility": "Improve device compatibility QA and casting stability.",
        "Ads & Interruptions": "Rebalance ad load around high-intent viewing moments.",
        "Overall Experience": "Break generic sentiment into sharper UX and product sub-themes.",
    }

    board = priority_df[["Aspect", "mentions", "Negative", "negative_rate", "priority_bucket", "risk_bucket"]].copy()
    board["business_impact"] = board["Aspect"].map(impact_map)
    board["suggested_action"] = board["Aspect"].map(rec_map)
    board["owner"] = board["Aspect"].map(owner_map)
    board.rename(
        columns={
            "Aspect": "issue",
            "mentions": "mentions",
            "Negative": "negative_mentions",
            "negative_rate": "negative_rate_pct",
            "priority_bucket": "priority",
            "risk_bucket": "risk_type",
        },
        inplace=True,
    )
    return board


def fig_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(246,243,238,0.65)",
        font=dict(color="#28282A", family="Inter, Segoe UI, Arial"),
        margin=dict(l=18, r=18, t=50, b=18),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color="#28282A")
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color="#28282A",
        tickfont=dict(color="#28282A"),
        title_font=dict(color="#28282A"),
    )
    fig.update_yaxes(
        gridcolor="rgba(40,40,42,0.12)",
        zeroline=False,
        color="#28282A",
        tickfont=dict(color="#28282A"),
        title_font=dict(color="#28282A"),
    )
    return fig


def render_plotly(fig, key=None, apply_global_style=True):
    if apply_global_style:
        fig = fig_style(fig)
    st.plotly_chart(fig, use_container_width=True, key=key)


def render_snapshot_table(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("No competitor snapshot data available.")
        return

    rows_html = ""
    for _, row in df.iterrows():
        rows_html += (
            "<tr>"
            f"<td class='app-name'>{row['App']}</td>"
            f"<td class='num'>{row['Reviews']}</td>"
            f"<td class='num'>{row['Avg Rating']}</td>"
            f"<td class='num'>{row['Positive %']}</td>"
            f"<td class='num'>{row['Negative %']}</td>"
            f"<td class='num'>{row['Review Share %']}</td>"
            "</tr>"
        )

    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: Inter, Segoe UI, Arial, sans-serif;
        }}

        .snapshot-table-card {{
            background: #F6F3EE;
            border: 1px solid rgba(40, 40, 42, 0.14);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 28px rgba(40, 40, 42, 0.10);
        }}

        .snapshot-table {{
            width: 100%;
            border-collapse: collapse;
            color: #28282A;
            font-size: 15px;
        }}

        .snapshot-table thead th {{
            background: #4B4951;
            color: #F6F3EE;
            font-weight: 800;
            text-align: left;
            padding: 14px 16px;
            border-bottom: 1px solid rgba(40, 40, 42, 0.20);
        }}

        .snapshot-table tbody td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(40, 40, 42, 0.12);
            color: #28282A;
            font-weight: 550;
        }}

        .snapshot-table tbody tr:nth-child(odd) {{
            background: #F6F3EE;
        }}

        .snapshot-table tbody tr:nth-child(even) {{
            background: #EDE2CC;
        }}

        .snapshot-table tbody tr:hover {{
            background: #D4D4D4;
        }}

        .snapshot-table td.num {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}

        .snapshot-table td.app-name {{
            font-weight: 800;
            color: #28282A;
        }}
    </style>
    </head>

    <body>
        <div class="snapshot-table-card">
            <table class="snapshot-table">
                <thead>
                    <tr>
                        <th>App</th>
                        <th>Reviews</th>
                        <th>Avg Rating</th>
                        <th>Positive %</th>
                        <th>Negative %</th>
                        <th>Review Share %</th>
                    </tr>
                </thead>

                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    components.html(html, height=260, scrolling=False, width=None)

def build_review_window_distribution(tagged_df: pd.DataFrame, month_key: str) -> pd.DataFrame:
    if tagged_df.empty or "date" not in tagged_df.columns:
        return pd.DataFrame(columns=["period", "reviews"])

    yyyy, mm = month_key.split("_")
    year = int(yyyy)
    month = int(mm)

    df = tagged_df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Use unique reviews if available; otherwise count rows.
    # Since tagged_df is exploded by aspect, one review can appear multiple times.
    # So we deduplicate using review text + name + date.
    dedupe_cols = [col for col in ["name", "review_text", "date"] if col in df.columns]
    if dedupe_cols:
        df = df.drop_duplicates(subset=dedupe_cols)

    last_day = calendar.monthrange(year, month)[1]

    windows = [
        (1, 5),
        (6, 10),
        (11, 15),
        (16, 20),
        (21, 25),
        (26, last_day),
    ]

    rows = []
    for start_day, end_day in windows:
        start_date = pd.Timestamp(year=year, month=month, day=start_day)
        end_date = pd.Timestamp(year=year, month=month, day=end_day)

        count = df[
            (df["date"].dt.date >= start_date.date()) &
            (df["date"].dt.date <= end_date.date())
        ].shape[0]

        rows.append({
            "period": f"{start_day}–{end_day} {start_date.strftime('%b')}",
            "reviews": count,
            "start_day": start_day,
        })

    return pd.DataFrame(rows)

# =========================================================
# LOAD DATA
# =========================================================
try:
    latest_month = get_latest_month(SPREADSHEET_NAME)
    all_months = available_month_keys(SPREADSHEET_NAME)
except Exception as e:
    st.error(f"Could not connect to Google Sheets: {e}")
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## Product Intelligence")
st.sidebar.caption("Interactive sentiment and product risk dashboard")

selected_month = st.sidebar.selectbox(
    "Reporting month",
    options=all_months,
    index=all_months.index(latest_month) if latest_month in all_months else 0,
    format_func=parse_month_label,
)

compare_prev = st.sidebar.toggle("Compare with previous month", value=True)
show_only_actionable = st.sidebar.toggle("Focus on actionable aspects", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<span class='pill'>Latest month: {parse_month_label(latest_month)}</span>",
    unsafe_allow_html=True,
)

prev_month = previous_month_key(selected_month, all_months)

try:
    current_bundle = preprocess_bundle(load_month_bundle(selected_month))
except Exception as e:
    st.error(f"Could not load selected month data: {e}")
    st.stop()

prev_bundle = None
if compare_prev and prev_month:
    try:
        prev_bundle = preprocess_bundle(load_month_bundle(prev_month))
    except Exception:
        prev_bundle = None

summary_df = compute_category_metrics(current_bundle["summary"])
weekly_df = current_bundle["weekly"]
daily_df = current_bundle["daily"]
aspects_df = current_bundle["tamasha_aspects"].copy()
tagged_df = current_bundle["tamasha_tagged"].copy()
insights_df = current_bundle["tamasha_insights"].copy()

if show_only_actionable and not aspects_df.empty:
    aspects_df = aspects_df[aspects_df["Aspect"] != "Overall Experience"].copy()

priority_df = compute_priority_matrix(aspects_df)
risk_scores = build_risk_scores(aspects_df)
action_board = build_action_board(priority_df)

prev_summary_df = prev_bundle["summary"] if prev_bundle else pd.DataFrame()
prev_summary_df = compute_category_metrics(prev_summary_df) if not prev_summary_df.empty else prev_summary_df
prev_aspects_df = prev_bundle["tamasha_aspects"] if prev_bundle else pd.DataFrame()
if prev_bundle:
    prev_aspects_df = prev_bundle["tamasha_aspects"].copy()
    prev_aspects_df = to_numeric_safe(
        prev_aspects_df,
        ["mentions", "Positive", "Neutral", "Negative", "Unknown", "pos_%", "neu_%", "neg_%"]
    )
else:
    prev_aspects_df = pd.DataFrame()


# =========================================================
# DERIVED METRICS
# =========================================================
def get_app_metric(df: pd.DataFrame, app: str, metric: str) -> Optional[float]:
    if df.empty:
        return None
    sub = df[df["app"] == app]
    if sub.empty or metric not in sub.columns:
        return None
    return sub.iloc[0][metric]


tamasha_reviews = get_app_metric(summary_df, "tamasha", "total_reviews")
tamasha_rating = get_app_metric(summary_df, "tamasha", "avg_rating")
tamasha_pos = get_app_metric(summary_df, "tamasha", "positive_pct")
tamasha_neg = get_app_metric(summary_df, "tamasha", "negative_pct")

t_prev_reviews = get_app_metric(prev_summary_df, "tamasha", "total_reviews") if not prev_summary_df.empty else None
t_prev_rating = get_app_metric(prev_summary_df, "tamasha", "avg_rating") if not prev_summary_df.empty else None
t_prev_pos = get_app_metric(prev_summary_df, "tamasha", "positive_pct") if not prev_summary_df.empty else None
t_prev_neg = get_app_metric(prev_summary_df, "tamasha", "negative_pct") if not prev_summary_df.empty else None

best_strength = None
if not aspects_df.empty and "Positive" in aspects_df.columns:
    best_strength = aspects_df.sort_values(["Positive", "mentions"], ascending=False).iloc[0]["Aspect"]

highest_risk = None
if not priority_df.empty:
    highest_risk = priority_df.iloc[0]["Aspect"]

most_discussed = None
if not aspects_df.empty:
    most_discussed = aspects_df.sort_values("mentions", ascending=False).iloc[0]["Aspect"]

most_improved = None
most_deteriorated = None
mom_issue_table = pd.DataFrame()
if prev_bundle is not None and not prev_aspects_df.empty and not current_bundle["tamasha_aspects"].empty:
    curr_base = current_bundle["tamasha_aspects"][["Aspect", "mentions", "Negative"]].copy()
    prev_base = prev_aspects_df[["Aspect", "mentions", "Negative"]].copy()
    mom_issue_table = curr_base.merge(prev_base, on="Aspect", how="outer", suffixes=("_curr", "_prev")).fillna(0)
    mom_issue_table["neg_change"] = mom_issue_table["Negative_curr"] - mom_issue_table["Negative_prev"]
    mom_issue_table["mention_change"] = mom_issue_table["mentions_curr"] - mom_issue_table["mentions_prev"]
    if not mom_issue_table.empty:
        most_deteriorated = mom_issue_table.sort_values(["neg_change", "mention_change"], ascending=False).iloc[0]["Aspect"]
        most_improved = mom_issue_table.sort_values(["neg_change", "mention_change"], ascending=True).iloc[0]["Aspect"]

leader_rating = summary_df["avg_rating"].max() if not summary_df.empty else None
rating_gap_to_leader = (tamasha_rating - leader_rating) if tamasha_rating is not None and leader_rating is not None else None

trust_risk_score = 0.0
if not risk_scores.empty:
    trust_row = risk_scores[risk_scores["risk_bucket"] == "Trust / Revenue Risk"]
    if not trust_row.empty:
        trust_risk_score = float(trust_row.iloc[0]["weighted_risk"])


# =========================================================
# HERO
# =========================================================
logo_col, hero_col = st.columns([0.12, 0.88])

with logo_col:
    try:
        logo = Image.open("Tamashaa_logo.png")
        st.image(logo, width=110)
    except Exception:
        st.markdown("")

with hero_col:
    st.markdown(
        f"""
        <div class='hero-card'>
            <div class='eyebrow'>Play Store Product Intelligence Dashboard</div>
            <div class='hero-title'>Tamasha Sentiment & Consumer Intelligence</div>
            <p class='hero-subtitle'>A decision-grade product dashboard built from Google Play reviews, competitor benchmarking, risk diagnostics, and aspect-level insight tracking for <b>{parse_month_label(selected_month)}</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"<span class='pill'>Reporting month: {parse_month_label(selected_month)}</span>"
    f"<span class='pill'>Default month source: meta.latest_month</span>"
    f"<span class='pill'>Apps tracked: {', '.join(APP_DISPLAY[a] for a in APP_DISPLAY if a in summary_df['app'].tolist())}</span>",
    unsafe_allow_html=True,
)


tab1, tab4 = st.tabs([
    "Executive Overview",
    "Tamasha Deep Dive",
])

# -----------------------------------------------------
# GLOBAL RANK METRICS USED ACROSS TABS
# -----------------------------------------------------
try:
    rating_rank = int(
        rank_apps(summary_df, "avg_rating")
        .query("app == 'tamasha'")["rank"]
        .iloc[0]
    )
except Exception:
    rating_rank = None

try:
    volume_rank = int(
        rank_apps(summary_df, "total_reviews")
        .query("app == 'tamasha'")["rank"]
        .iloc[0]
    )
except Exception:
    volume_rank = None

# =========================================================
# TAB 1 - EXECUTIVE OVERVIEW
# =========================================================
with tab1:
    section_header(
        "Executive Command Center",
        "A high-level operating view of Tamasha’s review volume, sentiment health, competitor position, and in-month activity patterns.",
    )

#     # -----------------------------------------------------
#     # PRODUCT HEALTH SCORE
#     # -----------------------------------------------------
#     health_score = (
#         (tamasha_pos or 0) * 0.45
#         + ((tamasha_rating or 0) / 5 * 100) * 0.35
#         + (100 - (tamasha_neg or 0)) * 0.20
#     )

#     tamasha_review_share = get_app_metric(summary_df, "tamasha", "review_share_pct")

#     st.markdown(
#     f"""
#     <div class="metric-explainer">
#         <b>Product Health Index</b><br>
#         Calculated using:
#         <ul>
#             <li>{tamasha_pos:.1f}% Positive Reviews</li>
#             <li>{tamasha_rating:.2f}/5 Average Rating</li>
#             <li>{tamasha_neg:.1f}% Negative Reviews</li>
#         </ul>
#         Higher scores indicate stronger customer satisfaction and lower complaint pressure.
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# -----------------------------------------------------
# KPI METRICS
# -----------------------------------------------------
    tamasha_review_share = get_app_metric(
        summary_df,
        "tamasha",
        "review_share_pct"
    )


    #  HEALTH SCORE
    health_score = (
    (tamasha_pos or 0) * 0.45
    + ((tamasha_rating or 0) / 5 * 100) * 0.35
    + (100 - (tamasha_neg or 0)) * 0.20
    )
    # -----------------------------------------------------
    # KPI ROW
    # -----------------------------------------------------
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        d, s = build_delta(tamasha_reviews, t_prev_reviews)
        card(
            "Tamasha reviews",
            f"{int(tamasha_reviews):,}" if tamasha_reviews is not None else "—",
            d,
            s,
            "brand",
        )

    with c2:
        d, s = build_delta(tamasha_rating, t_prev_rating)
        card(
            "Avg rating",
            f"{tamasha_rating:.2f}" if tamasha_rating is not None else "—",
            d,
            s,
            "warning",
        )

    with c3:
        d, s = build_delta(tamasha_pos, t_prev_pos, " pp")
        card(
            "Positive share",
            f"{tamasha_pos:.1f}%" if tamasha_pos is not None else "—",
            d,
            s,
            "positive",
        )

    with c4:
        d, s = build_delta(tamasha_neg, t_prev_neg, " pp")
        card(
            "Negative share",
            f"{tamasha_neg:.1f}%" if tamasha_neg is not None else "—",
            d,
            s,
            "negative",
        )

    with c5:
        card(
            "Category share",
            f"{tamasha_review_share:.1f}%" if tamasha_review_share is not None and pd.notna(tamasha_review_share) else "—",
            "Share of tracked reviews",
            "flat",
            "brand",
        )

    with c6:
        card(
            "Health score",
            f"{health_score:.0f}/100",
            "Composite index",
            "flat",
            "positive" if health_score >= 70 else "warning" if health_score >= 45 else "negative",
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

           # -----------------------------------------------------
    # FULL-WIDTH DAILY RATING TRAJECTORY
    # -----------------------------------------------------
    section_header(
        "Daily rating trajectory",
        "Signal of rating stability and quality perception across the month.",
    )

    fig = go.Figure()

    line_colors = {
        "tamasha": "#6F8F68",  # muted green
        "tapmad": "#D9903D",   # muted orange
        "myco": "#3F7FBF",     # muted blue
    }

    for app_name, grp in daily_df.sort_values("date").groupby("source_display"):
        app_key = str(app_name).strip().lower()
        is_tamasha = app_key == "tamasha"

        fig.add_trace(
            go.Scatter(
                x=grp["date"],
                y=grp["avg_rating"],
                mode="lines+markers",
                name=app_name,
                line=dict(
                    width=4 if is_tamasha else 2.4,
                    dash="solid" if is_tamasha else "dot",
                    color=line_colors.get(app_key, "#ADABAE"),
                ),
                marker=dict(
                    size=9 if is_tamasha else 7,
                    color=line_colors.get(app_key, "#ADABAE"),
                    line=dict(
                        width=2,
                        color="#F6F3EE",
                    ),
                ),
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Date: %{x|%d %b}<br>"
                    "Avg rating: %{y:.2f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        height=455,
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(237,226,204,0.00)",
        xaxis_title="Date",
        yaxis_title="Average rating",
        margin=dict(l=24, r=24, t=35, b=36),
        hoverlabel=dict(
            bgcolor="#5F5C58",
            bordercolor="#8A857E",
            font=dict(
                color="#F8F5F0",
                size=13,
                family="Inter, Segoe UI, Arial, sans-serif",
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(
                size=13,
                color="#28282A",
            ),
        ),
        font=dict(
            family="Inter, Segoe UI, Arial, sans-serif",
            color="#28282A",
            size=13,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickformat="%d",
        dtick="D1",
        tickfont=dict(
            size=12,
            color="#4B4951",
            family="Inter, Segoe UI, Arial, sans-serif",
        ),
        title_font=dict(
            size=13,
            color="#28282A",
            family="Inter, Segoe UI, Arial, sans-serif",
        ),
        ticks="",
    )

    fig.update_yaxes(
        range=[1, 5],
        tickmode="array",
        tickvals=[1, 2, 3, 4, 5],
        showgrid=True,
        gridcolor="rgba(255,255,255,0.25)",
        gridwidth=2.5,

        showline=False,
        zeroline=False,

        tickfont=dict(
            size=12,
            color="#4B4951",
            family="Inter, Segoe UI, Arial, sans-serif",
        ),
        title_font=dict(
            size=13,
            color="#28282A",
            family="Inter, Segoe UI, Arial, sans-serif",
        ),
        ticks="",
    )

    render_plotly(fig, key="daily_trend_full_width", apply_global_style=False)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # REVIEW VOLUME DISTRIBUTION + TAMASHA SENTIMENT MIX
    # -----------------------------------------------------
    review_windows = build_review_window_distribution(tagged_df, selected_month)

    review_col, sentiment_col = st.columns([1.45, 0.9])

    # -----------------------------------------------------
    # REVIEW VOLUME
    # -----------------------------------------------------
    with review_col:
        with st.container(border=True):
            section_header("Review volume distribution", "")

            if review_windows.empty:
                st.info("No review distribution data available.")
            else:
                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=review_windows["period"],
                        y=review_windows["reviews"],
                        text=review_windows["reviews"],
                        textposition="outside",
                        marker=dict(
                            color=review_windows["reviews"],
                            colorscale=[
                                [0.0, "#A7A4A0"],
                                [0.5, "#6B6870"],
                                [1.0, "#3F3D43"],
                            ],
                        ),
                        hovertemplate="<b>%{x}</b><br>Reviews: %{y}<extra></extra>",
                    )
                )

                fig.update_layout(
                    height=350,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=10, b=20),
                    showlegend=False,
                )

                render_plotly(
                    fig,
                    key="review_volume_windows",
                    apply_global_style=False
                )

    # -----------------------------------------------------
    # SENTIMENT MIX
    # -----------------------------------------------------
    with sentiment_col:
        with st.container(border=True):
            section_header("Tamasha sentiment mix", "")

            tamasha_row = summary_df[summary_df["app"] == "tamasha"]

            if not tamasha_row.empty:
                row = tamasha_row.iloc[0]

                sentiment_mix = pd.DataFrame(
                    {
                        "Sentiment": ["Positive", "Neutral", "Negative"],
                        "Share": [
                            row.get("positive_pct", 0),
                            row.get("neutral_pct", 0),
                            row.get("negative_pct", 0),
                        ],
                    }
                )

                fig = px.pie(
                    sentiment_mix,
                    names="Sentiment",
                    values="Share",
                    hole=0.65,
                    color="Sentiment",
                    color_discrete_map=SENTIMENT_COLORS,
                )

                fig.update_layout(
                    height=340,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=0, b=0),
                    annotations=[
                        dict(
                            text="Sentiment",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(size=16, color="#28282A")
                        )
                    ],
                )

                render_plotly(
                    fig,
                    key="tamasha_sentiment_mix",
                    apply_global_style=False
                )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # COMPETITOR SNAPSHOT
    # -----------------------------------------------------
    with st.container(border=True):
        section_header("Competitor snapshot", "")

        snapshot_cols = [
            "app_display",
            "total_reviews",
            "avg_rating",
            "positive_pct",
            "negative_pct",
            "review_share_pct",
        ]

        snapshot = summary_df[snapshot_cols].copy().sort_values(
            "avg_rating",
            ascending=False
        )

        snapshot.columns = [
            "App",
            "Reviews",
            "Avg Rating",
            "Positive %",
            "Negative %",
            "Review Share %",
        ]

        snapshot["Reviews"] = snapshot["Reviews"].map(
            lambda x: f"{int(x):,}" if pd.notna(x) else "—"
        )

        snapshot["Avg Rating"] = snapshot["Avg Rating"].map(
            lambda x: f"{x:.2f}" if pd.notna(x) else "—"
        )

        snapshot["Positive %"] = snapshot["Positive %"].map(
            lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
        )

        snapshot["Negative %"] = snapshot["Negative %"].map(
            lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
        )

        snapshot["Review Share %"] = snapshot["Review Share %"].map(
            lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
        )

        render_snapshot_table(snapshot)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)


# =========================================================
# TAB 4 - TAMASHA DEEP DIVE
# =========================================================

actionable_aspects_df = aspects_df[
    aspects_df["Aspect"].astype(str).str.lower() != "overall experience"
].copy()

top_discussed_actionable = (
    actionable_aspects_df.sort_values("mentions", ascending=False).iloc[0]["Aspect"]
    if not actionable_aspects_df.empty
    else "—"
)

top_negative_actionable = (
    actionable_aspects_df.sort_values("Negative", ascending=False).iloc[0]["Aspect"]
    if not actionable_aspects_df.empty
    else "—"
)

with tab4:
    section_header(
        "Tamasha Deep Dive",
        "Granular view of user feedback, recurring complaint themes, and representative review evidence.",
    )

    t1, t2, t3, t4 = st.columns(4)

    with t1:
        card(
            "Total tagged reviews",
            f"{len(tagged_df):,}",
            "Reviews matched to at least one aspect",
            "flat",
            "brand",
            size="small"
        )

    with t2:
        coverage = insights_df.iloc[0]["aspect_coverage_pct"] if not insights_df.empty else np.nan
        card(
            "Aspect coverage",
            f"{coverage:.1f}%" if pd.notna(coverage) else "—",
            "Share of reviews with detected themes",
            "flat",
            "warning",
            size="small"
        )

    with t3:
        card(
            "Top discussed aspect",
            top_discussed_actionable,
            "Most mentioned non-generic theme",
            "flat",
            "positive",
            size="small"
        )

    with t4:
        card(
            "Top negative aspect",
            top_negative_actionable,
            "Most negative non-generic theme",
            "flat",
            "negative",
            size="small"
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        # -----------------------------------------------------
    # TAMASHA RISK & ACTION INTELLIGENCE
    # -----------------------------------------------------
    section_header(
        "Tamasha risk & action intelligence",
        "Complaint drivers, month-over-month issue movement, and product ownership view.",
    )

    risk_left, risk_right = st.columns([1, 1])

    with risk_left:
        with st.container(border=True):
            section_header("Top complaint drivers", "")

            if priority_df.empty:
                st.info("No complaint data available.")
            else:
                topn = priority_df[
                    priority_df["Aspect"].astype(str).str.lower() != "overall experience"
                ].sort_values("Negative", ascending=False).head(8)

                fig = px.bar(
                    topn,
                    x="Negative",
                    y="Aspect",
                    orientation="h",
                    color="negative_rate",
                    color_continuous_scale=[
                        [0.0, "#F3D6D2"],
                        [0.45, "#C96F65"],
                        [1.0, "#8A3A3A"],
                    ],
                )

                fig.update_layout(
                    yaxis=dict(categoryorder="total ascending"),
                    xaxis_title="Negative mentions",
                    yaxis_title="",
                    height=390,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        family="Inter, Segoe UI, Arial, sans-serif",
                        size=14,
                        color="#4B4951",
                    ),
                    coloraxis_colorbar=dict(
                        title=dict(
                            text="Negative rate",
                            font=dict(size=13, color="#4B4951"),
                        ),
                        tickfont=dict(size=12, color="#4B4951"),
                    ),
                    margin=dict(l=20, r=20, t=20, b=30),
                )

                fig.update_xaxes(
                    showgrid=True,
                    gridcolor="rgba(75,73,81,0.10)",
                    zeroline=False,
                    showline=False,
                    tickfont=dict(size=13, color="#4B4951"),
                    title_font=dict(size=14, color="#4B4951"),
                )

                fig.update_yaxes(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    tickfont=dict(size=13, color="#4B4951"),
                )

                fig.update_traces(
                    marker_line_width=0,
                    hovertemplate="<b>%{y}</b><br>Negative mentions: %{x}<br>Negative rate: %{marker.color:.1f}%<extra></extra>",
                )

                render_plotly(fig, key="top_neg_drivers_deepdive", apply_global_style=False)

        with risk_right:
            with st.container(border=True):
                section_header(
                    "Month-over-month issue movement",
                    "Compares Tamasha complaint themes in tagged reviews against the previous month. Positive values mean the issue worsened; negative values mean it improved.",
                )

                if mom_issue_table.empty:
                    st.info("No month-over-month issue movement available.")
                else:
                    movement = mom_issue_table[
                        mom_issue_table["Aspect"].astype(str).str.lower() != "overall experience"
                    ].copy().sort_values("neg_change", ascending=False)

                    fig = px.bar(
                        movement,
                        x="Aspect",
                        y="neg_change",
                        color="neg_change",
                        color_continuous_scale=[
                            [0.0, "#6F8F68"],   # muted green = improved
                            [0.50, "#D8CFAE"],  # muted cream/yellow = little change
                            [1.0, "#8A3A3A"],   # muted red = worsened
                        ],
                    )

                    fig.update_layout(
                        height=390,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis_title="",
                        yaxis_title="Change in negative mentions",
                        font=dict(
                            family="Inter, Segoe UI, Arial, sans-serif",
                            size=13,
                            color="#4B4951",
                        ),
                        margin=dict(l=20, r=20, t=20, b=95),
                        coloraxis_colorbar=dict(
                            title=dict(
                                text="Change",
                                font=dict(size=13, color="#4B4951"),
                            ),
                            tickfont=dict(size=12, color="#4B4951"),
                        ),
                        hoverlabel=dict(
                            bgcolor="#5F5C58",
                            bordercolor="#8A857E",
                            font=dict(color="#F8F5F0", size=13),
                        ),
                    )

                    fig.update_xaxes(
                        showgrid=False,
                        zeroline=False,
                        showline=False,
                        tickangle=-35,
                        tickfont=dict(size=12, color="#4B4951"),
                    )

                    fig.update_yaxes(
                        showgrid=True,
                        gridcolor="rgba(80,73,81,0.18)",
                        gridwidth=2.2,
                        zeroline=True,
                        zerolinecolor="rgba(75,73,81,0.42)",
                        zerolinewidth=1.8,
                        showline=False,
                        tickfont=dict(size=12, color="#4B4951"),
                        title_font=dict(size=13, color="#4B4951"),
                    )

                    fig.update_traces(
                        marker_line_width=0,
                        hovertemplate="<b>%{x}</b><br>Change in negative mentions: %{y}<extra></extra>",
                    )

                    render_plotly(
                        fig,
                        key="mom_issues_deepdive",
                        apply_global_style=False,
                    )
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        section_header("Product action board", "")

        if action_board.empty:
            st.info("No action board data available.")
        else:
            board_view = action_board[
                [
                    "issue",
                    "priority",
                    "mentions",
                    "negative_mentions",
                    "negative_rate_pct",
                    "risk_type",
                    "owner",
                    "business_impact",
                ]
            ].copy()

            board_view.columns = [
                "Issue",
                "Priority",
                "Mentions",
                "Negative Mentions",
                "Negative Rate %",
                "Risk Type",
                "Owner",
                "Business Impact",
            ]

            board_view = board_view[
                board_view["Issue"].astype(str).str.lower() != "overall experience"
            ]

            st.markdown("<div class='action-board-wrapper'>", unsafe_allow_html=True)

            st.dataframe(
                board_view,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    section_header(
        "Tamasha intelligence summary",
        "High-level interpretation of Tamasha’s current position, product risk, and dominant user theme.",
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        insight_box(
            "Competitive position",
            f"Tamasha is ranked #{rating_rank or '—'} on rating and #{volume_rank or '—'} on review volume within the tracked set.",
        )

    with s2:
        insight_box(
            "Biggest product risk",
            f"{highest_risk or 'No issue detected'} is currently the strongest issue signal, based on complaint volume and negative intensity.",
            "This is the best candidate for executive escalation and weekly monitoring.",
        )

    with s3:
        insight_box(
            "Most discussed theme",
            f"{most_discussed or 'No aspect detected'} is attracting the most user attention this month.",
            "High discussion does not always mean highest risk — but it often shapes brand perception.",
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    section_header(
        "Priority calls",
        "What product owners should care about first.",
    )

    priority_data = [
        (
            "Stabilize the dominant complaint cluster",
            f"{highest_risk or 'Top issue'} is the clearest short-term risk to user experience and should be prioritized first."
        ),
        (
            "Protect Tamasha’s strongest differentiator",
            f"{best_strength or 'Core experience'} remains a competitive advantage, but adjacent friction needs tightening."
        ),
        (
            "Monitor trust-sensitive signals",
            f"Trust risk score currently stands at {trust_risk_score:.1f}, making billing and confidence-related issues worth close review."
        ),
    ]

    p1, p2, p3 = st.columns(3)

    for col, (title, desc), idx in zip([p1, p2, p3], priority_data, range(1, 4)):
        with col:
            st.markdown(
                f"""
                <div class='priority-card'>
                    <div class='priority-index'>{idx}</div>
                    <div class='priority-content'>
                        <div class='priority-title'>{title}</div>
                        <div class='priority-sub'>{desc}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)    

    # -----------------------------------------------------
    # REVIEW EXPLORER
    # -----------------------------------------------------
    with st.container(border=True):
        section_header(
            "Review explorer",
            "Filter representative Tamasha reviews by sentiment and aspect."
        )

        aspect_options = sorted([
            a for a in tagged_df.get("aspects", pd.Series(dtype=str))
            .dropna()
            .astype(str)
            .unique()
            .tolist()
            if a.lower() != "overall experience"
        ])

        selected_aspects = st.multiselect(
            "Aspect filter",
            options=aspect_options,
            default=aspect_options[:3] if aspect_options else []
        )

        review_df = tagged_df.copy()

        if selected_aspects:
            review_df = review_df[review_df["aspects"].isin(selected_aspects)]

        review_df = review_df.sort_values(
            ["sentiment", "rating"],
            ascending=[True, True]
        )

        review_df["date"] = pd.to_datetime(
            review_df["date"],
            errors="coerce"
        ).dt.strftime("%d %b %Y")

        review_show = review_df[
            ["date", "name", "rating", "sentiment", "aspects", "review_text"]
        ].copy()

        review_show.columns = [
            "Date",
            "User",
            "Rating",
            "Sentiment",
            "Aspect",
            "Review"
        ]

        st.dataframe(
            review_show.head(200),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # SIGNAL INDEX CARDS
    # -----------------------------------------------------
    rx1, rx2, rx3 = st.columns(3)

    with rx1:
        streaming_neg = 0
        if not current_bundle["tamasha_aspects"].empty:
            row = current_bundle["tamasha_aspects"][
                current_bundle["tamasha_aspects"]["Aspect"] == "Live Sports Streaming & Latency"
            ]
            streaming_neg = float(row.iloc[0]["Negative"]) if not row.empty else 0

        insight_box(
            "Streaming pain index",
            f"{(streaming_neg / len(tagged_df) * 100):.1f}% of tagged Tamasha review-aspect records relate to negative streaming complaints."
            if len(tagged_df) else "No data available.",
            "Useful as a single headline metric for event-time reliability tracking.",
        )

    with rx2:
        payment_neg = 0
        if not current_bundle["tamasha_aspects"].empty:
            row = current_bundle["tamasha_aspects"][
                current_bundle["tamasha_aspects"]["Aspect"] == "Payments & Auto-Renew/Charges"
            ]
            payment_neg = float(row.iloc[0]["Negative"]) if not row.empty else 0

        insight_box(
            "Payment trust index",
            f"{(payment_neg / len(tagged_df) * 100):.1f}% of tagged Tamasha review-aspect records are negative payment-related mentions."
            if len(tagged_df) else "No data available.",
            "A compact trust metric for subscriptions, billing, and deductions.",
        )

    with rx3:
        generic_row = (
            current_bundle["tamasha_aspects"][
                current_bundle["tamasha_aspects"]["Aspect"] == "Overall Experience"
            ]
            if not current_bundle["tamasha_aspects"].empty
            else pd.DataFrame()
        )

        generic_mentions = float(generic_row.iloc[0]["mentions"]) if not generic_row.empty else 0
        total_mentions = (
            float(current_bundle["tamasha_aspects"]["mentions"].sum())
            if not current_bundle["tamasha_aspects"].empty
            else 0
        )

        insight_box(
            "Actionable signal share",
            f"{((total_mentions - generic_mentions) / total_mentions * 100):.1f}% of aspect-tagged mentions are feature or issue specific."
            if total_mentions else "No data available.",
            "This helps separate generic praise/complaints from operationally actionable product feedback.",
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)


# -----------------------------------------------------
# RECOMMENDED ACTIONS & OWNER MAPPING
# -----------------------------------------------------

    with st.container(border=True):
        section_header(
            "Recommended actions & owner mapping",
            "A sharper execution layer for product, engineering, CX, and monetization teams.",
        )

        if action_board.empty:
            st.info("No action recommendations available.")
        else:
            action_view = action_board.copy()

            action_view["negative_rate_pct"] = pd.to_numeric(
                action_view["negative_rate_pct"],
                errors="coerce"
            ).round(1)

            action_view = action_view[
                action_view["issue"].astype(str).str.lower() != "overall experience"
            ]

            action_view = action_view[
                [
                    "issue",
                    "priority",
                    "mentions",
                    "negative_mentions",
                    "negative_rate_pct",
                    "risk_type",
                    "owner",
                    "business_impact",
                    "suggested_action",
                ]
            ].copy()

            action_view.columns = [
                "Issue",
                "Priority",
                "Mentions",
                "Negative Mentions",
                "Negative Rate %",
                "Risk Type",
                "Owner",
                "Business Impact",
                "Suggested Action",
            ]

            st.dataframe(
                action_view,
                use_container_width=True,
                hide_index=True
            )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

 # =================================
# EXECUTIVE NARRATIVE
# =================================

    narrative_left, narrative_right = st.columns([1.1, 0.9])

    top_issue_text = highest_risk or "the leading issue cluster"
    top_strength_text = best_strength or "a strong product-use case"
    top_discussed_text = most_discussed or "the most discussed user theme"
    top_deteriorated_text = most_deteriorated or "month-over-month deterioration is not available"

    tamasha_reviews_text = (
        f"{int(tamasha_reviews):,}"
        if tamasha_reviews is not None and not pd.isna(tamasha_reviews)
        else "N/A"
    )

    tamasha_rating_text = (
        f"{tamasha_rating:.2f}"
        if tamasha_rating is not None and not pd.isna(tamasha_rating)
        else "N/A"
    )

    with narrative_left:
        with st.container(border=True):
            section_header(
                "Executive narrative for stakeholders",
                "A ready-to-present insight summary for product owners and leadership reviews.",
            )

            narrative_paragraphs = [
                f"Tamasha remains one of the most visible apps in the tracked competitor set, with <b>{tamasha_reviews_text}</b> monthly reviews and an average rating of <b>{tamasha_rating_text}</b>. This month, the app’s strongest positive association is <b>{top_strength_text}</b>, reinforcing where users already see clear value.",
                f"The primary experience risk is <b>{top_issue_text}</b>, which is currently the strongest complaint driver when complaint frequency and negative intensity are assessed together. This is the clearest candidate for short-term product and engineering prioritization.",
                f"At a category level, <b>{top_discussed_text}</b> is shaping perception most strongly, while <b>{top_deteriorated_text}</b> appears to be worsening fastest versus the prior month. That makes it a useful watchpoint for next month’s operating review.",
            ]

            st.markdown(
                "<div class='insight-body'>"
                + "<br><br>".join(narrative_paragraphs)
                + "</div>",
                unsafe_allow_html=True,
            )

    with narrative_right:
        with st.container(border=True):
            section_header(
                "Leadership watchlist",
                "Three focused calls that make the dashboard immediately actionable.",
            )

            watchlist = [
                f"<b>P1:</b> Address <b>{top_issue_text}</b> before the next peak traffic cycle.",
                f"<b>P2:</b> Protect Tamasha’s advantage in <b>{top_strength_text}</b> while tightening adjacent experience quality.",
                f"<b>P3:</b> Review the month-over-month movement of <b>{top_deteriorated_text}</b> to confirm whether the issue is structural or event-led.",
            ]

            st.markdown(
                "<div class='insight-body'>"
                + "<br><br>".join(watchlist)
                + "</div>",
                unsafe_allow_html=True,
            )

    st.caption("Built for executive product reviews, competitor monitoring, and monthly sentiment diagnostics.")