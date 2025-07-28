from prometheus_client import Counter, Gauge

messages_total = Counter(
    "websocket_messages_total",
    "Total number of WebSocket messages received"
)

active_connections = Gauge(
    "websocket_active_connections",
    "Number of active WebSocket connections"
)

errors_total = Counter(
    "websocket_errors_total",
    "Number of WebSocket disconnections with non-1001 code"
)

last_shutdown_ts = Gauge(
    "websocket_last_shutdown_timestamp_seconds",
    "Timestamp of last graceful shutdown"
)