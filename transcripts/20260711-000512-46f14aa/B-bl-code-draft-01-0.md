**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
You said you'll test behavior yourself and want something to react to on shape/naming/interface — so I'm optimizing for a clean, idiomatic surface rather than defending choices. Key assumptions baked into the shape:

- **No batching** — each call sends immediately via HTTP POST. If your API expects buffered/batched submission, the interface changes shape significantly (would need `flush()`, background thread, etc.)
- **Single endpoint** (`/metrics`) taking `{type, name, value, tags}` as JSON — I don't know your actual wire format, this is a placeholder shape
- **Synchronous, `requests`-based** — no async, no retry/backoff logic yet
- **Errors are loud** (`raise_for_status()`) rather than swallowed or logged — first-pass assumes you want failures visible
- **Tags are optional and mergeable** with client-level defaults — common pattern, may not match your API's actual dimension model

<assumptions>
  <project>Internal metrics API reachable over HTTP; no auth scheme specified so none is implemented, just a `session` seam to add it later</project>
  <task>You want a shape to critique, not a production-ready client — so I favored a small, obvious surface over completeness (no gauges, no batching, no retries)</task>
  <operator>You'll drive the interface iteration; I kept commentary minimal so the code itself is the thing to react to</operator>
</assumptions>

### The artifact

```python
import time
import contextlib
from typing import Optional, Mapping, Union

import requests


class MetricsClient:
    """Client for sending counters and timings to the internal metrics API."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 2.0,
        default_tags: Optional[Mapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._default_tags = dict(default_tags or {})
        self._session = session or requests.Session()

    def increment(
        self,
        name: str,
        value: int = 1,
        *,
        tags: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Report a counter increment."""
        self._send("counter", name, value, tags)

    def timing(
        self,
        name: str,
        value_ms: float,
        *,
        tags: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Report a timing in milliseconds."""
        self._send("timing", name, value_ms, tags)

    @contextlib.contextmanager
    def timer(self, name: str, *, tags: Optional[Mapping[str, str]] = None):
        """Time a block of code and report it as a timing on exit."""
        start = time.monotonic()
        try:
            yield
        finally:
            elapsed_ms = (time.monotonic() - start) * 1000
            self.timing(name, elapsed_ms, tags=tags)

    def _send(
        self,
        metric_type: str,
        name: str,
        value: Union[int, float],
        tags: Optional[Mapping[str, str]],
    ) -> None:
        payload = {
            "type": metric_type,
            "name": name,
            "value": value,
            "tags": {**self._default_tags, **(tags or {})},
        }
        response = self._session.post(
            f"{self._base_url}/metrics",
            json=payload,
            timeout=self._timeout,
        )
        response.raise_for_status()

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "MetricsClient":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()
```

Things most likely to be wrong for your actual API: the payload shape in `_send`, whether counters/timings even share an endpoint, and whether "fire immediately" is acceptable or you need buffering. Those are the three places I'd expect you to push back first.