# Internal Metrics API Client

Here's a clean, testable first pass:

```python
import time
import requests
from typing import Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass, asdict


@dataclass
class MetricPayload:
    """Shape of a single metric submission"""
    name: str
    value: float
    type: str  # "counter" or "timing"
    tags: Dict[str, str]
    timestamp: float


class MetricsClient:
    """Client for internal metrics API"""
    
    def __init__(self, base_url: str, default_tags: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")
        self.default_tags = default_tags or {}
        self.session = requests.Session()
    
    def counter(self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric"""
        self._submit_metric(name, value, "counter", tags)
    
    def timing(self, name: str, milliseconds: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a timing metric in milliseconds"""
        self._submit_metric(name, milliseconds, "timing", tags)
    
    @contextmanager
    def timer(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for automatic timing"""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.timing(name, elapsed_ms, tags)
    
    def _submit_metric(self, name: str, value: float, metric_type: str, tags: Optional[Dict[str, str]] = None) -> None:
        """Submit a single metric (internal)"""
        merged_tags = {**self.default_tags, **(tags or {})}
        
        payload = MetricPayload(
            name=name,
            value=value,
            type=metric_type,
            tags=merged_tags,
            timestamp=time.time()
        )
        
        try:
            response = self.session.post(
                f"{self.base_url}/metrics",
                json=asdict(payload),
                timeout=2.0
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Don't crash the app over metrics; log and continue
            print(f"Failed to submit metric '{name}': {e}")
    
    def close(self):
        """Clean up session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
```

## Example usage:

```python
# Basic setup
client = MetricsClient("http://localhost:8000", default_tags={"service": "auth"})

# Counters
client.counter("login_attempts")
client.counter("failed_login", tags={"reason": "invalid_password"})

# Manual timings
client.timing("db_query", 45.2, tags={"query": "users"})

# Auto-timing with context manager
with client.timer("api_request", tags={"endpoint": "/users"}):
    # do work
    pass

# Context manager for resource cleanup
with MetricsClient("http://localhost:8000") as client:
    client.counter("requests")
```

## Shape notes:

- **Payload structure**: Clean dataclass for JSON serialization
- **Default tags**: Baked in at init; overridable per-call
- **Timing**: Always milliseconds (more intuitive than seconds)
- **Timer context**: Automatic elapsed calculation with `perf_counter()`
- **Error handling**: Graceful degradation (metrics failures don't break app)
- **Resource cleanup**: Works with context managers

Test away—what aspects would you want to adjust?