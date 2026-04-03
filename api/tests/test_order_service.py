import pytest
from unittest.mock import Mock
from api.app.services.order_service import OrderService
from api.app.models.dtos import OrderCreate, BrokerOrderResponse
from api.app.repo.database import Order, Trade

@pytest.fixture
def mock_order_repo():
    return Mock()

@pytest.fixture
def mock_trade_repo():
    return Mock()

@pytest.fixture
def mock_broker():
    return Mock()

@pytest.fixture
def order_service(mock_order_repo, mock_trade_repo, mock_broker):
    return OrderService(mock_order_repo, mock_trade_repo, mock_broker)

def test_create_order_aapl_fails_validation(order_service, mock_order_repo):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="AAPL",
        order_type="LIMIT",
        price=150.0,
        qty=100
    )

    mock_order = Order(
        order_id=1,
        broker="IBKR",
        symbol="AAPL",
        order_type="LIMIT",
        price=150.0,
        qty=100,
        order_status="NEW"
    )
    mock_order_repo.create_order.return_value = mock_order

    result = order_service.create_order(order_data)

    assert result.order_status == "NEW"
    mock_order_repo.update_order_status.assert_not_called()

def test_create_order_rejected_insufficient_balance(order_service, mock_order_repo, mock_trade_repo, mock_broker):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=100.0,
        qty=1000000
    )

    mock_order = Order(
        order_id=2,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=100.0,
        qty=1000000,
        order_status="NEW"
    )
    mock_order_repo.create_order.return_value = mock_order

    mock_broker.send_order.return_value = BrokerOrderResponse(
        status="REJECTED",
        rejection_reason="Insufficient balance",
        fill_qty=None,
        fill_price=None
    )

    mock_rejected_order = Order(
        order_id=2,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=100.0,
        qty=1000000,
        order_status="REJECTED",
        rejection_reason="Insufficient balance"
    )
    mock_order_repo.get_order.return_value = mock_rejected_order

    result = order_service.create_order(order_data)

    assert result.order_status == "REJECTED"
    assert result.rejection_reason == "Insufficient balance"

def test_create_order_filled(order_service, mock_order_repo, mock_trade_repo, mock_broker):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=100
    )

    mock_order = Order(
        order_id=3,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=100,
        order_status="NEW"
    )
    mock_order_repo.create_order.return_value = mock_order

    mock_broker.send_order.return_value = BrokerOrderResponse(
        status="FILLED",
        rejection_reason=None,
        fill_qty=100,
        fill_price=30.0
    )

    mock_filled_order = Order(
        order_id=3,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=100,
        order_status="FILLED"
    )
    mock_order_repo.get_order.return_value = mock_filled_order

    result = order_service.create_order(order_data)

    assert result.order_status == "FILLED"
    mock_trade_repo.create_trade.assert_called_once()

def test_create_order_partial_fill(order_service, mock_order_repo, mock_trade_repo, mock_broker):
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=101
    )

    mock_order = Order(
        order_id=4,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=101,
        order_status="NEW"
    )
    mock_order_repo.create_order.return_value = mock_order

    mock_broker.send_order.return_value = BrokerOrderResponse(
        status="PARTIAL_FILL",
        rejection_reason=None,
        fill_qty=50,
        fill_price=30.0
    )

    mock_partial_order = Order(
        order_id=4,
        broker="IBKR",
        symbol="DBS",
        order_type="LIMIT",
        price=30.0,
        qty=101,
        order_status="PARTIAL_FILL"
    )
    mock_order_repo.get_order.return_value = mock_partial_order

    result = order_service.create_order(order_data)

    assert result.order_status == "PARTIAL_FILL"
    mock_trade_repo.create_trade.assert_called_once()

def test_create_order_non_limit_type_fails():
    order_service = OrderService(Mock(), Mock(), Mock())
    order_data = OrderCreate(
        broker="IBKR",
        symbol="DBS",
        order_type="MARKET",
        price=30.0,
        qty=100
    )

    with pytest.raises(AssertionError, match="Only LIMIT orders are supported"):
        order_service.create_order(order_data)
