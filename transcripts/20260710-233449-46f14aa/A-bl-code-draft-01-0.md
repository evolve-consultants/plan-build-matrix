# First-pass metrics client

```python
import time
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    endpoint: str
    api_key: str
    timeout: float = 5.0
    batch_size: int = 100
    auto_flush_interval: float = 30.0


class MetricsClient:
    """
    HTTP client for sending counters and timings to the metrics API.
    
    Usage:
        client = MetricsClient(
            endpoint="https://metrics.internal/v1",
            api_key="secret_key"
        )
        client.counter("requests.total", 1, tags={"endpoint": "/users"})
        with client.timer("db.query.duration", tags={"query": "users"}):
            # do work
            pass
        client.flush()
    """

    def __init__(self, endpoint: str, api_key: str, **kwargs):
        self.config = MetricsConfig(endpoint=endpoint, api_key=api_key, **kwargs)
        self._buffer: list[Dict[str, Any]] = []
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        })

    def counter(self, name: str, value: float = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        self._add_metric("counter", name, value, tags)

    def timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a timing metric (duration in milliseconds)."""
        self._add_metric("timing", name, duration_ms, tags)

    @contextmanager
    def timer(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for measuring block execution time."""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.timing(name, elapsed_ms, tags)

    def _add_metric(self, metric_type: str, name: str, value: float, tags: Optional[Dict[str, str]]) -> None:
        """Buffer a metric for batch submission."""
        metric = {
            "type": metric_type,
            "name": name,
            "value": value,
            "timestamp": time.time(),
            "tags": tags or {}
        }
        self._buffer.append(metric)

        if len(self._buffer) >= self.config.batch_size:
            self.flush()

    def flush(self) -> None:
        """Send all buffered metrics to the API."""
        if not self._buffer:
            return

        payload = {"metrics": self._buffer}
        
        try:
            response = self._session.post(
                f"{self.config.endpoint}/metrics",
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # TODO: add logging/retry strategy
            raise MetricsClientError(f"Failed to flush metrics: {e}") from e
        finally:
            self._buffer.clear()

    def close(self) -> None:
        """Clean up resources."""
        self.flush()
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class MetricsClientError(Exception):
    """Raised when the metrics client encounters an error."""
    pass
```

## Key design choices to discuss:

- **Buffering**: Metrics batch before sending (configurable size/interval)
- **Context manager**: `timer()` for ergonomic timing blocks
- **Tags/labels**: Attached to individual metrics for filtering
- **Type hints**: Ready for mypy validation
- **Session reuse**: Uses `requests.Session` for connection pooling
- **Simple API**: `counter()`, `timing()`, `timer()` are the main surfaces

## Testing surface I've left for you:

- Error handling (what happens on network failures?)
- Should `flush()` be automatic on timer exit?
- Tag validation/sanitization needed?
- Do you want metric name validation (regex)?
- Async variant needed?

What behavior would you want to add or change?