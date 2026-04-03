from api.app.repo.order_repository import OrderRepository
from api.app.repo.trade_repository import TradeRepository
from api.app.models.dtos import OrderCreate, OrderResponse
from api.brokers.broker_interface import BrokerInterface
from typing import List

class OrderService:
    def __init__(self, order_repo: OrderRepository, trade_repo: TradeRepository, broker: BrokerInterface):
        self.order_repo = order_repo
        self.trade_repo = trade_repo
        self.broker = broker

    def _validate_order(self, order_data: OrderCreate) -> bool:
        if order_data.symbol == "AAPL":
            return False
        return True

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        assert order_data.order_type.upper() == "LIMIT", "Only LIMIT orders are supported"

        order = self.order_repo.create_order(
            broker=order_data.broker,
            symbol=order_data.symbol,
            order_type=order_data.order_type,
            price=order_data.price,
            qty=order_data.qty,
            order_status="NEW"
        )

        if not self._validate_order(order_data):
            return OrderResponse.from_orm(order)

        self.order_repo.update_order_status(order.order_id, "SENT")

        broker_response = self.broker.send_order(
            broker=order_data.broker,
            symbol=order_data.symbol,
            order_type=order_data.order_type,
            price=order_data.price,
            qty=order_data.qty
        )

        if broker_response.status == "REJECTED":
            self.order_repo.update_order_status(
                order.order_id,
                "REJECTED",
                broker_response.rejection_reason
            )
        elif broker_response.status == "FILLED":
            self.order_repo.update_order_status(order.order_id, "FILLED")
            self.trade_repo.create_trade(
                order_id=order.order_id,
                broker=order_data.broker,
                symbol=order_data.symbol,
                fill_qty=broker_response.fill_qty,
                fill_price=broker_response.fill_price
            )
        elif broker_response.status == "PARTIAL_FILL":
            self.order_repo.update_order_status(order.order_id, "PARTIAL_FILL")
            self.trade_repo.create_trade(
                order_id=order.order_id,
                broker=order_data.broker,
                symbol=order_data.symbol,
                fill_qty=broker_response.fill_qty,
                fill_price=broker_response.fill_price
            )
        else:
            self.order_repo.update_order_status(order.order_id, broker_response.status)

        updated_order = self.order_repo.get_order(order.order_id)
        return OrderResponse.from_orm(updated_order)

    def get_all_orders(self) -> List:
        return self.order_repo.get_all_orders()
