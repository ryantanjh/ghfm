# PLAN

## Db schema 
Orders table
- order id
- broker
- symbol
- order type
- price
- qty
- order status
- rejection reason

Trades table
- Order id
- trade id
- broker
- symbol
- fill qty
- fill price
- timestamp

# General Project Architecture
/client
    /src
        /pages
        /components
    app.ts
/api
    requirements.txt
    start.sh
    /app
        main.py # all routes go here, injects services layer as dependency
        /models # pydantic dtos
        /repo # repo layer classes
            database.py # SQLAlchemy engine + Sqlite setup
        /services # business logic, injects repo layer as dependency
    /tests # unit testing for functions in services layer
    /brokers # classes simulating API calls to broker REST API endpoints. It should only accomodate cases for the mock workflow


## Features 
Feature 1: API /POST send_limit_order. User creates a limit order in our OMS system
- As a user, i should be able to create an order with the following details
  - broker
  - symbol
  - order type (assert it is only limit)
  - price
  - qty
- What happens in the OMS service handler: 
  1. Store order in order database as NEW
  2. Do internal validation check (for now do nothing)
     -  If pass internal validation check:
       - Update Order status updated to SENT
       - Send order to mock broker and read broker response on order status, which can be FILL, PARTIAL_FILL, REJECTION
       - Update Orders table with order status
     - If fail internal validation check: order status remains as NEW
  3. Update trade table
     - If order response if FILL or PARTIAL FILL, update trades table with Trade details from the broker API response

Feature 2: Mock workflows
1. Order remains in NEW state
- User creates a new order in the UI for AAPL stock for IBKR
- This order should always remain in NEW state, reason being it has failed internal validation check

2. Order sent but rejected by broker
- User has a account balance of 1 million USD
- User creates a new order in the UI for DBS stock for IBKR at qty = 1 million which exceeds balance
- Mock broker API returns Rejection message due "insufficient balance"
- Update order status accordingly

3. Order Sent and Filled fully
- User creates a new order in the UI for DBS stock for IBKR that does not exceed account balance threshold
- User gets a response for FILL
- User should be able to see updated order status and trade records in UI

4. Order Sent and Partial Fill
- User creates a new order in the UI for DBS stock for IBKR that does not exceed account threshold
- User gets a response for Partial fill
- User should be able to see updated order status and trade records in UI

Feature 3: UI
- OMS page: User should be able to submit an order via a form based on the above workflow scenarios
- Orders / Trades view page: User should be able to view current status of all orders and trades from internal db







