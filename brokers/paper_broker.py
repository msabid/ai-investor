from brokers.broker_interface import BrokerInterface

class PaperBroker(BrokerInterface):
    def get_positions(self):
        return []

    def get_balance(self):
        return {"cash": 100000, "currency": "CAD", "mode": "PAPER"}

    def place_order(self, order):
        return {
            "broker": "PaperBroker",
            "status": "FILLED",
            "fill_price": order["estimated_price"],
            "quantity": order["quantity"],
            "mode": "PAPER"
        }

    def cancel_order(self, order_id):
        return {"broker": "PaperBroker", "status": "CANCELLED", "order_id": order_id}
