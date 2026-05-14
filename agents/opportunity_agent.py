from agents.base_agent import BaseAgent
from analytics.opportunity_scanner import score_universe

class OpportunityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Opportunity Scanner Agent")

    def run(self):
        df = score_universe()
        self.health("GREEN", f"{len(df)} assets scanned")
        self.log("INFO", "Opportunity scan completed", {"count": len(df)})
        return df
