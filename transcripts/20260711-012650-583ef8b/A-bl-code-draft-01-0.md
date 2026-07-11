# Internal Metrics API Client

Here's a straightforward first pass:

```python
import time
import requests
from typing import Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    endpoint: str
    api_key: str
    timeout: float = 5.0
    batch_size: int = 100
    flush_interval: float = 10.0


class MetricsClient:
    """Client for sending counters and timings to the metrics API."""
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self._queue: list[Dict[str, Any]] = []
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    
    def increment(self, metric: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a counter increment.
        
        Args:
            metric: The counter name (e.g., "requests.total")
            value: Amount to increment by (default: 1)
            tags: Optional dict of tag key-value pairs
        """
        self._enqueue({
            "type": "counter",
            "metric": metric,
            "value": value,
            "tags": tags or {}
        })
    
    def timing(self, metric: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a timing measurement.
        
        Args:
            metric: The timing name (e.g., "request.duration")
            duration_ms: Duration in milliseconds
            tags: Optional dict of tag key-value pairs
        """
        self._enqueue({
            "type": "timing",
            "metric": metric,
            "value": duration_ms,
            "tags": tags or {}
        })
    
    @contextmanager
    def timer(self, metric: str, tags: Optional[Dict[str, str]] = None):
        """
        Context manager for automatic timing.
        
        Usage:
            with client.timer("db.query", tags={"table": "users"}):
                # do work
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.timing(metric, elapsed_ms, tags)
    
    def _enqueue(self, event: Dict[str, Any]) -> None:
        """Queue an event for batched sending."""
        self._queue.append(event)
        if len(self._queue) >= self.config.batch_size:
            self.flush()
    
    def flush(self) -> None:
        """Send all queued metrics to the API."""
        if not self._queue:
            return
        
        payload = {"events": self._queue}
        try:
            response = self._session.post(
                self.config.endpoint,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            self._queue.clear()
        except requests.RequestException as e:
            # In production, you'd probably log this and maybe retry
            print(f"Failed to flush metrics: {e}")
    
    def close(self) -> None:
        """Flush any remaining metrics and close the session."""
        self.flush()
        self._session.close()
```

## Quick Usage Example

```python
config = MetricsConfig(
    endpoint="https://metrics.internal/api/v1/ingest",
    api_key="secret-key-123"
)
client = MetricsClient(config)

# Counter
client.increment("api.requests", tags={"endpoint": "/users"})
client.increment("api.errors", value=2, tags={"status": "500"})

# Manual timing
client.timing("db.query", duration_ms=45.2, tags={"query": "SELECT *"})

# Context manager timing
with client.timer("cache.lookup", tags={"cache": "redis"}):
    time.sleep(0.1)

# Explicit flush (automatic at batch_size)
client.flush()

# Cleanup
client.close()
```

## Design Notes

- **Config object**: Grouping settings makes it testable and reusable
- **Tags over kwargs**: Explicit dict keeps the API clean and extensible
- **Batching**: Queues events to reduce HTTP overhead
- **Context manager**: Natural syntax for timing blocks
- **perf_counter**: Higher resolution than time.time()
- **Session reuse**: Single requests.Session for connection pooling
- **Minimal error handling**: Left intentionally simple—you'll want to add logging/retry logic based on your needs

What would you like to adjust? (error handling strategy, retry logic, async support, tag validation, etc.)