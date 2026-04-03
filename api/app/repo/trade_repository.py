from sqlalchemy.orm import Session
from api.app.repo.database import Trade
from typing import List

class TradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_trade(self, order_id: int, broker: str, symbol: str, fill_qty: int, fill_price: float) -> Trade:
        trade = Trade(
            order_id=order_id,
            broker=broker,
            symbol=symbol,
            fill_qty=fill_qty,
            fill_price=fill_price
        )
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade

    def get_trades_by_order(self, order_id: int) -> List[Trade]:
        return self.db.query(Trade).filter(Trade.order_id == order_id).all()

    def get_all_trades(self) -> List[Trade]:
        return self.db.query(Trade).all()
