def apply_theme(st, theme):
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {background-color:#05070b;color:#f5f7fa}
        [data-testid="stHeader"] {background: rgba(5,7,11,.72); backdrop-filter: blur(10px);}
        section[data-testid="stSidebar"]{background-color:#0b1020;border-right:1px solid rgba(148,163,184,.16)}
        .block-container {padding-top:2rem; max-width: 1280px;}
        .stMetric{background-color:#111827;padding:14px;border-radius:14px;border:1px solid rgba(148,163,184,.16)}
        div[data-testid="stDataFrame"] {border-radius:14px; overflow:hidden;}
        div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label {font-weight:700;color:#cbd5e1;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .block-container {padding-top:2rem; max-width: 1280px;}
        .stMetric{background-color:#f8fafc;padding:14px;border-radius:14px;border:1px solid #e2e8f0}
        section[data-testid="stSidebar"]{background-color:#f8fafc}
        </style>
        """, unsafe_allow_html=True)
