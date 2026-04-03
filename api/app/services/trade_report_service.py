from api.app.repo.trade_repository import TradeRepository
import csv
import io

class TradeReportService:
    def __init__(self, trade_repository: TradeRepository):
        self.trade_repository = trade_repository

    def generate_csv_report(self) -> str:
        trades = self.trade_repository.get_all_trades()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['Trade ID', 'Order ID', 'Broker', 'Symbol', 'Fill Price', 'Fill Quantity', 'Timestamp'])

        for trade in trades:
            writer.writerow([
                trade.trade_id,
                trade.order_id,
                trade.broker,
                trade.symbol,
                f"{trade.fill_price:.2f}",
                trade.fill_qty,
                trade.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return output.getvalue()
