TABLE_CSS = """

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

"""