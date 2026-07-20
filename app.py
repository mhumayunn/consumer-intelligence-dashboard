from styles.css import inject_css
from pages.executive_overview import render_executive_overview
from pages.tamasha_deep_dive import render_tamasha_deep_dive

inject_css()

tab1, tab2 = st.tabs(
    [
        "Executive Overview",
        "Tamasha Deep Dive"
    ]
)

with tab1:
    render_executive_overview(bundle)

with tab2:
    render_tamasha_deep_dive(bundle)