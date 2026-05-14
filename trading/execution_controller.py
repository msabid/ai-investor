from database.db import run_query
from agents.base_agent import BaseAgent
from agents.risk_agent import RiskAgent
from brokers.paper_broker import PaperBroker
from brokers.live_broker_placeholder import LiveBrokerPlaceholder

class ExecutionController(BaseAgent):
    def __init__(self):
        super().__init__("Execution Controller")
        self.risk = RiskAgent()
        self.paper_broker = PaperBroker()
        self.live_broker = LiveBrokerPlaceholder()

    def propose_from_recommendation(self, rec, price, portfolio_value):
        qty = 1.0
        max_loss = portfolio_value * 0.005
        stop = price * .95 if rec["action"] == "BUY" else None
        run_query('''
        INSERT INTO proposed_trades(ticker,action,account_type,quantity,estimated_price,estimated_value,
        max_loss,stop_loss,reason,risk_level,confidence_score,status,execution_mode,
        human_approval_required,approved,created_by_agent)
        VALUES(:ticker,:action,:account_type,:qty,:price,:value,:max_loss,:stop,:reason,:risk,:conf,
        'PROPOSED',:mode,1,0,'AI Decision Agent')
        ''', {
            "ticker":rec["ticker"],"action":rec["action"],"account_type":rec["account_type"],
            "qty":qty,"price":price,"value":qty*price,"max_loss":max_loss,"stop":stop,
            "reason":rec["reason"],"risk":rec["risk_level"],"conf":rec["confidence_score"],
            "mode":rec.get("execution_mode","PAPER")
        })
        self.log("INFO", "Proposed order created by AI agent", rec)

    def execute_approved(self, portfolio_value):
        orders = run_query("SELECT * FROM proposed_trades WHERE approved=1 AND status='APPROVED'").fetchall()
        executed = []
        for o in orders:
            trade = {
                "ticker": o.ticker,
                "action": o.action,
                "account_type": o.account_type,
                "max_loss": o.max_loss,
                "execution_mode": o.execution_mode,
                "time_horizon": "short-term"
            }
            ok, reason = self.risk.approve_trade(trade, portfolio_value)
            if not ok:
                run_query("UPDATE proposed_trades SET status='REJECTED' WHERE id=:id", {"id": o.id})
                self.log("WARNING", "Order rejected by risk gate", {"id": o.id, "reason": reason})
                continue

            broker = self.paper_broker if o.execution_mode == "PAPER" else self.live_broker
            fill = broker.place_order({
                "ticker": o.ticker,
                "action": o.action,
                "quantity": o.quantity,
                "estimated_price": o.estimated_price
            })

            run_query('''
            INSERT INTO executed_trades(proposed_trade_id,ticker,action,account_type,quantity,fill_price,currency,execution_mode,broker)
            VALUES(:id,:ticker,:action,:account,:qty,:price,'USD',:mode,:broker)
            ''', {
                "id": o.id, "ticker": o.ticker, "action": o.action, "account": o.account_type,
                "qty": fill["quantity"], "price": fill["fill_price"], "mode": o.execution_mode, "broker": fill["broker"]
            })
            run_query("UPDATE proposed_trades SET status='EXECUTED' WHERE id=:id", {"id": o.id})
            executed.append(o.ticker)

        self.health("GREEN", f"Executed {len(executed)} approved orders")
        return executed
