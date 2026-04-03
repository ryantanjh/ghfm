from api.app.repo.order_repository import OrderRepository
from api.app.repo.trade_repository import TradeRepository
from api.app.models.dtos import OrderCreate, OrderResponse

class OrderService:
    def __init__(self, order_repo: OrderRepository, trade_repo: TradeRepository):
        self.order_repo = order_repo
        self.trade_repo = trade_repo

    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        order = self.order_repo.create_order(
            broker=order_data.broker,
            symbol=order_data.symbol,
            order_type=order_data.order_type,
            price=order_data.price,
            qty=order_data.qty,
            order_status="NEW"
        )
        return OrderResponse.from_orm(order)

    def get_all_orders(self):
        return self.order_repo.get_all_orders()
