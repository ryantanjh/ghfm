Order lifecycle workflow

1. User creates an order in the UI, sends order to backend REST API endpoint
2. Backend service logs order in database with status NEW
3. Service does pre-flight validation check: If validation check passes, then order is sent to exchange
* In production, one workflow is that a PM enters a NEW order, but we only want to send it after certain conditions and internal checks pass
In this case, an order can remain in NEW state until it gets cancelled by manager, or when it gets executed. 
To implement this, We need a background worker to continuously poll the database for NEW orders, and validate them before sending the order to the exchange
However in the mock workflow for simplicaity purposes, we just automatically assume that when symbol is AAPL, it fails the internal validation check and remains in NEW statte
4. Order is sent to broker, update order status to sent
5. Wait for response from broker: 
- update order status to failure, fill, or partial fill
- if broker response is fill or partial fill, we also update our internal trade records with the trade
* in production, we cannot update our internal order status records based on the rest api order response of the broker due to partial fills
* for example, if we send a limit order via rest api and its response says it is partial filled, how would we know when the rest is filled? 
* 2 ways: 
1. If we want to use REST API, we continously poll the broker's REST API to check on the status of each order we went, and updating our internal db 
2. We open a live connection (typically websocket or FIX) where we listen for updates from the exchange on updates to our order
For example, if our order is broken down into 3 partial fills, the exchange would send 3 updates via this socket connection, and our system should
listen to this connection and update the internal records accordingly. In FIX protocol this is done via the Execution report message from the exchange. 
Our system will listen for these messages and update our internal order and trade records accordingly




    