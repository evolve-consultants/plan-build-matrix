# Internal Metrics API Client

```python
import time
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class MetricType(Enum):
    COUNTER = "counter"
    TIMING = "timing"


@dataclass
class Metric:
    name: str
    value: float
    type: MetricType
    tags: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "type": self.type.value,
            "tags": self.tags or {},
        }


class MetricsClient:
    def __init__(
        self,
        endpoint: str,
        api_key: Optional[str] = None,
        batch_size: int = 10,
        timeout: float = 5.0,
    ):
        """
        Args:
            endpoint: Base URL of the metrics API (e.g., http://localhost:8080/metrics)
            api_key: Optional API key for authentication
            batch_size: Number of metrics to accumulate before sending
            timeout: HTTP request timeout in seconds
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.batch_size = batch_size
        self.timeout = timeout
        self._buffer: list[Metric] = []
        self._headers = {"Content-Type": "application/json"}
        if api_key:
            self._headers["Authorization"] = f"Bearer {api_key}"

    def counter(
        self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a counter metric."""
        self._add_metric(Metric(name, value, MetricType.COUNTER, tags))

    def timing(
        self, name: str, milliseconds: float, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Record a timing metric (in milliseconds)."""
        self._add_metric(Metric(name, milliseconds, MetricType.TIMING, tags))

    def _add_metric(self, metric: Metric) -> None:
        """Buffer a metric and flush if batch is full."""
        self._buffer.append(metric)
        if len(self._buffer) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        """Send all buffered metrics to the API."""
        if not self._buffer:
            return

        payload = {"metrics": [m.to_dict() for m in self._buffer]}
        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=self._headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Silently fail; production code should log this
            print(f"Failed to send metrics: {e}")
        finally:
            self._buffer.clear()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.flush()


# Context manager for timing blocks
class Timer:
    def __init__(self, client: MetricsClient, name: str, tags: Optional[Dict[str, str]] = None):
        self.client = client
        self.name = name
        self.tags = tags
        self.start_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        elapsed_ms = (time.time() - self.start_time) * 1000
        self.client.timing(self.name, elapsed_ms, self.tags)
```

## Usage Examples

```python
# Basic usage
client = MetricsClient("http://localhost:8080/metrics", api_key="secret123")

client.counter("user_signup")
client.counter("api_requests", value=5, tags={"endpoint": "/users"})
client.timing("db_query", milliseconds=145.3, tags={"query": "users_select"})

client.flush()  # Send immediately

# Auto-flush with context manager
with MetricsClient("http://localhost:8080/metrics") as client:
    client.counter("session_start")
    client.counter("api_calls", value=3)
    # Flushes automatically on exit

# Time a code block
with Timer(client, "request_handler", tags={"handler": "login"}):
    # ... do work
    pass
```

---

**Design notes:**

- **Batching**: Metrics accumulate and send when `batch_size` is reached, or call `flush()` explicitly
- **Tags**: Optional dictionary for dimensionality (endpoint, handler, etc.)
- **Timing units**: Milliseconds (easier to reason about than seconds)
- **Error handling**: Silent failures; add logging in production
- **Context managers**: Both for client (auto-flush) and Timer (convenience)

What would you change about the API shape?