import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import init_db, run_query
from security.auth import ensure_default_admin, authenticate, change_password
from dashboard.auth_ui import auth_screen
from dashboard.styles import apply_theme
from dashboard.qa_checklist import QA_ITEMS
from data_sources.market_data import MarketDataClient
from agents.risk_agent import RiskAgent
from agents.opportunity_agent import OpportunityAgent
from agents.ai_decision_agent import AIDecisionAgent
from trading.execution_controller import ExecutionController

st.set_page_config(page_title="AI Portfolio Command Center", layout="wide")
init_db()
ensure_default_admin()

if "auth" not in st.session_state:
    st.session_state.auth = False
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if not st.session_state.auth:
    auth_screen()
    st.stop()

apply_theme(st, st.session_state.theme)

market = MarketDataClient()
risk = RiskAgent()
scanner = OpportunityAgent()
ai = AIDecisionAgent()
execution = ExecutionController()

st.sidebar.title("AI Portfolio Command Center")
section = st.sidebar.selectbox("Section", ["Command Center","Portfolio","AI Agents","Risk & Controls","Scanner","System","Settings"])
pages = {
"Command Center":["Home","AI Market Intelligence"],
"Portfolio":["Holdings","Performance"],
"AI Agents":["AI Decisions","Agent Execution"],
"Risk & Controls":["Risk Rules","Orders","Kill Switch"],
"Scanner":["Opportunity Scanner"],
"System":["System Health","Logs","QA Checklist"],
"Settings":["App Settings","Security"]
}
page = st.sidebar.selectbox("Page", pages[section])
st.session_state.theme = st.sidebar.selectbox("Theme", ["Dark","Light"])
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

if "holdings" not in st.session_state:
    st.session_state.holdings = [
        {"account_type":"TFSA","ticker":"VFV","asset_type":"ETF","quantity":1.0},
        {"account_type":"TFSA","ticker":"VEQT","asset_type":"ETF","quantity":1.0},
        {"account_type":"TFSA","ticker":"ZGD","asset_type":"ETF","quantity":1.0},
        {"account_type":"NON_REGISTERED","ticker":"NVDA","asset_type":"STOCK","quantity":1.0},
    ]

def holdings_df():
    rows=[]
    for r in st.session_state.holdings:
        t=str(r.get("ticker","")).upper().strip()
        if not t: continue
        p=market.get_price(t)
        q=float(r.get("quantity",0) or 0)
        rows.append({**r,"ticker":t,"last_price":p["price"],"currency":p["currency"],"market_value":round(q*p["price"],2)})
    return pd.DataFrame(rows)

def qdf(sql, params=None):
    res = run_query(sql, params or {})
    return pd.DataFrame(res.fetchall(), columns=res.keys())

hdf = holdings_df()
portfolio_value = float(hdf["market_value"].sum()) if not hdf.empty else 0

if page == "Home":
    st.title("AI Portfolio Command Center")
    rr = risk.evaluate_portfolio(hdf)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Portfolio Value", f"${portfolio_value:,.2f}")
    c2.metric("Risk Status", rr["status"])
    c3.metric("AI Agent", "ENABLED")
    c4.metric("Execution", "PAPER NOW / LIVE PATH LOCKED")
    if not hdf.empty:
        st.plotly_chart(px.pie(hdf, names="ticker", values="market_value", title="Portfolio Allocation"), use_container_width=True)

elif page == "Holdings":
    st.title("Holdings")
    ed = st.data_editor(pd.DataFrame(st.session_state.holdings), num_rows="dynamic", use_container_width=True)
    if st.button("Save Holdings"):
        st.session_state.holdings = ed.to_dict("records")
        st.rerun()
    st.dataframe(hdf, use_container_width=True)

elif page == "AI Market Intelligence":
    st.title("AI Market Intelligence")
    tickers = list(hdf["ticker"]) if not hdf.empty else ["VFV","VEQT","ZGD","NVDA"]
    st.dataframe(pd.DataFrame([market.get_price(t) for t in tickers]), use_container_width=True)

elif page == "AI Decisions":
    st.title("AI Decisions")
    st.success("AI agent can create proposed executable orders. Current execution mode: PAPER.")
    scored = scanner.run()
    recs = ai.recommend(scored)
    st.dataframe(pd.DataFrame(recs), use_container_width=True)
    if st.button("AI Agent Create Proposed Orders"):
        for r in recs:
            if r["action"] == "BUY":
                execution.propose_from_recommendation(r, market.get_price(r["ticker"])["price"], portfolio_value)
        st.success("AI agent created proposed executable paper orders.")

