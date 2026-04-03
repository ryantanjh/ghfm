from api.app.models.dtos import BrokerOrderResponse

class MockBroker:
    def send_order(self, broker: str, symbol: str, order_type: str, price: float, qty: int) -> BrokerOrderResponse:
        return BrokerOrderResponse(
            status="NEW",
            rejection_reason=None,
            fill_qty=None,
            fill_price=None
        )
