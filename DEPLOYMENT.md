# Deployment Guide

This guide covers different deployment options for the Configurable Researcher Agent.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Cloud Deployment](#cloud-deployment)

## Local Development

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/shashanksaxena-tz/Configurable-Researcher-Agent.git
cd Configurable-Researcher-Agent
```

2. Backend setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend setup:
```bash
cd ../frontend
npm install
```

4. Start both servers:
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Access the application at `http://localhost:3000`

## Docker Deployment

### Using Docker Compose (Recommended)

1. Create `docker-compose.yml` in the root directory:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - CORS_ORIGINS=http://localhost:3000
    volumes:
      - ./backend/reports:/app/reports

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8000
```

2. Create backend Dockerfile (`backend/Dockerfile`):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. Create frontend Dockerfile (`frontend/Dockerfile`):
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

## Production Deployment

### Backend (FastAPI)

#### Using Gunicorn + Uvicorn Workers

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with:
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

#### Systemd Service

Create `/etc/systemd/system/researcher-api.service`:
```ini
[Unit]
Description=Configurable Researcher Agent API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/researcher-agent/backend
Environment="PATH=/var/www/researcher-agent/backend/venv/bin"
ExecStart=/var/www/researcher-agent/backend/venv/bin/gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable researcher-api
sudo systemctl start researcher-api
```

### Frontend (React)

#### Build for Production

```bash
cd frontend
npm run build
```

#### Serve with Nginx

Create `/etc/nginx/sites-available/researcher-agent`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/researcher-agent/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/researcher-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Cloud Deployment

### AWS Deployment

#### Using AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
cd backend
eb init -p python-3.11 researcher-agent
```

3. Deploy:
```bash
eb create researcher-env
eb deploy
```

#### Using AWS ECS with Fargate

1. Build and push Docker images to ECR
2. Create ECS task definition
3. Create ECS service with Fargate launch type
4. Configure Application Load Balancer

### Google Cloud Platform

#### Using Cloud Run

1. Build container:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/researcher-agent
```

2. Deploy:
```bash
gcloud run deploy researcher-agent \
  --image gcr.io/PROJECT_ID/researcher-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku Deployment

#### Backend

1. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create researcher-agent-api
git push heroku main
```

#### Frontend

1. Build the frontend and serve with a static server
2. Deploy to Netlify, Vercel, or similar platforms

### Vercel Deployment (Frontend)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd frontend
vercel
```

## Environment Variables

### Production Environment Variables

Backend (`.env`):
```bash
APP_NAME="Configurable Researcher Agent"
VERSION="1.0.0"
API_PREFIX="/api/v1"
CORS_ORIGINS="https://yourdomain.com"
MAX_SEARCH_RESULTS=10
TIMEOUT_SECONDS=30
REPORTS_DIR="/var/www/researcher-agent/reports"
```

Frontend:
```bash
VITE_API_URL=https://api.yourdomain.com
```

## SSL/TLS Configuration

### Using Let's Encrypt with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Auto-renewal:
```bash
sudo certbot renew --dry-run
```

## Monitoring and Logging

### Application Logs

Backend logs location: `/var/log/researcher-agent/api.log`

Configure logging in `main.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/researcher-agent/api.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring

Consider using:
- **Prometheus + Grafana** for metrics
- **Sentry** for error tracking
- **ELK Stack** for log aggregation
- **Uptime Robot** for uptime monitoring

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy, AWS ALB)
- Deploy multiple backend instances
- Use shared file storage for reports (S3, GCS, etc.)

### Caching

- Redis for caching API responses
- CDN for frontend assets

### Database

For production, consider adding:
- PostgreSQL for storing research history
- MongoDB for document-based storage
- Redis for caching and session management

## Security Best Practices

1. **Enable HTTPS** in production
2. **Set secure CORS policies**
3. **Implement rate limiting**
4. **Add authentication** for API access
5. **Sanitize user inputs**
6. **Keep dependencies updated**
7. **Use environment variables** for secrets
8. **Enable firewall** and security groups
9. **Regular security audits**
10. **Implement API key authentication**

## Backup and Recovery

Regular backups:
```bash
# Backup reports directory
tar -czf reports-backup-$(date +%Y%m%d).tar.gz /var/www/researcher-agent/reports

# Automated daily backup
0 2 * * * /path/to/backup-script.sh
```

## Performance Optimization

1. Enable gzip compression in Nginx
2. Use CDN for static assets
3. Implement caching strategies
4. Optimize database queries
5. Use connection pooling
6. Enable HTTP/2
7. Minimize bundle sizes
8. Lazy load components

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Permission issues:**
```bash
sudo chown -R www-data:www-data /var/www/researcher-agent
```

**Dependencies not installing:**
```bash
pip install --upgrade pip
npm cache clean --force
```

## Health Checks

Set up health check endpoints:
- `/api/v1/health` - Application health
- Monitor response times
- Check disk space for reports directory
- Monitor memory usage

## Support

For deployment issues:
1. Check logs first
2. Verify environment variables
3. Test network connectivity
4. Review firewall rules
5. Check service status
