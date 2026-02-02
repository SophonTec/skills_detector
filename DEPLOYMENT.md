# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB+ RAM
- 10GB+ disk space
- Linux/macOS/Windows with WSL2

## Step 1: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Generate secure keys (Linux/macOS)
openssl rand -base64 32  # For DATABASE_ENCRYPTION_KEY
openssl rand -base64 32  # For SECRET_KEY

# Edit .env file
nano .env
```

## Step 2: Setup GitHub Token (Recommended)

1. Go to https://github.com/settings/tokens
2. Generate new classic token
3. Select scopes: `public_repo`
4. Copy token and add to `.env`:
```
GITHUB_TOKEN=ghp_your_token_here
```

## Step 3: Build and Start

```bash
# Using start script (recommended)
./scripts/start.sh

# Or manually
docker compose up -d
```

## Step 4: Verify Deployment

```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f

# Test API
curl http://localhost/api/v1/health

# Test web UI
# Open http://localhost in browser
```

## Step 5: Setup Automated Scraping

The scheduler starts automatically. To trigger manual scrapes:

```bash
# Scrape GitHub
curl -X POST http://localhost/api/v1/scrape/github

# Check scrape status
curl http://localhost/api/v1/scrapes
```

## Step 6: Setup Backups

```bash
# Create backup
./scripts/backup.sh

# Add to crontab for daily backups at 2 AM
crontab -e
# Add: 0 2 * * * /path/to/skill_detector/scripts/backup.sh
```

## Optional: Systemd Service (Auto-start on boot)

```bash
# Install as systemd service
sudo cp ai-skills-tracker.service /etc/systemd/system/
sudo mkdir -p /opt/ai-skills-tracker
sudo cp -r * /opt/ai-skills-tracker/
sudo chown -R $USER:$USER /opt/ai-skills-tracker

# Enable service
sudo systemctl enable ai-skills-tracker
sudo systemctl start ai-skills-tracker

# Check status
sudo systemctl status ai-skills-tracker
```

## Optional: SSL/TLS (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx.conf to use SSL
# Uncomment SSL configuration
# Add certificate paths

# Reload nginx
docker compose restart nginx
```

## Troubleshooting

### Port already in use
```bash
# Check what's using port 80
sudo lsof -i :80

# Change port in docker-compose.yml
# ports:
#   - "8080:80"
```

### Database corruption
```bash
# Restore from backup
docker compose down -v
cp backups/skills_backup_YYYYMMDD_HHMMSS.db.enc data/skills.db
docker compose up -d
```

### Out of memory
```bash
# Check resource usage
docker stats

# Limit container memory in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
```

### Scraper failing
```bash
# Check logs for specific errors
docker compose logs backend | grep -i error

# Trigger manual scrape to see detailed logs
curl -X POST http://localhost/api/v1/scrape/github
docker compose logs backend -f
```

## Monitoring

### Health check endpoint
```bash
watch -n 5 'curl -s http://localhost/api/v1/health'
```

### View statistics
```bash
curl -s http://localhost/api/v1/stats | jq .
```

### Resource usage
```bash
docker stats
```

## Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose down
docker compose up -d --build
```

## Uninstall

```bash
# Stop and remove containers
docker compose down -v

# Remove systemd service (if installed)
sudo systemctl disable ai-skills-tracker
sudo rm /etc/systemd/system/ai-skills-tracker.service

# Remove files
sudo rm -rf /opt/ai-skills-tracker
```

---

*For support, check logs: `docker compose logs -f`*
