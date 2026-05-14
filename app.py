import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import init_db, run_query
from data_sources.market_data import MarketDataClient
from data_sources.news_data import NewsClient
from agents.risk_agent import RiskAgent
from analytics.opportunity_scanner import get_starter_universe, score_universe
from dashboard.qa_checklist import QA_ITEMS

st.set_page_config(page_title="AI Portfolio Command Center", layout="wide")

init_db()

market_client = MarketDataClient()
news_client = NewsClient()
risk_agent = RiskAgent()

st.sidebar.title("AI Portfolio Command Center")
page = st.sidebar.radio(
    "Navigation",
    [
        "Home", "Holdings", "Market", "News", "AI Decisions", "Orders",
        "Risk", "Opportunity Scanner", "Strategy Performance",
        "System Health", "Settings", "QA Checklist"
    ]
)

def load_agent_logs():
    result = run_query("SELECT agent_name, level, message, created_at FROM agent_logs ORDER BY id DESC LIMIT 50")
    return pd.DataFrame(result.fetchall(), columns=result.keys())

def get_manual_holdings_df(input_rows):
    rows = []
    for row in input_rows:
        ticker = row["ticker"].upper().strip()
        if not ticker:
            continue
        price_data = market_client.get_price(ticker)
        quantity = float(row["quantity"])
        market_value = round(quantity * price_data["price"], 2)
        rows.append({
            "account_type": row["account_type"],
            "ticker": ticker,
            "asset_type": row["asset_type"],
            "quantity": quantity,
            "last_price": price_data["price"],
            "currency": price_data["currency"],
            "market_value": market_value
        })
    return pd.DataFrame(rows)

default_holdings = [
    {"account_type": "TFSA", "ticker": "VFV", "asset_type": "ETF", "quantity": 1.0},
    {"account_type": "TFSA", "ticker": "VEQT", "asset_type": "ETF", "quantity": 1.0},
    {"account_type": "TFSA", "ticker": "ZGD", "asset_type": "ETF", "quantity": 1.0},
    {"account_type": "NON_REGISTERED", "ticker": "NVDA", "asset_type": "STOCK", "quantity": 1.0},
]

if "manual_holdings" not in st.session_state:
    st.session_state.manual_holdings = default_holdings

holdings_df = get_manual_holdings_df(st.session_state.manual_holdings)

if page == "Home":
    st.title("AI Portfolio Command Center")
    st.caption("MVP: dashboard, manual tracking, risk status, opportunity scanner shell, and QA checklist. No real trading.")

    col1, col2, col3, col4 = st.columns(4)
    total_value = holdings_df["market_value"].sum() if not holdings_df.empty else 0
    risk_result = risk_agent.evaluate_portfolio(holdings_df)

    col1.metric("Portfolio Value", f"${total_value:,.2f}")
    col2.metric("Risk Status", risk_result["status"])
    col3.metric("Live Trading", "DISABLED")
    col4.metric("Margin", "DISABLED")

    st.subheader("Portfolio Allocation")
    if not holdings_df.empty:
        fig = px.pie(holdings_df, names="ticker", values="market_value", title="Current Manual Holdings")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Enter holdings on the Holdings page.")

    st.subheader("System Principle")
    st.write("1. Survival and capital preservation → 2. Long-term compounding → 3. Maximizing returns")

elif page == "Holdings":
    st.title("Holdings")
    st.write("Enter holdings manually for MVP. Broker sync comes later.")

    edited_df = st.data_editor(
        pd.DataFrame(st.session_state.manual_holdings),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "account_type": st.column_config.SelectboxColumn("Account Type", options=["TFSA", "NON_REGISTERED", "PAPER"]),
            "asset_type": st.column_config.SelectboxColumn("Asset Type", options=["ETF", "STOCK", "CASH"]),
        }
    )

    if st.button("Save Manual Holdings"):
        st.session_state.manual_holdings = edited_df.to_dict("records")
        st.success("Manual holdings saved for this session.")

    holdings_df = get_manual_holdings_df(st.session_state.manual_holdings)
    st.subheader("Valuation")
    st.dataframe(holdings_df, use_container_width=True)

    if not holdings_df.empty:
        fig = px.bar(holdings_df, x="ticker", y="market_value", color="account_type", title="Market Value by Holding")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Market":
    st.title("Market")
    ticker = st.text_input("Ticker", "VFV")
    if st.button("Fetch Price"):
        data = market_client.get_price(ticker)
        st.json(data)

elif page == "News":
    st.title("News")
    ticker = st.text_input("Ticker or topic", "NVDA")
    headlines = news_client.get_headlines(ticker)
    st.dataframe(pd.DataFrame(headlines), use_container_width=True)

elif page == "AI Decisions":
    st.title("AI Decisions")
    st.warning("AI integration is disabled in MVP. AI cannot execute trades or override risk rules.")
    st.write("Future AI duties: summarize news, summarize macro, explain trades, rank opportunities, detect risk patterns.")

elif page == "Orders":
    st.title("Orders")
    st.error("No real trading is available in MVP.")
    st.write("Order execution requires paper trading first, then broker integration, then human approval.")

elif page == "Risk":
    st.title("Risk")
    risk_result = risk_agent.evaluate_portfolio(holdings_df)
    st.metric("Risk Status", risk_result["status"])

    if risk_result["warnings"]:
        for warning in risk_result["warnings"]:
            st.warning(warning)
    else:
        st.success("No MVP risk warnings detected.")

    st.subheader("Mandatory Rules")
    st.json(risk_result["rules"])

elif page == "Opportunity Scanner":
    st.title("Opportunity Scanner")
    st.caption("MVP shell only. Scores are placeholders until real data validation is added.")
    universe = get_starter_universe()
    scored = score_universe(universe)
    st.dataframe(scored, use_container_width=True)

elif page == "Strategy Performance":
    st.title("Strategy Performance")
    st.info("Strategy isolation and performance tracking will be added in later phases.")

elif page == "System Health":
    st.title("System Health")
    st.metric("Overall Status", "YELLOW")
    st.write("Yellow because MVP uses mock market data and has no broker/database resilience checks yet.")

    st.subheader("Recent Agent Logs")
    logs = load_agent_logs()
    st.dataframe(logs, use_container_width=True)

elif page == "Settings":
    st.title("Settings")
    st.subheader("Safety Defaults")
    st.json({
        "live_trading_enabled": False,
        "paper_trading_enabled": False,
        "margin_enabled": False,
        "tfsa_mode": "long-term ETF-focused",
        "options_enabled": False,
        "human_approval_required": True
    })

elif page == "QA Checklist":
    st.title("QA Checklist")
    st.write("Use this checklist after each phase.")
    for item in QA_ITEMS:
        st.checkbox(item, value=False)
