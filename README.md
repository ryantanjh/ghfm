# Order Management System (OMS) Prototype

## Overview

This prototype demonstrates a simplified OMS workflow for a hedge fund. The system implements order validation, lifecycle management, simulated broker integration, and basic trade storage.

## Running the Prototype

```bash
./start.sh
```

This single command:
- Installs all required Python and Node.js dependencies
- Seeds the database with example data
- Starts the backend server on `http://localhost:8000`
- Starts the frontend UI on `http://localhost:3000`

## Order Lifecycle Workflow

### Prototype Implementation

1. **Order Creation**: User submits an order via the UI, which calls the backend REST API endpoint
2. **Database Logging**: Backend service creates an order record in the Orders table in the database with status `NEW`
3. **Internal Validation**: System performs pre-flight validation checks
   - **Pass**: Order status updated to `SENT` and forwarded to broker
   - **Fail**: Order remains in `NEW` state
4. **Broker Submission**: Order is sent to the broker
5. **Execution Response**: Broker returns execution status
   - Update order status to `REJECTED`, `FILLED`, or `PARTIAL_FILL`
   - Create trade records for filled/partial fills

### Mock Workflows

The prototype includes 4 demonstrable scenarios:

| Scenario | Trigger | Result |
|----------|---------|--------|
| **Validation Failure** | Symbol = `AAPL` | Order remains `NEW` (simulates failed internal checks) |
| **Broker Rejection** | Order value > $1,000,000 | Status = `REJECTED`, reason = "Insufficient balance" |
| **Full Fill** | Symbol = `DBS`, even quantity | Status = `FILLED`, trade record created |
| **Partial Fill** | Symbol = `DBS`, odd quantity | Status = `PARTIAL_FILL`, partial trade record created |

### Simplifications vs. Production

#### 1. Order Validation

**Prototype**: Order validation logic is simplified. Orders for symbol `AAPL` immediately fail validation and remain in `NEW` state. All other orders pass validation.

**Production**: Order validation involves comprehensive checks including risk limits, position constraints, and portfolio-level logic. Upon successful validation, the order is transmitted to the broker and status transitions from `NEW` to `SENT`.

#### 2. Order Status Updates (REST API vs. Persistent Connections)

**Prototype**: Order status is updated immediately based on the broker's REST API response (single request/response).

**Production Challenge**: REST API responses are insufficient for tracking partial fills. If an order is partially filled, we need to continue to listen for updates on when the remaining order is filled

**Production Solutions**:

1. **Continuous Polling**: Periodically query the broker's REST API to check order status and update internal records. This is inefficient and has latency issues.

2. **Persistent Connection (Recommended)**: Establish a live connection (WebSocket or FIX protocol) to receive real-time updates from the broker:
   - Broker sends execution reports as orders are filled
   - Example: An order filled in 3 chunks triggers 3 separate partial fill messages over the connection
   - Our system listens continuously and updates order/trade records in real-time
   - In FIX protocol, this is handled via Execution Report messages from the exchange

The prototype uses approach #1 (simulated single response) for simplicity, while production systems would implement approach #2 for real-time, event-driven updates.

## Architecture

```
Frontend (React)  →  Backend API (FastAPI)  →  Database (SQLite)
                             ↓
                       Broker Interface
                             ↓
                      Mock Broker (Simulated)
```

**Technology Stack**:
- **Frontend**: React.js with Ant Design UI components
- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Broker Integration**: Mock broker class (simulates REST API responses)

## Testing

```bash
python -m pytest api/tests/
```

The test suite includes:
- Unit tests for order service business logic
- Integration tests for all 4 mock workflow scenarios
- End-to-end verification of order and trade database records

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/send_limit_order` | Create new limit order |
| GET | `/orders` | Retrieve all orders |
| GET | `/trades` | Retrieve all trades |

---

## Design Choices

**Layered Architecture**: The backend separates business logic (services), data access (repositories), and API endpoints into distinct layers, enabling independent testing and easier maintenance.

**Repository Pattern**: Database operations are abstracted through a repository layer, allowing the underlying database implementation to be replaced without modifying business logic.

**Relational Database**: SQL databases support complex queries across orders and trades, and maintain referential integrity through foreign key constraints.

## Trade Reconciliation

**Prototype**: Trade records are created immediately upon order execution and stored in the database without external validation.

**Production**: Brokers typically send end-of-day (EOD) trade history reports. Production systems would:
- Schedule automated jobs to download EOD trade reports from brokers
- Compare broker-reported trades against internal database records
- Flag discrepancies for manual review (e.g., missing trades, mismatched quantities/prices)
- Generate reconciliation reports for compliance and audit purposes

## Trade File Generation for Prime Brokers and Fund Administrators

**Prototype**: The UI includes a trade report export feature that generates CSV files from internal trade records. Users can download complete trade history via the Trades page. This trade history is based on trades stored in the internal database.

**Production**: Trade files for prime brokers and fund administrators would be generated through scheduled cron jobs:
- Automated daily/monthly reports aggregating trade activity by broker, strategy, or account
- Position reconciliation reports comparing internal records against prime broker statements


## Production Scalability

**Prototype**: All historical orders and trades remain in the SQLite database indefinitely.

**Production**: As trade and order data accumulates over time, database growth requires strategic management:
- **Auto-scaling databases**: Cloud-hosted relational databases (RDS, Cloud SQL) can scale storage and compute automatically, but incur significant costs at scale
- **Data archival strategy**: Archive historical data (e.g., previous financial years) to low-cost storage solutions (S3, cold storage) while maintaining a lean operational database for active trading periods
- **Partitioning**: Implement time-based table partitioning to improve query performance and simplify archival processes

**Prototype**: Single SQLite database instance without backup mechanisms. Data is vulnerable to local disk corruption or hardware failure.

**Production**: Cloud database services (e.g., Amazon RDS, Google Cloud SQL) provide automated backup and point-in-time recovery capabilities to ensure data durability.

**Prototype**: Single mock broker implementation for testing order workflows.

**Production**: Multi-broker integration supporting portfolio manager selection at order creation. Each broker requires custom connectors due to varying API specifications and protocols.

