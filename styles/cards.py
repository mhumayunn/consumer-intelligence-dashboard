CARD_CSS = """

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
    font-size: 3rem;
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
    background: linear-gradient(
        90deg,
        #28282A,
        #ADABAE,
        #EDE2CC
    );
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
   PRIORITY CALLS
========================= */

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

"""