from sqlalchemy.orm import Session
from api.app.repo.database import Order
from typing import List

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, broker: str, symbol: str, order_type: str, price: float, qty: int, order_status: str) -> Order:
        order = Order(
            broker=broker,
            symbol=symbol,
            order_type=order_type,
            price=price,
            qty=qty,
            order_status=order_status
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order_status(self, order_id: int, status: str, rejection_reason: str = None) -> Order:
        order = self.db.query(Order).filter(Order.order_id == order_id).first()
        if order:
            order.order_status = status
            if rejection_reason:
                order.rejection_reason = rejection_reason
            self.db.commit()
            self.db.refresh(order)
        return order

    def get_order(self, order_id: int) -> Order:
        return self.db.query(Order).filter(Order.order_id == order_id).first()

    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).all()
