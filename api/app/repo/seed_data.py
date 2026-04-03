from sqlalchemy.orm import Session
from api.app.repo.database import Order, Trade
from datetime import datetime, timedelta

def seed_database(db: Session):
    existing_orders = db.query(Order).count()
    if existing_orders > 0:
        return

    base_time = datetime.utcnow()

    seed_orders = [
        Order(
            order_id=1,
            broker="IBKR",
            symbol="AAPL",
            order_type="LIMIT",
            price=150.00,
            qty=100,
            order_status="NEW",
            rejection_reason=None
        ),
        Order(
            order_id=2,
            broker="IBKR",
            symbol="DBS",
            order_type="LIMIT",
            price=35.00,
            qty=1000000,
            order_status="REJECTED",
            rejection_reason="Insufficient balance"
        ),
        Order(
            order_id=3,
            broker="IBKR",
            symbol="DBS",
            order_type="LIMIT",
            price=35.00,
            qty=100,
            order_status="FILLED",
            rejection_reason=None
        ),
        Order(
            order_id=4,
            broker="IBKR",
            symbol="DBS",
            order_type="LIMIT",
            price=35.00,
            qty=101,
            order_status="PARTIAL_FILL",
            rejection_reason=None
        )
    ]

    seed_trades = [
        Trade(
            trade_id=1,
            order_id=3,
            broker="IBKR",
            symbol="DBS",
            fill_qty=100,
            fill_price=35.00,
            timestamp=base_time - timedelta(minutes=5)
        ),
        Trade(
            trade_id=2,
            order_id=4,
            broker="IBKR",
            symbol="DBS",
            fill_qty=50,
            fill_price=35.00,
            timestamp=base_time - timedelta(minutes=3)
        )
    ]

    db.bulk_save_objects(seed_orders)
    db.bulk_save_objects(seed_trades)
    db.commit()
