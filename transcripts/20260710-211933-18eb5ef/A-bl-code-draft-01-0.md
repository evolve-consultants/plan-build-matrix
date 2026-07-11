# Internal Metrics API Client

```python
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import requests
import time


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    base_url: str
    api_key: str
    timeout: int = 5
    batch_size: int = 100
    flush_interval: int = 10  # seconds


class MetricsClient:
    """Client for pushing counters and timings to internal metrics API."""

    def __init__(self, config: MetricsConfig):
        self.config = config
        self._batch: list[Dict[str, Any]] = []
        self._last_flush = time.time()

    def counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric.
        
        Args:
            name: Metric name (e.g., "requests_total")
            value: Amount to increment by (default: 1)
            tags: Optional dict of tag name/value pairs
        """
        self._add_metric("counter", name, value, tags)

    def timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a timing metric in milliseconds.
        
        Args:
            name: Metric name (e.g., "request_duration")
            duration_ms: Duration in milliseconds
            tags: Optional dict of tag name/value pairs
        """
        self._add_metric("timing", name, duration_ms, tags)

    def _add_metric(self, metric_type: str, name: str, value: float, tags: Optional[Dict[str, str]]) -> None:
        """Add a metric to the batch queue."""
        metric = {
            "type": metric_type,
            "name": name,
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "tags": tags or {},
        }
        self._batch.append(metric)
        
        # Auto-flush if batch is full or interval elapsed
        if self._should_flush():
            self.flush()

    def _should_flush(self) -> bool:
        """Check if batch should be flushed."""
        batch_full = len(self._batch) >= self.config.batch_size
        interval_elapsed = time.time() - self._last_flush >= self.config.flush_interval
        return batch_full or (interval_elapsed and self._batch)

    def flush(self) -> None:
        """Send all batched metrics to the API."""
        if not self._batch:
            return

        payload = {"metrics": self._batch}
        
        try:
            response = requests.post(
                f"{self.config.base_url}/metrics",
                json=payload,
                headers={"Authorization": f"Bearer {self.config.api_key}"},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            self._batch.clear()
            self._last_flush = time.time()
        except requests.RequestException as e:
            # TODO: Add proper logging and retry logic
            print(f"Failed to flush metrics: {e}")

    def close(self) -> None:
        """Flush any remaining metrics and close the client."""
        self.flush()
```

## Usage Example

```python
# Setup
config = MetricsConfig(
    base_url="https://metrics.internal.example.com",
    api_key="sk_test_..."
)
client = MetricsClient(config)

# Record metrics
client.counter("user_signups", tags={"source": "web"})
client.counter("errors_total", value=3, tags={"service": "api"})
client.timing("db_query_duration", duration_ms=42.5, tags={"query": "users"})

# Flush when done
client.close()
```

---

**Shape notes for your review:**
- Batching with configurable thresholds (flush on size OR interval)
- Separate `counter()` and `timing()` methods (explicit over implicit)
- Optional `tags` dict for dimensions/labels
- Simple POST payload with timestamp included
- Graceful `flush()` and `close()` for cleanup

What's your API's expected request/response shape? I can adjust the payload structure.