elif page == "Agent Execution":
    st.title("Agent Execution")
    st.warning("Agent execution is active for PAPER mode. Live mode pathway exists but is locked.")
    proposed = qdf("SELECT * FROM proposed_trades ORDER BY created_at DESC LIMIT 100")
    st.dataframe(proposed, use_container_width=True)
    oid = st.number_input("Order ID to approve", min_value=0, step=1)
    if st.button("Approve Order"):
        run_query("UPDATE proposed_trades SET approved=1,status='APPROVED' WHERE id=:id", {"id": int(oid)})
        st.success("Order approved.")
    if st.button("AI Agent Execute Approved Orders"):
        done = execution.execute_approved(portfolio_value)
        st.success(f"Executed: {done}")

elif page == "Risk Rules":
    st.title("Risk Rules")
    s = risk.settings()
    with st.form("risk"):
        max_risk = st.slider("Max risk per trade", 0.001, 0.05, float(s["max_risk_per_trade"]), 0.001)
        daily = st.slider("Daily loss limit", 0.005, 0.10, float(s["daily_loss_limit"]), 0.005)
        weekly = st.slider("Weekly loss limit", 0.01, 0.20, float(s["weekly_loss_limit"]), 0.005)
        monthly = st.slider("Monthly drawdown limit", 0.02, 0.30, float(s["monthly_drawdown_limit"]), 0.005)
        concentration = st.slider("Single-stock concentration", 0.05, 0.80, float(s["single_stock_concentration_limit"]), 0.01)
        paper = st.checkbox("Paper trading enabled", value=bool(s["paper_trading_enabled"]))
        agent_exec = st.checkbox("Agent execution enabled", value=bool(s["agent_execution_enabled"]))
        approval = st.checkbox("Human approval required", value=bool(s["human_approval_required"]))
        st.checkbox("Live trading enabled", value=bool(s["live_trading_enabled"]), disabled=True)
        st.checkbox("Margin enabled", value=bool(s["margin_enabled"]), disabled=True)
        if st.form_submit_button("Save Risk Settings"):
            run_query('''
            UPDATE risk_settings SET max_risk_per_trade=:max_risk,daily_loss_limit=:daily,
            weekly_loss_limit=:weekly,monthly_drawdown_limit=:monthly,
            single_stock_concentration_limit=:concentration,paper_trading_enabled=:paper,
            agent_execution_enabled=:agent_exec,human_approval_required=:approval,
            updated_at=CURRENT_TIMESTAMP WHERE id=1
            ''', {"max_risk":max_risk,"daily":daily,"weekly":weekly,"monthly":monthly,
            "concentration":concentration,"paper":int(paper),"agent_exec":int(agent_exec),"approval":int(approval)})
            st.success("Saved.")

elif page == "Orders":
    st.title("Orders")
    tab1, tab2 = st.tabs(["Proposed", "Executed"])
    with tab1:
        st.dataframe(qdf("SELECT * FROM proposed_trades ORDER BY created_at DESC LIMIT 100"), use_container_width=True)
    with tab2:
        st.dataframe(qdf("SELECT * FROM executed_trades ORDER BY executed_at DESC LIMIT 100"), use_container_width=True)

elif page == "Kill Switch":
    st.title("Kill Switch")
    st.error("Live execution is locked. Use this to stop paper order flow.")
    if st.button("Reject All Open Orders"):
        run_query("UPDATE proposed_trades SET status='REJECTED' WHERE status IN ('PROPOSED','APPROVED')")
        st.success("Open proposed/approved orders rejected.")

elif page == "Opportunity Scanner":
    st.title("Opportunity Scanner")
    scored = scanner.run()
    min_score = st.slider("Minimum opportunity score", 0, 100, 60)
    max_risk = st.slider("Maximum risk score", 0, 100, 70)
    st.dataframe(scored[(scored.opportunity_score >= min_score) & (scored.risk_score <= max_risk)], use_container_width=True)

elif page == "Performance":
    st.title("Strategy Performance")
    st.dataframe(qdf("SELECT * FROM executed_trades ORDER BY executed_at DESC LIMIT 100"), use_container_width=True)

elif page == "System Health":
    st.title("System Health")
    st.dataframe(qdf("SELECT component,status,MAX(last_run) AS last_run,message FROM system_health GROUP BY component ORDER BY component"), use_container_width=True)

elif page == "Logs":
    st.title("Agent Logs")
    st.dataframe(qdf("SELECT * FROM agent_logs ORDER BY id DESC LIMIT 200"), use_container_width=True)

elif page == "QA Checklist":
    st.title("QA Checklist")
    for item in QA_ITEMS:
        st.checkbox(item)

elif page == "App Settings":
    st.title("App Settings")
    st.json(risk.settings())
    st.info("Live execution pathway is present through BrokerInterface and LiveBrokerPlaceholder, but locked.")

elif page == "Security":
    st.title("Security")
    st.warning("Change the default password before deployment. Production should use Supabase Auth/Auth0/Clerk.")
    st.subheader("Change Password")
    with st.form("change_password_form"):
        current = st.text_input("Current password", type="password")
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Update password")
        if submitted:
            ok, msg = change_password(st.session_state.user["id"], current, new_password, confirm_password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
