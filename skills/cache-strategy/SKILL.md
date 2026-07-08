---
name: cache-strategy
description: Implement caching strategies for HTTP, service workers, and memoization
disable-model-invocation: false
---

# Cache Strategy Implementation

I'll analyze your application and implement appropriate caching strategies to improve performance and reduce server load.

Arguments: `$ARGUMENTS` - cache type focus (e.g., "http", "service-worker", "redis", "browser")

## Strategic Planning Process

<think>
Effective caching requires careful strategy:

1. **Application Analysis**
   - What type of application? (SPA, MPA, API, static site)
   - What data changes frequently vs. rarely?
   - What's cached currently, if anything?
   - Client-side, server-side, or both?
   - CDN usage and configuration

2. **Cache Layer Selection**
   - Browser cache (HTTP headers)
   - Service worker cache (offline-first PWA)
   - Application cache (in-memory, localStorage)
   - Server cache (Redis, Memcached)
   - CDN cache (edge caching)
   - Database query cache

3. **Cache Invalidation Strategy**
   - Time-based expiration (TTL)
   - Event-based invalidation
   - Version-based cache busting
   - Manual invalidation mechanisms
   - Stale-while-revalidate patterns

4. **Performance vs. Freshness Tradeoff**
   - Critical real-time data (no cache or very short TTL)
   - Semi-dynamic data (short TTL, stale-while-revalidate)
   - Static assets (long TTL, immutable)
   - User-specific data (private cache)
</think>

## Phase 1: Cache Audit

**MANDATORY FIRST STEPS:**
1. Detect application type and architecture
2. Analyze current caching configuration
3. Identify cacheable resources
4. Determine cache invalidation needs

Let me analyze your current caching setup:

```bash
# Check for existing cache configurations
echo "=== Cache Configuration Audit ==="

# Check for service worker
if [ -f "public/service-worker.js" ] || [ -f "src/service-worker.js" ] || [ -f "sw.js" ]; then
    echo "✓ Service Worker detected"
    ls -lh **/service-worker.js **/sw.js 2>/dev/null | head -5
else
    echo "✗ No Service Worker found"
fi

# Check for HTTP caching headers (common web server configs)
if [ -f ".htaccess" ]; then
    echo "✓ Apache .htaccess found"
    grep -i "cache-control\|expires" .htaccess 2>/dev/null | head -5
fi

if [ -f "nginx.conf" ] || [ -f "nginx/*.conf" ]; then
    echo "✓ Nginx config found"
    grep -i "cache\|expires" nginx*.conf 2>/dev/null | head -5
fi

# Check for Redis/Memcached dependencies
if grep -q "\"redis\"" package.json 2>/dev/null; then
    echo "✓ Redis client installed"
fi

if grep -q "\"memcached\"" package.json 2>/dev/null; then
    echo "✓ Memcached client installed"
fi

# Check for caching libraries
if grep -q "\"workbox\"" package.json 2>/dev/null; then
    echo "✓ Workbox (service worker toolkit) installed"
fi

# Check CDN configuration
if [ -f "vercel.json" ] || [ -f "netlify.toml" ]; then
    echo "✓ CDN configuration detected"
fi
```

## Phase 2: Cache Strategy Design

Based on application type, I'll design appropriate caching layers:

### Browser Cache Strategy (HTTP Headers)

**Static Assets:**
- Long cache duration (1 year)
- Immutable for versioned assets
- Public caching allowed
- Proper ETag configuration

**Dynamic Content:**
- Short cache duration or no-cache
- Private cache for user-specific data
- Stale-while-revalidate for better UX
- Proper cache-control directives

**API Responses:**
- Cache-Control based on data freshness
- ETag for conditional requests
- Vary headers for content negotiation
- Private cache for authenticated requests

### Service Worker Cache Strategy

**Cache-First (Offline-First):**
- Static assets, fonts, images
- Application shell
- Third-party libraries

**Network-First:**
- API calls
- Dynamic content
- Real-time data

