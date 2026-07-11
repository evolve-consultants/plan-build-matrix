# Let's Step Back

Good catch. Before you implement *any* caching solution, let's diagnose the actual problem:

## 1. First: What's the real issue?

```python
# routes/products.py - Add instrumentation FIRST
import time
import logging
from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    start = time.time()
    
    # Where's the time going?
    db_start = time.time()
    product = db.query(Product).filter_by(id=product_id).first()
    db_time = time.time() - db_start
    
    processing_time = time.time() - start
    
    logger.info(f"Product {product_id}: DB={db_time:.3f}s, Total={processing_time:.3f}s")
    
    return product
```

**Questions to answer:**
- Is it a **database query problem**? (slow SQL, missing indexes, N+1 queries)
- Is it a **processing problem**? (expensive calculations, transformations)
- Is it a **concurrency problem**? (too many requests, connection pool exhaustion)
- Is it a **specific endpoint** that's slow, or everything?

## 2. Postgres-Native Solutions (Better Than External Cache)

### Option A: Query-Level Caching with Materialized Views

```python
# migrations/create_popular_products_view.sql
CREATE MATERIALIZED VIEW popular_products_cache AS
SELECT 
    p.id,
    p.name,
    p.price,
    COUNT(o.id) as order_count
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.id
WITH DATA;

CREATE INDEX ON popular_products_cache(order_count DESC);

-- Refresh periodically (via scheduled job)
REFRESH MATERIALIZED VIEW CONCURRENTLY popular_products_cache;
```

```python
# Usage in your API
class ProductService:
    def get_popular_products(self):
        # Queries pre-computed view instead of expensive joins
        return db.session.execute(
            "SELECT * FROM popular_products_cache ORDER BY order_count DESC LIMIT 10"
        ).fetchall()
```

### Option B: Proper Indexing

```python
# models.py
from sqlalchemy import Index

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)  # Single column index
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Float)
    created_at = Column(DateTime, index=True)
    
    # Composite index for common query patterns
    __table_args__ = (
        Index('idx_category_price', 'category_id', 'price'),
        Index('idx_name_created', 'name', 'created_at'),
    )
```

### Option C: Connection Pooling Tuning

```python
# config/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

DATABASE_URL = "postgresql://user:password@localhost/products_db"

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,           # Connections to keep open
    max_overflow=10,        # Extra connections when busy
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Test connections before use
    echo=False,
)
```

### Option D: Query Optimization

```python
# services/product_service.py - N+1 Query Problem
from sqlalchemy.orm import joinedload

class ProductService:
    
    # ❌ BAD - N+1 queries (1 for products + N for each product's reviews)
    def get_products_bad(self):
        products = db.session.query(Product).all()
        return [
            {
                **product.to_dict(),
                "reviews": [r.to_dict() for r in product.reviews]  # Extra query per product!
            }
            for product in products
        ]
    
    # ✅ GOOD - Single query with joinedload
    def get_products_good(self):
        products = db.session.query(Product).options(
            joinedload(Product.reviews),
            joinedload(Product.category)
        ).all()
        return [p.to_dict() for p in products]
    
    # ✅ ALSO GOOD - Batch query only needed data
    def get_product_ids_with_names(self):
        return db.session.query(Product.id, Product.name).all()
```

## 3. Application-Level Caching (Using Only Postgres)

If you *really* need caching without Redis, use Postgres itself:

```python
# models.py
class CacheEntry(Base):
    __tablename__ = "cache_entries"
    
    key = Column(String, primary_key=True)
    value = Column(JSON)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# services/postgres_cache.py
import json
from datetime import datetime, timedelta

class PostgresCache:
    def get(self, key: str):
        entry = db.session.query(CacheEntry).filter(
            CacheEntry.key == key,
            CacheEntry.expires_at > datetime.utcnow()
        ).first()
        return json.loads(entry.value) if entry else None
    
    def set(self, key: str, value: dict, ttl_seconds: int = 3600):
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        
        db.session.merge(CacheEntry(
            key=key,
            value=json.dumps(value),
            expires_at=expires_at
        ))
        db.session.commit()
    
    def cleanup_expired(self):
        """Run periodically to delete expired entries"""
        db.session.query(CacheEntry).filter(
            CacheEntry.expires_at <= datetime.utcnow()
        ).delete()
        db.session.commit()

# Scheduled job to clean up
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=PostgresCache().cleanup_expired,
    trigger="interval",
    minutes=30
)
scheduler.start()
```

## 4. What To Actually Do Right Now

**Priority order:**

1. **Measure** - Add logging to find the bottleneck (see code above)
2. **Index** - Add database indexes on filter/join columns
3. **Optimize queries** - Fix N+1 problems with joinedload
4. **Tune connections** - Adjust pool settings
5. **Materialize** - Create views for expensive aggregations
6. **Only then consider caching** - If it's *still* slow

## 5. Monitoring to Help Diagnosis

```python
# middleware/timing.py
from fastapi import Request
import time

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    
    response.headers["X-Process-Time"] = str(process_time)
    if process_time > 1.0:
        logger.warning(f"SLOW: {request.url.path} took {process_time:.2f}s")
    
    return response
```

**Bottom line:** 90% of the time, the answer is "fix your queries" not "add a cache." What does your slow endpoint's query actually look like?