from agents.base_agent import BaseAgent

class AIDecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__("AI Decision Agent")

    def recommend(self, scored, limit=10):
        rows = []
        for _, r in scored.head(limit).iterrows():
            action = "BUY" if r.opportunity_score >= 80 and r.risk_score <= 65 else "WATCH"
            rows.append({
                "ticker": r.ticker,
                "action": action,
                "account_type": "NON_REGISTERED",
                "confidence_score": min(r.opportunity_score/100, .95),
                "risk_level": "LOW" if r.risk_score < 40 else "MEDIUM" if r.risk_score < 65 else "HIGH",
                "reason": r.reason,
                "time_horizon": "short-term" if action=="BUY" else "watch",
                "execution_mode": "PAPER"
            })
        self.health("GREEN", f"{len(rows)} recommendations generated")
        self.log("INFO", "AI recommendations generated", {"count": len(rows)})
        return rows
