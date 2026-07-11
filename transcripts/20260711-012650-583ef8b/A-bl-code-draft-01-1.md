# First-pass metrics client

```python
from dataclasses import dataclass
from typing import Optional
import time
import requests


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    endpoint: str
    api_key: str
    timeout: float = 5.0
    batch_size: int = 100
    flush_interval: float = 10.0


class MetricsClient:
    """HTTP client for submitting counters and timings to the metrics API."""

    def __init__(self, config: MetricsConfig):
        self.config = config
        self._pending: list[dict] = []
        self._last_flush = time.time()

    def counter(self, name: str, value: int = 1, tags: Optional[dict] = None) -> None:
        """Record a counter metric."""
        self._add_metric({
            "type": "counter",
            "name": name,
            "value": value,
            "tags": tags or {},
            "timestamp": time.time(),
        })

    def timing(self, name: str, milliseconds: float, tags: Optional[dict] = None) -> None:
        """Record a timing metric in milliseconds."""
        self._add_metric({
            "type": "timing",
            "name": name,
            "value": milliseconds,
            "tags": tags or {},
            "timestamp": time.time(),
        })

    def _add_metric(self, metric: dict) -> None:
        """Add a metric to the batch and flush if needed."""
        self._pending.append(metric)
        
        should_flush = (
            len(self._pending) >= self.config.batch_size
            or (time.time() - self._last_flush) >= self.config.flush_interval
        )
        if should_flush:
            self.flush()

    def flush(self) -> None:
        """Send all pending metrics to the API."""
        if not self._pending:
            return

        try:
            response = requests.post(
                f"{self.config.endpoint}/metrics",
                json={"metrics": self._pending},
                headers={"Authorization": f"Bearer {self.config.api_key}"},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # TODO: add proper logging & retry strategy
            print(f"Failed to flush metrics: {e}")
        finally:
            self._pending.clear()
            self._last_flush = time.time()


# Example usage
if __name__ == "__main__":
    config = MetricsConfig(
        endpoint="https://metrics.internal.example.com",
        api_key="secret-key-123",
    )
    client = MetricsClient(config)

    # Track requests
    client.counter("http_requests", tags={"endpoint": "/api/users", "status": 200})
    
    # Track timing
    client.timing("db_query_ms", 45.2, tags={"query": "select_users"})

    # Explicit flush
    client.flush()
```

**Shape & design notes:**

- **Config object** — single source of truth for credentials/behavior
- **Two metric types** — simple `counter()` and `timing()` methods with optional tags
- **Auto-batching** — flushes on size or time threshold
- **Error handling stub** — requests exceptions caught, but needs real logging/retry logic
- **Clear timestamp semantics** — captured at record time, not flush time

**Things to test/iterate on:**
- Does the JSON payload shape match your API's expectations?
- Should timing accept seconds instead of ms?
- Need context manager / async support?
- Should failed flushes drop metrics or persist them?