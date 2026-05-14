from abc import ABC, abstractmethod

class BrokerInterface(ABC):
    @abstractmethod
    def get_positions(self):
        raise NotImplementedError

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError

    @abstractmethod
    def place_order(self, order):
        raise NotImplementedError

    @abstractmethod
    def cancel_order(self, order_id):
        raise NotImplementedError
