# MetricsClient sketch

```python
from dataclasses import dataclass
from typing import Optional
import time
import requests


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    base_url: str
    api_key: str
    timeout: float = 5.0
    batch_size: int = 100


class MetricsClient:
    """Client for sending counters and timings to the internal metrics API."""
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {config.api_key}"})
    
    def counter(self, name: str, value: int = 1, tags: Optional[dict] = None) -> None:
        """
        Increment a counter metric.
        
        Args:
            name: Metric name (e.g., "requests.total")
            value: Amount to increment by (default: 1)
            tags: Optional dict of tags/labels
        """
        self._send_metric("counter", name, value, tags)
    
    def timing(self, name: str, milliseconds: float, tags: Optional[dict] = None) -> None:
        """
        Record a timing metric.
        
        Args:
            name: Metric name (e.g., "request.duration")
            milliseconds: Duration in milliseconds
            tags: Optional dict of tags/labels
        """
        self._send_metric("timing", name, milliseconds, tags)
    
    def time_it(self, name: str, tags: Optional[dict] = None):
        """
        Context manager for timing a block of code.
        
        Usage:
            with client.time_it("db.query", tags={"table": "users"}):
                # do work
        """
        class Timer:
            def __enter__(inner_self):
                inner_self.start = time.perf_counter()
                return inner_self
            
            def __exit__(inner_self, *args):
                elapsed_ms = (time.perf_counter() - inner_self.start) * 1000
                self.timing(name, elapsed_ms, tags)
        
        return Timer()
    
    def _send_metric(self, metric_type: str, name: str, value: float, 
                     tags: Optional[dict] = None) -> None:
        """Send a single metric to the API."""
        payload = {
            "type": metric_type,
            "name": name,
            "value": value,
            "tags": tags or {},
        }
        
        try:
            response = self._session.post(
                f"{self.config.base_url}/metrics",
                json=payload,
                timeout=self.config.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Silently fail for now - metrics shouldn't crash the app
            print(f"Failed to send metric {name}: {e}")
    
    def close(self) -> None:
        """Close the underlying session."""
        self._session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# Usage example
if __name__ == "__main__":
    config = MetricsConfig(
        base_url="https://metrics.internal.example.com",
        api_key="sk-test-xxx"
    )
    
    with MetricsClient(config) as client:
        client.counter("app.startup")
        client.counter("requests.processed", value=42, tags={"endpoint": "/api/users"})
        
        with client.time_it("database.query", tags={"query": "select_users"}):
            time.sleep(0.1)  # simulate work
```

**Design notes:**
- **Config object** separates credentials/settings from runtime behavior
- **Simple naming**: `counter()`, `timing()`, `time_it()` are self-documenting
- **Tags as dict**: flexible, works with most backends (Prometheus, DataDog, etc.)
- **Context manager**: both class-level (connection mgmt) and method-level (timing)
- **Silent failure**: metrics are observability infrastructure—don't take down the app
- **Session reuse**: HTTP connection pooling for efficiency

What'd you change on first read?