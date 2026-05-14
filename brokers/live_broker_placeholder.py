from brokers.broker_interface import BrokerInterface

class LiveBrokerPlaceholder(BrokerInterface):
    def get_positions(self):
        raise RuntimeError("Live broker is not enabled in Phase 1.5.")

    def get_balance(self):
        raise RuntimeError("Live broker is not enabled in Phase 1.5.")

    def place_order(self, order):
        raise RuntimeError("Blocked: live trading pathway exists but is locked.")

    def cancel_order(self, order_id):
        raise RuntimeError("Blocked: live trading pathway exists but is locked.")
