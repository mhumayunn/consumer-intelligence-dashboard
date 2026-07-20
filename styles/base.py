BASE_CSS = """

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

/* =========================
   STREAMLIT CONTAINERS
========================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 22px;
    padding: 10px;
}

/* =========================
   BUTTONS / INPUTS
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

"""