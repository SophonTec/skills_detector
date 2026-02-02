# AI Skills Tracker - System Design

## Phase 1: Research Summary

### Data Sources Selected

| Source | Metrics Tracked | API Rate Limit | Update Frequency |
|--------|----------------|----------------|------------------|
| GitHub | stars, forks, last_updated | 5000/hr (authenticated) | Every hour |
| npm | downloads (daily/weekly/monthly), last_modified | IP-based | Daily |
| PyPI | downloads (daily/weekly/monthly), upload_time | IP-based | Daily |
| Hugging Face | downloads, likes, lastModified | Varies | Every hour |

### Sorting Metrics Mapping

| Sort Type | GitHub | npm | PyPI | Hugging Face |
|-----------|--------|-----|------|---------------|
| Latest/Newest | `updated_at` | `time.modified` | `upload_time` | `lastModified` |
| Hot/Popular | `stargazers_count` | `downloads/last-week` | `last_week` | `downloads` |
| Most Used | `forks_count` | `downloads/last-month` | `last_month` | `downloads` |

---

## Phase 2: Architecture Design

### Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI (Python) | Async scraping, auto-docs, production-ready |
| Frontend | Next.js (React) | SSR/SSG, excellent DX, SEO-friendly |
| Database | SQLite + SQLCipher | Single-file, encrypted, zero-config |
| Scraping | Playwright (Python) | Cross-browser, async-first, anti-bot handling |
| Deployment | Docker + Compose + systemd | Isolated, reproducible, auto-restart |

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS (443)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Nginx (Reverse Proxy)                        │
│  - SSL/TLS termination                                            │
│  - Static file serving                                            │
│  - Rate limiting                                                  │
│  - Fail2ban integration                                          │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ├────────────────────────────┐
               │                            │
               ▼                            ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│  Next.js Frontend (Port 3000) │  │  FastAPI Backend (Port 8000) │
│  - React components           │  │  - REST API endpoints        │
│  - API client                │  │  - Data aggregation         │
│  - SSR/SSG                   │  │  - Rate limiting            │
│  - Static optimization       │  │  - Request validation       │
└──────────────────────────────┘  └──────────────────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────────────────┐
                                    │  SQLite Database (Encrypted)  │
                                    │  - skills table              │
                                    │  - metrics history          │
                                    │  - SQLCipher encryption      │
                                    └──────────────────────────────┘
                                              │
        ┌─────────────────────────────────────┼─────────────────────────────┐
        │                                     │                             │
        ▼                                     ▼                             ▼
┌──────────────┐                      ┌──────────────┐            ┌──────────────┐
│ GitHub API   │                      │ npm Registry  │            │ PyPI Stats   │
│ - Search API │                      │ - Downloads   │            │ - Downloads  │
│ - Repo API   │                      │ - Metadata    │            │ - Metadata   │
└──────────────┘                      └──────────────┘            └──────────────┘
        │
        ▼
┌──────────────────┐
│ Hugging Face API │
│ - Model info     │
│ - Downloads      │
└──────────────────┘

Background Services:
┌─────────────────────────────────────────────────────────────────┐
│  Scheduled Scraping Tasks (Background workers)                   │
│  - GitHub scraper (hourly)                                       │
│  - npm scraper (daily)                                           │
│  - PyPI scraper (daily)                                          │
│  - Hugging Face scraper (hourly)                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Database Schema

#### skills Table

| Column | Type | Description | Index |
|--------|------|-------------|-------|
| id | INTEGER PRIMARY KEY | Unique identifier | ✅ |
| name | TEXT | Skill name (unique) | ✅ |
| source | TEXT | Source platform (github/npm/pypi/huggingface) | ✅ |
| description | TEXT | Description of the skill | |
| url | TEXT | URL to the skill/resource | |
| language | TEXT | Programming language (if applicable) | |
| created_at | TIMESTAMP | When first discovered | |
| updated_at | TIMESTAMP | Last update timestamp | |

#### skill_metrics Table

| Column | Type | Description | Index |
|--------|------|-------------|-------|
| id | INTEGER PRIMARY KEY | Unique identifier | |
| skill_id | INTEGER | FK to skills.id | ✅ |
| stars | INTEGER | GitHub stars count | |
| forks | INTEGER | GitHub forks count | |
| downloads_day | INTEGER | Downloads in last day | |
| downloads_week | INTEGER | Downloads in last week | |
| downloads_month | INTEGER | Downloads in last month | |
| likes | INTEGER | Likes (Hugging Face) | |
| last_activity | TIMESTAMP | Last activity timestamp | |
| recorded_at | TIMESTAMP | When this metric snapshot was taken | ✅ |

#### scrapes Table (Tracking scraping history)

| Column | Type | Description | Index |
|--------|------|-------------|-------|
| id | INTEGER PRIMARY KEY | Unique identifier | |
| source | TEXT | Source platform | ✅ |
| items_scraped | INTEGER | Number of items scraped | |
| status | TEXT | success/error/partial | |
| error_message | TEXT | Error details (if any) | |
| started_at | TIMESTAMP | When scraping started | |
| completed_at | TIMESTAMP | When scraping completed | ✅ |