**Stale-While-Revalidate:**
- Semi-dynamic content
- News feeds, product listings
- Balance freshness with performance

**Cache-Only:**
- Fallback offline pages
- Critical UI assets

### Application-Level Caching

**In-Memory Caching:**
- Computed values (memoization)
- Expensive calculations
- API response caching
- Query result caching

**Local Storage:**
- User preferences
- Authentication tokens
- Offline data sync
- Application state persistence

### Server-Side Caching

**Redis/Memcached:**
- Database query results
- Computed data
- Session storage
- API response caching
- Rate limiting data

**CDN Edge Caching:**
- Static assets
- API responses (when appropriate)
- Geographic distribution
- DDoS protection

## Phase 3: Implementation

I'll implement selected caching strategies:

### HTTP Caching Headers

**For Node.js/Express:**
```javascript
// Static assets with long-term caching
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true,
  etag: true
}));

// API responses with short-term caching
app.use('/api', (req, res, next) => {
  res.set('Cache-Control', 'private, max-age=300'); // 5 minutes
  next();
});
```

**For Next.js:**
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
```

**For Nginx:**
```nginx
# Static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# HTML files - no cache
location ~* \.html$ {
    expires -1;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

### Service Worker Implementation

**Workbox Configuration:**
```javascript
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Precache static assets
precacheAndRoute(self.__WB_MANIFEST);

// Cache images with Cache First strategy
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
      }),
    ],
  })
);

// API calls with Network First strategy
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxAgeSeconds: 5 * 60, // 5 minutes
      }),
    ],
  })
);

// CSS and JS with Stale While Revalidate
registerRoute(
  ({ request }) => request.destination === 'style' || request.destination === 'script',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
  })
);
```

### Memoization Patterns

**React Memoization:**
```javascript
import { useMemo, useCallback } from 'react';
import { memo } from 'react';

// Memoize expensive calculations
const ExpensiveComponent = ({ data }) => {
  const processedData = useMemo(() => {
    return expensiveCalculation(data);
  }, [data]);

  const handleClick = useCallback(() => {
    // Handler logic
  }, []);

  return <div>{processedData}</div>;
};

export default memo(ExpensiveComponent);
```

**Function Memoization:**
```javascript
// Simple memoization utility
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// LRU cache with size limit
class LRUCache {
  constructor(limit = 100) {
    this.cache = new Map();
    this.limit = limit;
  }

  get(key) {
    if (!this.cache.has(key)) return undefined;
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value); // Move to end
    return value;
  }

  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.limit) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

### Redis Caching

**Express with Redis:**
```javascript
const redis = require('redis');
const client = redis.createClient();

// Cache middleware
const cache = (duration) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl}`;

    try {
      const cached = await client.get(key);
      if (cached) {
        return res.json(JSON.parse(cached));
      }

      // Store original send function
      const originalSend = res.json.bind(res);

      // Override send to cache response
      res.json = (body) => {
        client.setex(key, duration, JSON.stringify(body));
        return originalSend(body);
      };

      next();
    } catch (err) {
      next();
    }
  };
};

// Use cache middleware
app.get('/api/data', cache(300), async (req, res) => {
  const data = await fetchData();
  res.json(data);
});
```

## Phase 4: Cache Invalidation

I'll implement appropriate invalidation strategies:

**Time-Based Expiration:**
- Set appropriate TTL values
- Use max-age headers
- Configure Redis expiration
- Implement cleanup routines

**Event-Based Invalidation:**
- Clear cache on data updates
- Invalidate related cache entries
- Use cache tags for grouped invalidation
- Implement webhook-based clearing

**Version-Based Cache Busting:**
- Content hashing for static assets
- API versioning
- Service worker updates
- Cache key versioning

## Token Optimization

**Expected range**: 1,000–1,800 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches detected cache patterns in `.claude/cache/cache-strategy/cache_patterns.json` for 7 days.

**Early exit**: Returns immediately if caching patterns are already optimal for the project.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
