# First-pass metrics API client

```python
import time
import requests
from dataclasses import dataclass
from typing import Optional
from contextlib import contextmanager


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    endpoint: str
    api_key: str
    timeout: float = 5.0
    batch_size: int = 100


class MetricsClient:
    """Client for sending counters and timings to the internal metrics API."""
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self._buffer: list[dict] = []
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    
    def increment(self, metric: str, value: int = 1, tags: Optional[dict] = None) -> None:
        """Increment a counter metric.
        
        Args:
            metric: Name of the counter (e.g., "requests.processed")
            value: Amount to increment by
            tags: Optional key-value tags (e.g., {"service": "api", "status": "200"})
        """
        self._buffer.append({
            "type": "counter",
            "name": metric,
            "value": value,
            "tags": tags or {},
            "timestamp": time.time(),
        })
        self._maybe_flush()
    
    def timing(self, metric: str, duration_ms: float, tags: Optional[dict] = None) -> None:
        """Record a timing metric in milliseconds.
        
        Args:
            metric: Name of the timing (e.g., "db.query.duration")
            duration_ms: Duration in milliseconds
            tags: Optional key-value tags
        """
        self._buffer.append({
            "type": "timing",
            "name": metric,
            "value": duration_ms,
            "tags": tags or {},
            "timestamp": time.time(),
        })
        self._maybe_flush()
    
    @contextmanager
    def timer(self, metric: str, tags: Optional[dict] = None):
        """Context manager for timing a code block.
        
        Usage:
            with client.timer("request.duration", tags={"endpoint": "/users"}):
                # do work
        """
        start = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start) * 1000
            self.timing(metric, duration_ms, tags)
    
    def flush(self) -> bool:
        """Explicitly flush buffered metrics.
        
        Returns:
            True if successful, False otherwise.
        """
        if not self._buffer:
            return True
        
        payload = {"metrics": self._buffer}
        try:
            resp = self._session.post(
                self.config.endpoint,
                json=payload,
                timeout=self.config.timeout,
            )
            resp.raise_for_status()
            self._buffer.clear()
            return True
        except requests.RequestException as e:
            # Log or handle error; keep buffer for retry
            print(f"Failed to flush metrics: {e}")
            return False
    
    def _maybe_flush(self) -> None:
        """Auto-flush if buffer reaches batch size."""
        if len(self._buffer) >= self.config.batch_size:
            self.flush()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.flush()
        self._session.close()
```

## Quick usage example:

```python
config = MetricsConfig(
    endpoint="https://metrics.internal/api/v1/metrics",
    api_key="secret-key-123",
)

with MetricsClient(config) as client:
    client.increment("requests.received", tags={"service": "checkout"})
    
    with client.timer("payment.processing", tags={"provider": "stripe"}):
        # process payment
        time.sleep(0.5)
    
    client.flush()
```

---

**Things to react to:**
- **Batch buffering**: Auto-flushes at `batch_size`, explicit `flush()` available
- **Context manager support**: Both for the client lifecycle and timing blocks
- **Tags/metadata**: Dict-based for flexibility
- **Timing in milliseconds**: Common convention, easier to reason about
- **Error handling**: Swallows network errors (adjust as needed—silent drop, retry queue, exceptions, etc.)

What aspects would you like to adjust?