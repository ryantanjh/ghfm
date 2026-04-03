import pytest
from api.app.repo.database import SessionLocal, Base, engine, Order, Trade
from api.app.repo.order_repository import OrderRepository
from api.app.repo.trade_repository import TradeRepository
from api.app.services.order_service import OrderService
from api.app.models.dtos import OrderCreate
from api.brokers.mock_broker import MockBroker

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def order_repo(db_session):
    return OrderRepository(db_session)

@pytest.fixture
def trade_repo(db_session):
    return TradeRepository(db_session)

@pytest.fixture
def broker():
    return MockBroker()

@pytest.fixture
def order_service(order_repo, trade_repo, broker):
    return OrderService(order_repo, trade_repo, broker)

def test_workflow_1_aapl_remains_new(order_service, db_session):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="AAPL",
        order_type="LIMIT",
        price=150.0,
        qty=100
    )

    result = order_service.create_order(order_data)

    assert result.order_status == "NEW"
    assert result.rejection_reason is None

    db_order = db_session.query(Order).filter(Order.order_id == result.order_id).first()
    assert db_order.order_status == "NEW"

    trades = db_session.query(Trade).filter(Trade.order_id == result.order_id).all()
    assert len(trades) == 0

def test_workflow_2_rejected_insufficient_balance(order_service, db_session):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=100.0,
        qty=1000000
    )

    result = order_service.create_order(order_data)

    assert result.order_status == "REJECTED"
    assert result.rejection_reason == "Insufficient balance"

    db_order = db_session.query(Order).filter(Order.order_id == result.order_id).first()
    assert db_order.order_status == "REJECTED"
    assert db_order.rejection_reason == "Insufficient balance"

    trades = db_session.query(Trade).filter(Trade.order_id == result.order_id).all()
    assert len(trades) == 0

def test_workflow_3_filled_fully(order_service, db_session):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=100
    )

    result = order_service.create_order(order_data)

    assert result.order_status == "FILLED"

    db_order = db_session.query(Order).filter(Order.order_id == result.order_id).first()
    assert db_order.order_status == "FILLED"

    trades = db_session.query(Trade).filter(Trade.order_id == result.order_id).all()
    assert len(trades) == 1
    assert trades[0].fill_qty == 100
    assert trades[0].fill_price == 30.0
    assert trades[0].symbol == "DBS"
    assert trades[0].broker == "IBKR"

def test_workflow_4_partial_fill(order_service, db_session):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=101
    )

    result = order_service.create_order(order_data)

    assert result.order_status == "PARTIAL_FILL"

    db_order = db_session.query(Order).filter(Order.order_id == result.order_id).first()
    assert db_order.order_status == "PARTIAL_FILL"

    trades = db_session.query(Trade).filter(Trade.order_id == result.order_id).all()
    assert len(trades) == 1
    assert trades[0].fill_qty == 50
    assert trades[0].fill_price == 30.0
    assert trades[0].symbol == "DBS"
    assert trades[0].broker == "IBKR"
