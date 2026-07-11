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
    timeout: int = 5
    batch_size: int = 10


class MetricsClient:
    """Client for posting counters and timings to internal metrics API."""
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self._buffer = []
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    
    def increment(self, metric_name: str, value: int = 1, tags: Optional[dict] = None) -> None:
        """Increment a counter metric."""
        self._buffer_metric("counter", metric_name, value, tags)
    
    def timing(self, metric_name: str, milliseconds: float, tags: Optional[dict] = None) -> None:
        """Record a timing metric in milliseconds."""
        self._buffer_metric("timing", metric_name, milliseconds, tags)
    
    @contextmanager
    def timer(self, metric_name: str, tags: Optional[dict] = None):
        """Context manager for timing a code block."""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.timing(metric_name, elapsed_ms, tags)
    
    def _buffer_metric(self, metric_type: str, name: str, value: float, tags: Optional[dict] = None) -> None:
        """Add metric to buffer, flush if needed."""
        self._buffer.append({
            "type": metric_type,
            "name": name,
            "value": value,
            "tags": tags or {}
        })
        
        if len(self._buffer) >= self.config.batch_size:
            self.flush()
    
    def flush(self) -> None:
        """Send buffered metrics to API."""
        if not self._buffer:
            return
        
        payload = {"metrics": self._buffer}
        try:
            response = self._session.post(
                self.config.endpoint,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            self._buffer.clear()
        except requests.RequestException as e:
            # Log but don't raise - metrics shouldn't break the app
            print(f"Failed to flush metrics: {e}")
    
    def close(self) -> None:
        """Flush and close the session."""
        self.flush()
        self._session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# Usage example
if __name__ == "__main__":
    config = MetricsConfig(
        endpoint="https://metrics.internal/api/v1/metrics",
        api_key="your-api-key"
    )
    
    with MetricsClient(config) as client:
        # Counter
        client.increment("requests.total", tags={"endpoint": "/api/users"})
        
        # Timing
        client.timing("db.query.time", 42.5, tags={"query": "users"})
        
        # Timer context manager
        with client.timer("process.duration", tags={"job": "cleanup"}):
            time.sleep(0.1)
        
        # Explicit flush (also happens on exit)
        client.flush()
```

## Key design decisions:

- **Config object** — easier to test, pass around, extend
- **Buffering** — batches metrics before sending (configurable batch size)
- **Context manager** (`timer`) — common pattern for timing operations
- **Silent failures** — metrics issues won't crash your app
- **Tags as dict** — flexible, mimics common metrics libraries
- **Session reuse** — HTTP connection pooling
- **Context manager for client** — ensures flush on exit

What would you want to stress-test first? Error handling, concurrent access, or something else?