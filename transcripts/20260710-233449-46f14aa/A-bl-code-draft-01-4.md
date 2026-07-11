# First-pass metrics client

```python
import requests
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class MetricsConfig:
    """Configuration for the metrics client."""
    base_url: str
    api_key: str
    timeout: float = 10.0
    batch_size: int = 100


class MetricsClient:
    """Client for submitting metrics (counters and timings) to internal metrics API."""
    
    def __init__(self, config: MetricsConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {config.api_key}"})
        self._buffer: list[Dict[str, Any]] = []
    
    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """Submit a counter increment."""
        self._buffer.append({
            "type": "counter",
            "name": metric_name,
            "value": value,
            "tags": tags or {},
            "timestamp": time.time(),
        })
        self._flush_if_needed()
    
    def timing(self, metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Submit a timing measurement in milliseconds."""
        self._buffer.append({
            "type": "timing",
            "name": metric_name,
            "value": duration_ms,
            "tags": tags or {},
            "timestamp": time.time(),
        })
        self._flush_if_needed()
    
    @contextmanager
    def timer(self, metric_name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for automatic timing measurement."""
        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self.timing(metric_name, duration_ms, tags)
    
    def flush(self) -> None:
        """Manually flush buffered metrics."""
        if not self._buffer:
            return
        
        batch = self._buffer[: self.config.batch_size]
        self._buffer = self._buffer[self.config.batch_size :]
        
        try:
            response = self.session.post(
                f"{self.config.base_url}/metrics",
                json={"metrics": batch},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Re-buffer on failure (simple approach)
            self._buffer = batch + self._buffer
            raise
    
    def _flush_if_needed(self) -> None:
        """Auto-flush if buffer reaches batch size."""
        if len(self._buffer) >= self.config.batch_size:
            self.flush()
    
    def close(self) -> None:
        """Flush remaining metrics and close session."""
        self.flush()
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
```

## Usage examples:

```python
# Basic setup
config = MetricsConfig(base_url="https://metrics.internal", api_key="secret-key")
client = MetricsClient(config)

# Simple counters
client.increment("requests.total")
client.increment("errors.count", value=2, tags={"error_type": "timeout"})

# Direct timing
client.timing("database.query_ms", duration_ms=45.2, tags={"query": "user_select"})

# Context manager timing
with client.timer("api.handler_ms", tags={"endpoint": "/users"}):
    # your code here
    pass

# Manual flush or context manager cleanup
client.flush()
# or use: with MetricsClient(config) as client: ...
```

**Design notes:**
- Buffering + batch API calls (configurable batch size)
- Simple tag support for cardinality
- `perf_counter()` for timing accuracy
- Context manager for both client and timer
- Minimal error handling (you'll want to expand on retry/deadletter strategy)
- Config object for easy testability

What would you like to adjust on the interface or behavior?