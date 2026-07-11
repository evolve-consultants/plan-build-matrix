**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
You want a draft Python client for posting metrics (counters and timings) to an internal HTTP API. You'll verify behavior yourself, so I should focus on interface design, naming clarity, and structural fit rather than defensive error handling or extensive docs.

<assumptions>
  <project>Internal metrics API; HTTP-based; accepts at minimum counters and timing data</project>
  <task>Need a usable client class to react to — shape and naming matter more than completeness right now</task>
  <operator>You own testing and integration; you'll give feedback on what fits your codebase style</operator>
</assumptions>

### What I'm unsure of
- Whether you batch submissions or fire individual metrics immediately
- Expected metric names/tags structure (flat dict, hierarchical, tags as separate arg?)
- Whether the API endpoint and auth are injected at init or class-level config

### Here's a rough draft (Option A)

```python
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any
import requests


@dataclass
class Metric:
    """Single metric submission."""
    name: str
    value: float
    metric_type: str  # "counter" or "timing"
    tags: Optional[Dict[str, str]] = None
    timestamp: Optional[float] = None


class MetricsClient:
    """Client for submitting metrics to internal metrics API."""
    
    def __init__(self, endpoint: str, timeout: float = 5.0):
        """
        Args:
            endpoint: Base URL of metrics API (e.g., http://metrics.internal/api/v1)
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.timeout = timeout
    
    def counter(self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None) -> None:
        """Submit a counter metric."""
        self._submit(name=name, value=value, metric_type="counter", tags=tags)
    
    def timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Submit a timing metric.
        
        Args:
            name: Metric name
            duration_ms: Duration in milliseconds
            tags: Optional labels
        """
        self._submit(name=name, value=duration_ms, metric_type="timing", tags=tags)
    
    def timing_context(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for timing a block of code."""
        return _TimingContext(self, name, tags)
    
    def _submit(self, name: str, value: float, metric_type: str, tags: Optional[Dict[str, str]] = None) -> None:
        """Internal: post a single metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            tags=tags or {},
            timestamp=time.time()
        )
        payload = {
            "name": metric.name,
            "value": metric.value,
            "type": metric.metric_type,
            "tags": metric.tags,
            "timestamp": metric.timestamp,
        }
        requests.post(f"{self.endpoint}/metrics", json=payload, timeout=self.timeout)


class _TimingContext:
    """Context manager for timing code blocks."""
    
    def __init__(self, client: MetricsClient, name: str, tags: Optional[Dict[str, str]]):
        self.client = client
        self.name = name
        self.tags = tags
        self.start_time: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        elapsed_ms = (time.time() - self.start_time) * 1000
        self.client.timing(self.name, elapsed_ms, tags=self.tags)
```

**Usage sketch:**
```python
client = MetricsClient(endpoint="http://localhost:8080/api/v1")

# Direct submission
client.counter("requests.total", value=1, tags={"endpoint": "/health"})
client.timing("query.duration", duration_ms=42.5, tags={"query": "users"})

# Context manager
with client.timing_context("request.time", tags={"handler": "fetch_data"}):
    # do work
    pass
```

### Alternatives I considered

- **B (Batching)**: Accumulate metrics in-memory and flush on demand or timer. Better for high-volume scenarios but adds complexity. Pick this if you're sending hundreds of metrics per second.
- **C (Async)**: Use `httpx` or `aiohttp` for non-blocking submission. Pick this if metrics posting can't block the hot path.

### Next prompt should include
- Reactions to naming (`counter()` vs `increment()`? `timing()` vs `record_duration()`?)
- Whether batching or async matters for your use case
- What the actual API payload shape expects (does it match this, or different structure?)
- Any auth requirement I should bake in