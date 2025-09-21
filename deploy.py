#!/usr/bin/env python3
"""
CareerAIpilot Deployment Script
Handles production deployment with proper configuration and monitoring
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_production_env():
    """Create production environment configuration"""
    print("🔧 Setting up production environment...")
    
    prod_env_content = """# CareerAIpilot Production Environment

# Required API Keys (Replace with your actual keys)
GOOGLE_API_KEY=your_production_google_api_key
OPENAI_API_KEY=your_production_openai_api_key

# Production Server Configuration
MCP_SERVER_URL=http://localhost:8000
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database Configuration
CHROMA_DB_PATH=/app/data/chroma_db
FAISS_INDEX_PATH=/app/data/cv_index.faiss
FAISS_DOCUMENTS_PATH=/app/data/cv_documents.pkl

# Security Configuration
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/app/logs/careerai.log

# Performance Configuration
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30
"""
    
    with open('.env.production', 'w') as f:
        f.write(prod_env_content)
    
    print("✅ Production environment file created (.env.production)")
    print("⚠️  Remember to update API keys in .env.production")

def create_docker_setup():
    """Create Docker configuration for deployment"""
    print("\n🐳 Creating Docker configuration...")
    
    # Dockerfile
    dockerfile_content = """FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    # Docker Compose
    docker_compose_content = """version: '3.8'

services:
  careerai-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  careerai-client:
    build: .
    command: ["python", "main.py"]
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MCP_SERVER_URL=http://careerai-server:8000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - careerai-server
    restart: unless-stopped
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose_content)
    
    # Docker ignore
    dockerignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
*.egg-info/
dist/
build/
.env
.env.local
.env.development
.env.test
.env.production
*.md
README.md
test_*
.gitignore
"""
    
    with open('.dockerignore', 'w') as f:
        f.write(dockerignore_content)
    
    print("✅ Docker configuration created")
    print("   - Dockerfile")
    print("   - docker-compose.yml")
    print("   - .dockerignore")

