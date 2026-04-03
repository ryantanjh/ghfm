# PLAN

## Database Schema
Orders Table
- Order ID
- Broker
- Symbol
- Order Type
- Price
- Quantity
- Order Status
- Rejection Reason

Trades Table
- Order ID
- Trade ID
- Broker
- Symbol
- Fill Quantity
- Fill Price
- Timestamp

# General Project Architecture

## Directory Structure

### Client (`/client`)
- **`/src`**
  - `/pages` - Page components
  - `/components` - Reusable UI components
- **`app.ts`** - Main application entry point

### API (`/api`)
- **`requirements.txt`** - Python dependencies
- **`start.sh`** - Application startup script
- **`/app`**
  - **`main.py`** - API routes and endpoints (injects services layer as dependency)
  - **`/models`** - Pydantic DTOs
  - **`/repo`** - Repository layer classes
    - `database.py` - SQLAlchemy engine + SQLite setup
  - **`/services`** - Business logic layer (injects repo layer as dependency)
- **`/tests`** - Unit tests for services layer functions
- **`/brokers`** - Mock broker API clients (simulates broker REST API endpoints for mock workflows)


## Features
Feature 1: API /POST send_limit_order - User creates a limit order in the OMS system
- As a user, I should be able to create an order with the following details:
  - Broker
  - Symbol
  - Order Type (assert it is only limit)
  - Price
  - Quantity
- OMS service handler workflow:
  1. Store order in the order database with status NEW
  2. Perform internal validation check (for now, do nothing)
     - If internal validation check passes:
       - Update the order's order_status field in the database to SENT and send order to mock broker via REST API
       - Read broker response on order status, which can be either FILL, PARTIAL_FILL, or REJECTION
       - Update the order's order_status field in the database to the response order status
     - If internal validation check fails: order status remains as NEW
  3. Update trades table
     - If order response is FILL or PARTIAL_FILL, update trades table with trade details from the broker API response

Feature 2: Mock Workflows
1. Order remains in NEW state
- User creates a new order in the UI for AAPL stock for IBKR
- This order should always remain in NEW state because it has failed the internal validation check

2. Order sent but rejected by broker
- User has an account balance of 1 million USD
- User creates a new order in the UI for DBS stock for IBKR at quantity = 1 million, which exceeds balance
- Mock broker API returns rejection message due to "insufficient balance"
- Update order status accordingly

3. Order sent and filled fully
- User creates a new order in the UI for DBS stock for IBKR that does not exceed the account balance threshold
- User receives a response for FILL
- User should be able to see updated order status and trade records in the UI

4. Order sent and partial fill
- User creates a new order in the UI for DBS stock for IBKR that does not exceed the account threshold
- User receives a response for partial fill
- User should be able to see updated order status and trade records in the UI

Feature 3: UI
- OMS page: User should be able to submit an order via a form based on the above workflow scenarios
- Orders/Trades view page: User should be able to view the current status of all orders and trades from the internal database







