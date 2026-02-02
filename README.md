# AI Skills Tracker

A web application that tracks, ranks, and displays AI skills from multiple sources including GitHub, npm, PyPI, and Hugging Face.

## Features

- **Multi-source data aggregation**: Tracks AI skills from GitHub repos, npm packages, PyPI packages, and Hugging Face models
- **Smart sorting**:
  - **Latest**: Recently updated skills
  - **Hot**: Most popular by weekly activity
  - **Most Used**: Most downloaded/utilized skills
- **Real-time updates**: Automated scraping at configurable intervals
- **Simple, clean UI**: Minimalist design with intuitive navigation
- **High security**: Encrypted database, rate limiting, security headers
- **Production-ready**: Docker-based deployment with auto-restart

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│  Next.js    │
│  (Proxy)    │     │  Frontend   │
└──────┬──────┘     └─────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  FastAPI    │────▶│  SQLite DB  │
│  Backend    │     │ (Encrypted) │
└──────┬──────┘     └─────────────┘
       │
       ├───────────┬───────────┬───────────┐
       ▼           ▼           ▼           ▼
    GitHub       npm         PyPI     Hugging Face
```

## Tech Stack

- **Backend**: FastAPI (Python), SQLite (encrypted), Playwright (scraping)
- **Frontend**: Next.js (React), TypeScript, Tailwind CSS
- **Deployment**: Docker, Docker Compose, Nginx
- **Security**: SQLCipher encryption, rate limiting, security headers

## Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 2GB RAM available

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd skill_detector
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the application:
```bash
./scripts/start.sh
```

4. Access the application:
- Web UI: http://localhost
- API docs: http://localhost/api/v1/docs

### Manual Start

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_ENCRYPTION_KEY` | 32-character encryption key for SQLite | Yes |
| `SECRET_KEY` | Secret key for JWT | Yes |
| `GITHUB_TOKEN` | GitHub PAT for higher rate limits | No |
| `FRONTEND_URL` | Frontend URL for CORS | Yes |

### Scraping Schedule

Default intervals (configurable):
- GitHub: Every 60 minutes
- npm: Every 24 hours
- PyPI: Every 24 hours
- Hugging Face: Every 60 minutes

## API Endpoints

### Public Endpoints

```
GET /api/v1/skills?sort=latest&source=all&limit=50
GET /api/v1/skills/{id}
GET /api/v1/skills/{id}/history?days=30
GET /api/v1/stats
```

### Admin Endpoints

```
GET /api/v1/health
GET /api/v1/scrapes
POST /api/v1/scrape/{source}
```

## Data Sources

| Source | Metrics Tracked | Update Frequency |
|--------|----------------|------------------|
| GitHub | stars, forks, last_updated | Hourly |
| npm | downloads (daily/weekly/monthly) | Daily |
| PyPI | downloads (daily/weekly/monthly) | Daily |
| Hugging Face | downloads, likes, lastModified | Hourly |

## Security

- **Database**: SQLCipher 256-bit AES encryption at rest
- **API**: Rate limiting (60 req/min per IP)
- **Network**: HTTPS with security headers
- **Container**: Non-root user, minimal base images

## Performance

- Handles 10,000+ daily visitors
- API response time: < 200ms
- Page load time: < 2s
- Database size: < 500MB

## Backup

Automated backups are stored in `./backups/`:

```bash
./scripts/backup.sh
```

Retention: Last 30 backups.

## Troubleshooting

### Services won't start
```bash
docker compose logs
```

### Database issues
```bash
docker compose exec backend ls -la /app/data
```

### Reset everything
```bash
docker compose down -v
docker compose up -d
```

## Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## License

MIT

## Contributing

Contributions welcome! Please read the contributing guidelines.

---

*Built with ❤️ for the AI community*