def create_systemd_service():
    """Create systemd service for Linux deployment"""
    print("\n⚙️  Creating systemd service...")
    
    service_content = """[Unit]
Description=CareerAIpilot MCP Server
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/careerai
Environment=PATH=/opt/careerai/venv/bin
ExecStart=/opt/careerai/venv/bin/uvicorn mcp_server:app --host 0.0.0.0 --port 8000 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('careerai.service', 'w') as f:
        f.write(service_content)
    
    print("✅ Systemd service file created (careerai.service)")
    print("📋 To install on Ubuntu/Debian:")
    print("   sudo cp careerai.service /etc/systemd/system/")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable careerai")
    print("   sudo systemctl start careerai")

def create_nginx_config():
    """Create Nginx configuration for reverse proxy"""
    print("\n🌐 Creating Nginx configuration...")
    
    nginx_config = """server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed for real-time features)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8000/;
        access_log off;
    }

    # Static files (if any)
    location /static/ {
        alias /opt/careerai/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
"""
    
    with open('nginx.conf', 'w') as f:
        f.write(nginx_config)
    
    print("✅ Nginx configuration created (nginx.conf)")
    print("📋 To install on Ubuntu/Debian:")
    print("   sudo cp nginx.conf /etc/nginx/sites-available/careerai")
    print("   sudo ln -s /etc/nginx/sites-available/careerai /etc/nginx/sites-enabled/")
    print("   sudo nginx -t")
    print("   sudo systemctl reload nginx")

def create_monitoring_setup():
    """Create monitoring and logging configuration"""
    print("\n📊 Creating monitoring setup...")
    
    # Logging configuration
    logging_config = """import logging
import os
from datetime import datetime

def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/careerai.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create separate loggers for different components
    logger = logging.getLogger('careerai')
    
    return logger

# Usage example:
# from logging_config import setup_logging
# logger = setup_logging()
# logger.info("Application started")
"""
    
    with open('logging_config.py', 'w') as f:
        f.write(logging_config)
    
    # Monitoring script
    monitoring_script = """#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime

def check_health():
    try:
        response = requests.get('http://localhost:8000/', timeout=10)
        if response.status_code == 200:
            print(f"✅ {datetime.now()}: Service is healthy")
            return True
        else:
            print(f"❌ {datetime.now()}: Service returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {datetime.now()}: Health check failed - {str(e)}")
        return False

def monitor_service():
    while True:
        check_health()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    monitor_service()
"""
    
    with open('monitor.py', 'w') as f:
        f.write(monitoring_script)
    
    print("✅ Monitoring setup created")
    print("   - logging_config.py")
    print("   - monitor.py")

def create_deployment_script():
    """Create deployment automation script"""
    print("\n🚀 Creating deployment script...")
    
    deploy_script = """#!/bin/bash
# CareerAIpilot Deployment Script

set -e  # Exit on any error

echo "🚀 Starting CareerAIpilot Deployment..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    exit 1
fi

# Create application directory
APP_DIR="/opt/careerai"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📁 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data logs static

# Set permissions
chmod +x test_system.py
chmod +x monitor.py

# Run tests
echo "🧪 Running system tests..."
python test_system.py

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Deployment aborted."
    exit 1
fi

# Setup systemd service
echo "⚙️  Setting up systemd service..."
sudo cp careerai.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable careerai

# Start service
echo "🚀 Starting CareerAIpilot service..."
sudo systemctl start careerai

# Check status
sleep 5
if sudo systemctl is-active --quiet careerai; then
    echo "✅ CareerAIpilot is running!"
    echo "🌐 Access your service at: http://localhost:8000"
    echo "📊 API docs at: http://localhost:8000/docs"
else
    echo "❌ Service failed to start. Check logs with:"
    echo "   sudo journalctl -u careerai -f"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
"""
    
    with open('deploy.sh', 'w') as f:
        f.write(deploy_script)
    
    # Make it executable
    os.chmod('deploy.sh', 0o755)
    
    print("✅ Deployment script created (deploy.sh)")
    print("📋 To deploy:")
    print("   chmod +x deploy.sh")
    print("   ./deploy.sh")

def create_documentation():
    """Create deployment documentation"""
    print("\n📚 Creating deployment documentation...")
    
    deployment_guide = """# CareerAIpilot Deployment Guide

## Prerequisites

1. **Python 3.11+** installed
2. **Git** installed
3. **API Keys**:
   - Google API key for Gemini
   - OpenAI API key (optional, for embeddings)

## Quick Start

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run tests
python test_system.py

# Start MCP server
uvicorn mcp_server:app --reload

# Run main application
python main.py
```

### 2. Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual container
docker build -t careerai .
docker run -p 8000:8000 --env-file .env careerai
```

### 3. Production Deployment
```bash
# Run deployment script
chmod +x deploy.sh
./deploy.sh
```

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for Gemini LLM
- `OPENAI_API_KEY`: Optional, for embeddings
- `MCP_SERVER_URL`: Server URL (default: http://localhost:8000)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### API Endpoints
- `GET /`: Discovery endpoint
- `POST /invoke`: Tool invocation
- `GET /resources/{name}`: Resource access
- `GET /prompts/{name}`: Prompt templates
- `GET /docs`: API documentation

## Monitoring

### Health Checks
```bash
# Check service status
sudo systemctl status careerai

# View logs
sudo journalctl -u careerai -f

# Manual health check
python monitor.py
```

### Logs
- Application logs: `/opt/careerai/logs/careerai.log`
- System logs: `sudo journalctl -u careerai`

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure GOOGLE_API_KEY is set correctly
   - Check API key permissions and quotas

2. **Port Conflicts**
   - Change PORT in .env if 8000 is occupied
   - Update nginx config if using reverse proxy

3. **Memory Issues**
   - Reduce number of workers in systemd service
   - Monitor memory usage with `htop`

4. **Dependency Issues**
   - Ensure all packages are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

### Performance Tuning

1. **Increase Workers**
   ```bash
   # Edit systemd service
   sudo systemctl edit careerai
   # Add: [Service] ExecStart=... --workers 8
   ```

2. **Database Optimization**
   - Adjust ChromaDB settings in enhanced_rag_pipeline.py
   - Monitor FAISS index size

3. **Caching**
   - Implement Redis for session management
   - Cache frequently accessed resources

## Security

### Production Security Checklist
- [ ] Change default SECRET_KEY
- [ ] Use HTTPS with SSL certificates
- [ ] Implement proper authentication
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor access logs

### SSL Setup with Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Scaling

### Horizontal Scaling
1. Use load balancer (nginx/HAProxy)
2. Deploy multiple instances
3. Use shared database (Redis/PostgreSQL)

### Vertical Scaling
1. Increase server resources
2. Optimize Python performance
3. Use faster embeddings models

## Support

For issues and questions:
1. Check logs first
2. Run test suite: `python test_system.py`
3. Review this documentation
4. Check GitHub issues (if applicable)
"""
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(deployment_guide)
    
    print("✅ Deployment documentation created (DEPLOYMENT.md)")

def main():
    """Main deployment setup function"""
    print("🚀 CareerAIpilot Deployment Setup")
    print("=" * 50)
    
    setup_functions = [
        ("Production Environment", create_production_env),
        ("Docker Configuration", create_docker_setup),
        ("Systemd Service", create_systemd_service),
        ("Nginx Configuration", create_nginx_config),
        ("Monitoring Setup", create_monitoring_setup),
        ("Deployment Script", create_deployment_script),
        ("Documentation", create_documentation),
    ]
    
    for name, func in setup_functions:
        try:
            func()
        except Exception as e:
            print(f"❌ Failed to create {name}: {str(e)}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 Deployment setup completed!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Update API keys in .env.production")
    print("2. Run tests: python test_system.py")
    print("3. Deploy: ./deploy.sh")
    print("\n📚 See DEPLOYMENT.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
