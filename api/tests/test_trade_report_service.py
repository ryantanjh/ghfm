import pytest
from unittest.mock import Mock
from api.app.services.trade_report_service import TradeReportService
from api.app.repo.database import Trade
from datetime import datetime

@pytest.fixture
def mock_trade_repo():
    return Mock()

@pytest.fixture
def trade_report_service(mock_trade_repo):
    return TradeReportService(mock_trade_repo)

def test_generate_csv_report_with_trades(trade_report_service, mock_trade_repo):
    trade1 = Trade(
        trade_id=1,
        order_id=1,
        broker="IBKR",
        symbol="AAPL",
        fill_qty=100,
        fill_price=150.50,
        timestamp=datetime(2026, 4, 3, 10, 0, 0)
    )
    trade2 = Trade(
        trade_id=2,
        order_id=2,
        broker="IBKR",
        symbol="GOOGL",
        fill_qty=50,
        fill_price=2800.75,
        timestamp=datetime(2026, 4, 3, 11, 0, 0)
    )
    mock_trade_repo.get_all_trades.return_value = [trade1, trade2]

    csv_content = trade_report_service.generate_csv_report()

    assert "Trade ID,Order ID,Broker,Symbol,Fill Price,Fill Quantity,Timestamp" in csv_content
    assert "AAPL" in csv_content
    assert "GOOGL" in csv_content
    assert "150.50" in csv_content
    assert "2800.75" in csv_content
    assert "2026-04-03 10:00:00" in csv_content

def test_generate_csv_report_empty(trade_report_service, mock_trade_repo):
    mock_trade_repo.get_all_trades.return_value = []

    csv_content = trade_report_service.generate_csv_report()

    assert "Trade ID,Order ID,Broker,Symbol,Fill Price,Fill Quantity,Timestamp" in csv_content
    lines = csv_content.strip().split('\n')
    assert len(lines) == 1
