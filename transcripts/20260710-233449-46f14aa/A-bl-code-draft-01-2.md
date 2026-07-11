# Metrics API Client (First Pass)

```python
import time
import requests
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class MetricType(Enum):
    COUNTER = "counter"
    TIMING = "timing"


@dataclass
class Metric:
    """Represents a single metric data point."""
    name: str
    value: float
    metric_type: MetricType
    tags: Optional[dict] = None
    timestamp: Optional[float] = None


class MetricsClient:
    """Client for posting counters and timings to internal metrics API."""
    
    def __init__(self, api_url: str, api_key: str, timeout: int = 5):
        """
        Initialize the metrics client.
        
        Args:
            api_url: Base URL of the metrics API (e.g., "https://metrics.internal/api")
            api_key: API authentication key
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def counter(self, name: str, value: float = 1.0, tags: Optional[dict] = None) -> None:
        """
        Record a counter metric.
        
        Args:
            name: Metric name (e.g., "requests.total")
            value: Counter increment (default: 1.0)
            tags: Optional dict of tags for filtering/grouping
        """
        metric = Metric(
            name=name,
            value=value,
            metric_type=MetricType.COUNTER,
            tags=tags
        )
        self._send(metric)
    
    def timing(self, name: str, duration_ms: float, tags: Optional[dict] = None) -> None:
        """
        Record a timing metric.
        
        Args:
            name: Metric name (e.g., "db.query.time")
            duration_ms: Duration in milliseconds
            tags: Optional dict of tags
        """
        metric = Metric(
            name=name,
            value=duration_ms,
            metric_type=MetricType.TIMING,
            tags=tags
        )
        self._send(metric)
    
    def timing_context(self, name: str, tags: Optional[dict] = None):
        """
        Context manager for automatic timing measurement.
        
        Usage:
            with metrics.timing_context("request.duration", tags={"endpoint": "/api/users"}):
                # do work
        """
        return _TimingContext(self, name, tags)
    
    def _send(self, metric: Metric) -> None:
        """Send a metric to the API."""
        payload = {
            "name": metric.name,
            "value": metric.value,
            "type": metric.metric_type.value,
            "tags": metric.tags or {},
            "timestamp": metric.timestamp or time.time()
        }
        
        try:
            response = self._session.post(
                f"{self.api_url}/metrics",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Fail silently to avoid breaking app behavior
            # Consider logging this
            pass


class _TimingContext:
    """Context manager for timing code blocks."""
    
    def __init__(self, client: MetricsClient, name: str, tags: Optional[dict] = None):
        self.client = client
        self.name = name
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        duration_ms = (time.time() - self.start_time) * 1000
        self.client.timing(self.name, duration_ms, self.tags)
```

## Usage Examples

```python
# Initialize
metrics = MetricsClient(
    api_url="https://metrics.internal/api",
    api_key="secret-key-123"
)

# Simple counter
metrics.counter("user.signups")
metrics.counter("payment.errors", value=5.0)

# Counter with tags
metrics.counter("http.requests", tags={"method": "POST", "status": "200"})

# Timing (explicit)
metrics.timing("db.query.duration", duration_ms=145.2)

# Timing (context manager)
with metrics.timing_context("api.endpoint", tags={"endpoint": "/users"}):
    # some operation
    time.sleep(0.1)
```

---

**Design choices for feedback:**
- Fail-silent on network errors (won't crash your app)
- Context manager for cleaner timing code
- Tags as optional dicts (flexible filtering)
- Session reuse for efficiency
- Simple, flat interface (easy to test and extend)

What's your take on the shape? Would you change how metrics are structured, or the method signatures?