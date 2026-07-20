import streamlit as st

from styles.base import BASE_CSS
from styles.cards import CARD_CSS
from styles.tables import TABLE_CSS
from styles.charts import CHART_CSS


def inject_css() -> None:
    st.markdown(
        f"""
        <style>

        {BASE_CSS}

        {CARD_CSS}

        {TABLE_CSS}

        {CHART_CSS}

        </style>
        """,
        unsafe_allow_html=True,
    )