### API Endpoints Design

#### Public Endpoints

```
GET /api/v1/skills
  Query params:
    - sort: latest|hot|used (default: latest)
    - source: github|npm|pypi|huggingface|all (default: all)
    - limit: 1-100 (default: 50)
  Response: List of skill objects with current metrics

GET /api/v1/skills/{id}
  Response: Single skill with full details

GET /api/v1/skills/{id}/history
  Query params:
    - days: 1-90 (default: 30)
  Response: Historical metrics for the skill

GET /api/v1/stats
  Response: Aggregate stats (total skills, last update, etc.)
```

#### Admin/Health Endpoints (Internal)

```
GET /api/v1/health
  Response: Service health status

POST /api/v1/scrape
  Query params:
    - source: github|npm|pypi|huggingface
  Response: Trigger scraping job

GET /api/v1/scrapes
  Response: Recent scraping history
```

### Data Model (Python)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class SkillBase(BaseModel):
    name: str
    source: Literal['github', 'npm', 'pypi', 'huggingface']
    description: str
    url: str
    language: Optional[str] = None

class SkillMetrics(BaseModel):
    stars: Optional[int] = None
    forks: Optional[int] = None
    downloads_day: Optional[int] = None
    downloads_week: Optional[int] = None
    downloads_month: Optional[int] = None
    likes: Optional[int] = None
    last_activity: Optional[datetime] = None

class Skill(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    metrics: SkillMetrics

class SkillsResponse(BaseModel):
    skills: list[Skill]
    total: int
    sort_by: str
    updated_at: datetime
```

---

## Phase 3: Security Measures

### 1. Database Security

- ✅ SQLCipher 256-bit AES encryption at rest
- ✅ File permissions: chmod 600 on database file
- ✅ Application runs as non-root user
- ✅ Parameterized queries (SQLAlchemy ORM)
- ✅ Encrypted backups

### 2. API Security

- ✅ HTTPS with Let's Encrypt SSL certificates
- ✅ CORS restricted to frontend domain only
- ✅ Rate limiting: 60 req/min per IP
- ✅ Input validation with Pydantic
- ✅ HTTP security headers (Nginx)
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security: max-age=31536000

### 3. Container Security

- ✅ Minimal base images (alpine)
- ✅ Run containers as non-root user
- ✅ Network isolation between services
- ✅ Secrets via environment variables only
- ✅ Regular image scanning with Trivy

### 4. Server Security

- ✅ Fail2ban for SSH protection
- ✅ Only necessary ports open (80, 443, 22)
- ✅ Automatic OS updates
- ✅ Regular dependency updates
- ✅ Daily encrypted database backups

### 5. Scraping Security

- ✅ Respect rate limits of external APIs
- ✅ Use rotating user agents (where applicable)
- ✅ Cache responses to minimize API calls
- ✅ Handle errors gracefully with retry logic
- ✅ Monitor for API key leaks

---

## Phase 4: Deployment Plan

### Docker Services

```yaml
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on: [frontend, backend]
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    restart: unless-stopped

  backend:
    build: ./backend
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_PATH=/app/data/skills.db
      - DATABASE_ENCRYPTION_KEY=${DB_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
```

### Systemd Service

```ini
[Unit]
Description=AI Skills Tracker
After=network.target docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/ai-skills-tracker
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

---

## Phase 5: Performance Considerations

### Expected Load Analysis

- **Daily visitors**: 10,000
- **Peak requests**: ~5 req/sec
- **Daily page views**: ~30,000 (3 pages/visitor)

### Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| API response time | < 200ms | SQLite indexing, connection pooling |
| Page load time | < 2s | Next.js SSR, static optimization |
| Scraping latency | < 5 min/job | Async operations, parallel requests |
| Database size | < 500MB | Regular cleanup, metrics retention |

### Caching Strategy

1. **Frontend**: Next.js static generation for homepage
2. **Backend**: Redis for API responses (5 min TTL)
3. **Database**: SQLite WAL mode for concurrent reads
4. **CDN**: Consider Cloudflare for global distribution

---

## Phase 6: Monitoring & Maintenance

### Health Checks

- ✅ `/api/v1/health` endpoint
- ✅ Docker container health checks
- ✅ Systemd service monitoring
- ✅ Uptime monitoring (UptimeRobot)

### Logging

- ✅ Application logs (structured JSON)
- ✅ Nginx access/error logs
- ✅ Scraping job logs
- ✅ Error tracking (Sentry optional)

### Backup Strategy

- ✅ Daily encrypted database backup (local)
- ✅ Retention: 30 days
- ✅ Backup script: cron job at 2 AM
- ✅ Offsite backup option (S3/GCS)

---

## Next Steps

1. ✅ Research completed
2. ✅ Architecture designed
3. ⏳ Create project structure
4. ⏳ Implement backend API
5. ⏳ Implement scraper services
6. ⏳ Build frontend UI
7. ⏳ Configure security
8. ⏳ Deploy and test

---

*Document generated: 2026-02-03*
*Version: 1.0*
