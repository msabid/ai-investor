import streamlit as st
from security.auth import authenticate, register_user

def auth_screen():
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37,99,235,.22), transparent 34rem),
            radial-gradient(circle at bottom right, rgba(16,185,129,.14), transparent 30rem),
            #05070b;
        color: #f8fafc;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2.5rem; max-width: 1180px; }
    .auth-hero {
        background: rgba(15,23,42,.88);
        border: 1px solid rgba(148,163,184,.24);
        border-radius: 28px;
        padding: 2.4rem;
        box-shadow: 0 28px 90px rgba(0,0,0,.36);
        min-height: 560px;
    }
    .auth-form {
        background: rgba(15,23,42,.92);
        border: 1px solid rgba(148,163,184,.24);
        border-radius: 28px;
        padding: 2.2rem;
        box-shadow: 0 28px 90px rgba(0,0,0,.36);
        min-height: 560px;
    }
    .hero-title {
        font-size: 3.15rem;
        line-height: 1.02;
        font-weight: 850;
        letter-spacing: -0.055em;
        margin-bottom: 1rem;
    }
    .hero-copy {
        color: #cbd5e1;
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    .pill-row { display:flex; gap:.7rem; flex-wrap:wrap; margin:1.4rem 0 2rem 0; }
    .pill {
        padding:.55rem .82rem;
        border-radius:999px;
        background:rgba(30,41,59,.9);
        border:1px solid rgba(148,163,184,.22);
        color:#dbeafe;
        font-size:.88rem;
    }
    .mini-grid { display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:.9rem; margin-top:2rem; }
    .mini-card {
        background:rgba(2,6,23,.72);
        border:1px solid rgba(148,163,184,.16);
        border-radius:18px;
        padding:1rem;
    }
    .mini-card b { display:block; font-size:1.35rem; color:white; }
    .mini-card span { color:#94a3b8; font-size:.85rem; }
    .form-title { font-size:1.7rem; font-weight:800; margin-bottom:.3rem; }
    .form-subtitle { color:#94a3b8; margin-bottom:1.2rem; }
    div[data-testid="stTextInput"] label { color:#cbd5e1; font-weight:650; }
    div[data-testid="stTextInput"] input {
        background:#0f172a;
        color:#f8fafc;
        border:1px solid rgba(148,163,184,.30);
        border-radius:12px;
    }
    div[data-testid="stButton"] button {
        width:100%;
        min-height:2.85rem;
        border-radius:12px;
        background:#2563eb;
        color:white;
        border:0;
        font-weight:750;
    }
    div[data-testid="stButton"] button:hover { background:#1d4ed8; color:white; border:0; }
    .footer-note { text-align:center; color:#64748b; font-size:.85rem; margin-top:1rem; }
    @media(max-width:900px) {
        .hero-title { font-size:2.3rem; }
        .auth-hero, .auth-form { min-height:auto; }
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.08, .92], gap="large")

    with left:
        st.markdown("""
        <div class="auth-hero">
            <div class="hero-title">AI Portfolio<br>Command Center</div>
            <div class="hero-copy">
                A private investing command center for portfolio monitoring, AI-assisted opportunity scanning,
                risk controls, paper execution, and future broker integration.
            </div>
            <div class="pill-row">
                <div class="pill">Risk-first</div>
                <div class="pill">Paper execution now</div>
                <div class="pill">Live trading locked</div>
                <div class="pill">Audit logged</div>
            </div>
            <div class="mini-grid">
                <div class="mini-card"><b>0</b><span>live trades allowed now</span></div>
                <div class="mini-card"><b>100%</b><span>approval gate retained</span></div>
                <div class="mini-card"><b>1%</b><span>default max risk/trade</span></div>
                <div class="mini-card"><b>Paper</b><span>current execution mode</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Secure access</div><div class="form-subtitle">Sign in or create your private account.</div>', unsafe_allow_html=True)
        sign_in, register = st.tabs(["Sign in", "Register"])

        with sign_in:
            email = st.text_input("Email", key="login_email", placeholder="admin@example.com")
            password = st.text_input("Password", key="login_password", type="password", placeholder="Your password")
            if st.button("Sign in", key="login_button"):
                user = authenticate(email, password)
                if user:
                    st.session_state.auth = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            with st.expander("Default local login"):
                st.code("admin@example.com\nChangeMeNow123!")

        with register:
            reg_email = st.text_input("Email", key="register_email", placeholder="you@example.com")
            reg_password = st.text_input("Password", key="register_password", type="password", placeholder="Minimum 10 chars, uppercase, number, symbol")
            reg_confirm = st.text_input("Confirm password", key="register_confirm", type="password")
            if st.button("Create account", key="register_button"):
                ok, msg = register_user(reg_email, reg_password, reg_confirm)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="footer-note">Before online deployment, change the default password and store secrets only as environment variables.</div>', unsafe_allow_html=True)
