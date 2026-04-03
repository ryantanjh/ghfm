from api.app.models.dtos import BrokerOrderResponse

class MockBroker:
    ACCOUNT_BALANCE = 1000000.0

    def send_order(self, broker: str, symbol: str, order_type: str, price: float, qty: int) -> BrokerOrderResponse:
        order_value = price * qty

        if order_value > self.ACCOUNT_BALANCE:
            return BrokerOrderResponse(
                status="REJECTED",
                rejection_reason="Insufficient balance",
                fill_qty=None,
                fill_price=None
            )

        if symbol == "DBS" and order_value <= self.ACCOUNT_BALANCE:
            if qty % 2 == 0:
                return BrokerOrderResponse(
                    status="FILLED",
                    rejection_reason=None,
                    fill_qty=qty,
                    fill_price=price
                )
            else:
                partial_qty = qty // 2
                return BrokerOrderResponse(
                    status="PARTIAL_FILL",
                    rejection_reason=None,
                    fill_qty=partial_qty,
                    fill_price=price
                )

        return BrokerOrderResponse(
            status="SENT",
            rejection_reason=None,
            fill_qty=None,
            fill_price=None
        )
