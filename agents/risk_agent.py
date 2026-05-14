from agents.base_agent import BaseAgent
from database.db import run_query

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("Risk Agent")

    def settings(self):
        row = run_query("SELECT * FROM risk_settings WHERE id=1").fetchone()
        return dict(row._mapping)

    def evaluate_portfolio(self, df):
        s = self.settings()
        warnings = []
        if df.empty:
            self.health("YELLOW", "No holdings entered")
            return {"status": "YELLOW", "warnings": ["No holdings entered yet"], "settings": s}
        total = df["market_value"].sum()
        for _, r in df.iterrows():
            weight = r["market_value"] / total if total else 0
            if r["asset_type"] == "STOCK" and weight > s["single_stock_concentration_limit"]:
                warnings.append(f"{r['ticker']} exceeds {s['single_stock_concentration_limit']:.0%} stock concentration.")
            if r["account_type"] == "TFSA" and r["asset_type"] not in ["ETF", "CASH"]:
                warnings.append(f"{r['ticker']} is not ETF/CASH inside TFSA.")
        status = "GREEN" if not warnings else "YELLOW"
        self.health(status, "Risk check completed")
        self.log("INFO", "Portfolio risk evaluated", {"warnings": warnings})
        return {"status": status, "warnings": warnings, "settings": s}

    def approve_trade(self, trade, portfolio_value):
        s = self.settings()

        if not s["agent_execution_enabled"]:
            return False, "Agent execution is disabled."

        if trade.get("execution_mode") == "LIVE" and not s["live_trading_enabled"]:
            return False, "Live trading is disabled."

        if trade.get("execution_mode") == "LIVE_LOCKED":
            return False, "Live path exists but is locked until future release."

        if trade.get("execution_mode") != "PAPER":
            return False, "Only PAPER execution is allowed in Phase 1.5."

        if trade.get("max_loss", 0) > portfolio_value * s["max_risk_per_trade"]:
            return False, "Max loss exceeds risk per trade."

        if trade.get("account_type") == "TFSA" and trade.get("time_horizon") == "short-term":
            return False, "Short-term TFSA trading is blocked."

        return True, "Approved by Risk Agent."
