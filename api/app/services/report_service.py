from typing import Dict, List
from datetime import datetime
from api.app.repo.trade_repository import TradeRepository
from api.app.repo.database import Trade

class PositionData:
    def __init__(self, broker: str, symbol: str, total_qty: int, avg_price: float):
        self.broker = broker
        self.symbol = symbol
        self.total_qty = total_qty
        self.avg_price = avg_price

class ReportService:
    def __init__(self, trade_repo: TradeRepository):
        self.trade_repo = trade_repo

    def calculate_positions(self) -> List[PositionData]:
        trades = self.trade_repo.get_all_trades()
        position_map: Dict[tuple, Dict] = {}

        for trade in trades:
            key = (trade.broker, trade.symbol)
            if key not in position_map:
                position_map[key] = {
                    'total_qty': 0,
                    'total_cost': 0.0
                }

            position_map[key]['total_qty'] += trade.fill_qty
            position_map[key]['total_cost'] += trade.fill_qty * trade.fill_price

        positions = []
        for (broker, symbol), data in position_map.items():
            avg_price = data['total_cost'] / data['total_qty'] if data['total_qty'] > 0 else 0
            positions.append(PositionData(broker, symbol, data['total_qty'], avg_price))

        return positions

    def get_all_trades(self) -> List[Trade]:
        return self.trade_repo.get_all_trades()
