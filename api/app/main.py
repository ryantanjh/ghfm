from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api.app.repo.database import get_db, init_db
from api.app.repo.order_repository import OrderRepository
from api.app.repo.trade_repository import TradeRepository
from api.app.services.order_service import OrderService
from api.app.models.dtos import OrderCreate, OrderResponse, TradeResponse
from typing import List

app = FastAPI(title="OMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "OMS API is running"}

@app.post("/send_limit_order", response_model=OrderResponse)
def send_limit_order(order: OrderCreate, db: Session = Depends(get_db)) -> OrderResponse:
    order_repo = OrderRepository(db)
    trade_repo = TradeRepository(db)
    order_service = OrderService(order_repo, trade_repo)
    return order_service.create_order(order)

@app.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)) -> List[OrderResponse]:
    order_repo = OrderRepository(db)
    trade_repo = TradeRepository(db)
    order_service = OrderService(order_repo, trade_repo)
    orders = order_service.get_all_orders()
    return [OrderResponse.from_orm(order) for order in orders]

@app.get("/trades", response_model=List[TradeResponse])
def get_trades(db: Session = Depends(get_db)) -> List[TradeResponse]:
    trade_repo = TradeRepository(db)
    trades = trade_repo.get_all_trades()
    return [TradeResponse.from_orm(trade) for trade in trades]
