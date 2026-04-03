from abc import ABC, abstractmethod
from api.app.models.dtos import BrokerOrderResponse

class BrokerInterface(ABC):
    @abstractmethod
    def send_order(self, broker: str, symbol: str, order_type: str, price: float, qty: int) -> BrokerOrderResponse:
        pass
