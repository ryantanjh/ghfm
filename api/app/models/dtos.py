from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    broker: str
    symbol: str
    order_type: str
    price: float
    qty: int

class OrderResponse(BaseModel):
    order_id: int
    broker: str
    symbol: str
    order_type: str
    price: float
    qty: int
    order_status: str
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True

class TradeResponse(BaseModel):
    trade_id: int
    order_id: int
    broker: str
    symbol: str
    fill_qty: int
    fill_price: float
    timestamp: datetime

    class Config:
        from_attributes = True

class BrokerOrderResponse(BaseModel):
    status: str
    rejection_reason: Optional[str] = None
    fill_qty: Optional[int] = None
    fill_price: Optional[float] = None
