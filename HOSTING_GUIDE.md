# Complete Self-Hosting Guide for DankMemer/imgen

This guide provides detailed step-by-step instructions for self-hosting the DankMemer image generation microservice from scratch on a dedicated server. This assumes no prior setup and covers all dependencies, database setup, configuration, and deployment.

## Quick Start Summary

For experienced users, here's the condensed version:

1. **Install dependencies**: RethinkDB, Redis, ImageMagick, Python 3.8+, FFmpeg
2. **Clone repo**: `git clone https://github.com/DankMemer/imgen.git && cd imgen`
3. **Setup Python**: `python3 -m venv venv && source venv/bin/activate`
4. **Install packages**: `pip install -r requirements.txt && pip install gunicorn`
5. **Configure**: `cp config.template.json config.json` (edit with Discord OAuth credentials)
6. **Setup database**: `python3 setup_database.py`
7. **Create directories**: `mkdir -p cache/avatars`
8. **Start services**: `systemctl start rethinkdb redis` then `./start.sh`
9. **Access**: Visit `http://your-server:65535`

**Critical files to customize**: `config.json` (Discord OAuth + admin user IDs)

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Initial Server Setup](#initial-server-setup)
3. [Database Installation and Setup](#database-installation-and-setup)
4. [Python Environment Setup](#python-environment-setup)
5. [Application Setup](#application-setup)
6. [Configuration](#configuration)
7. [Database Schema Setup](#database-schema-setup)
8. [Directory Structure Setup](#directory-structure-setup)
9. [Service Management](#service-management)
10. [Testing the Installation](#testing-the-installation)
11. [Troubleshooting](#troubleshooting)
12. [Production Considerations](#production-considerations)

## System Requirements

### Minimum Hardware Requirements
- **CPU**: 4+ cores (image processing is CPU intensive)
- **RAM**: 8GB+ (TensorFlow and image processing require significant memory)
- **Storage**: 50GB+ (for application, dependencies, cache, and database)
- **Network**: Stable internet connection for Discord OAuth and external image fetching

### Supported Operating Systems
- Ubuntu 20.04 LTS or newer (recommended)
- Debian 10+ 
- CentOS 8+
- Other Linux distributions (with package manager adaptations)

## Initial Server Setup

### 1. Update System Packages
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
# OR for newer versions
sudo dnf update -y
```

### 2. Install Essential Build Tools
```bash
# Ubuntu/Debian
sudo apt install -y build-essential curl wget git software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# CentOS/RHEL
sudo yum groupinstall -y "Development Tools"
sudo yum install -y curl wget git
```

## Database Installation and Setup

### 1. Install RethinkDB

#### Ubuntu/Debian:
```bash
# Add RethinkDB repository
source /etc/lsb-release && echo "deb https://download.rethinkdb.com/repository/ubuntu-$DISTRIB_CODENAME $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list

# Add repository key
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -

# Update and install
sudo apt update
sudo apt install -y rethinkdb
```

#### CentOS/RHEL:
```bash
# Add RethinkDB repository
sudo wget https://download.rethinkdb.com/repository/centos/rethinkdb.repo -O /etc/yum.repos.d/rethinkdb.repo

# Install
sudo yum install -y rethinkdb
```

### 2. Install Redis

#### Ubuntu/Debian:
```bash
sudo apt install -y redis-server
```

#### CentOS/RHEL:
```bash
sudo yum install -y redis
# OR for newer versions
sudo dnf install -y redis
```

### 3. Install ImageMagick/GraphicsMagick
```bash
# Ubuntu/Debian
sudo apt install -y imagemagick graphicsmagick

# CentOS/RHEL
sudo yum install -y ImageMagick GraphicsMagick
```

## Python Environment Setup

### 1. Install Python 3.8+
```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip python3-venv python3-dev

# CentOS/RHEL
sudo yum install -y python3 python3-pip python3-devel
```

### 2. Create Application User
```bash
sudo useradd -m -s /bin/bash imgen
sudo usermod -aG sudo imgen  # Optional: if you need sudo access
```

### 3. Switch to Application User
```bash
sudo su - imgen
```

### 4. Create Application Directory
```bash
mkdir -p /home/imgen/app
cd /home/imgen/app
```

## Application Setup

### 1. Clone the Repository
```bash
git clone https://github.com/DankMemer/imgen.git .
```

### 2. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
# Install main requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install gunicorn (required for production deployment)
pip install gunicorn

# Install optional performance dependencies (recommended)
pip install -r optional_requirements.txt
```

**Note**: If any packages fail to install, install their system dependencies:
```bash
# For pillow-simd and image processing
sudo apt install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev

# For tensorflow
sudo apt install -y libhdf5-dev

# For moviepy (video processing)
sudo apt install -y ffmpeg
```

## Configuration

### 1. Create Configuration File
```bash
cp config.template.json config.json
```

**Alternative: Use the provided template**
The repository includes `config.template.json` with the minimum required configuration. Copy it to `config.json` and modify as needed.

### 2. Set Up Discord OAuth Application
1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to OAuth2 → General
4. Copy the Client ID and Client Secret
5. Add redirect URI: `http://your-domain.com/callback` (replace with your actual domain)

**To get your Discord User ID (for admin access):**
1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click your username and select "Copy ID"
3. Use this ID in the `admins` array in config.json

### 3. Edit Configuration File
```bash
nano config.json
```

**Complete config.json structure:**
```json
{
  "client_id": "YOUR_DISCORD_CLIENT_ID",
  "client_secret": "YOUR_DISCORD_CLIENT_SECRET",
  "admins": ["DISCORD_USER_ID_1", "DISCORD_USER_ID_2"],
  "rdb_address": "localhost",
  "rdb_port": 28015,
  "rdb_db": "imgen",
  "rdb_password": "",
  "redis_address": "localhost",
  "redis_port": 6379,
  "redis_db": 1,
  "redis_password": "",
  "max_file_size": 5000000,
  "sentry_dsn": "YOUR_SENTRY_DSN_OPTIONAL",
  "memer_token": "SPECIAL_TOKEN_FOR_PROFILE_ENDPOINT_OPTIONAL",
  "webhook_url": "DISCORD_WEBHOOK_URL_FOR_RATELIMIT_NOTIFICATIONS_OPTIONAL",
  "new_proxy": false,
  "proxies": {},
  "proxy_url": "",
  "proxy_auth": ""
}
```

**Configuration Field Explanations:**
- `client_id`, `client_secret`: Discord OAuth credentials
- `admins`: Array of Discord user IDs who have admin access
- `rdb_*`: RethinkDB connection settings
- `redis_*`: Redis connection settings
- `max_file_size`: Maximum file size for image uploads (in bytes)
- `sentry_dsn`: Optional Sentry error tracking DSN
- `memer_token`: Special token for the profile endpoint (optional)
- `webhook_url`: Discord webhook URL for rate limit notifications (optional)
- Proxy settings: Optional for routing requests through proxies

## Database Schema Setup

### 1. Start Database Services
```bash
# Start RethinkDB
sudo systemctl start rethinkdb
sudo systemctl enable rethinkdb

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis
```

### 2. Create RethinkDB Database and Tables

**Automated Setup (Recommended):**
```bash
# Use the provided database setup script
python3 setup_database.py
```

**Manual Setup:**
```bash
# Open RethinkDB shell
rethinkdb --join localhost:29015
```

In RethinkDB admin interface (http://localhost:8080) or using Python:

```python
import rethinkdb as r

# Connect to RethinkDB
conn = r.connect('localhost', 28015)

# Create database
r.db_create('imgen').run(conn)
r.db('imgen').table_create('keys').run(conn)
r.db('imgen').table_create('applications').run(conn)

# Create indexes for better performance
r.db('imgen').table('keys').index_create('owner').run(conn)
r.db('imgen').table('applications').index_create('owner').run(conn)
r.db('imgen').table('keys').index_create('creation_time').run(conn)
r.db('imgen').table('keys').index_create('total_usage').run(conn)
```

**Database Schema Details:**

**`keys` table structure:**
```javascript
{
  "id": "api_key_string",
  "name": "Application Name",
  "owner": "discord_user_id",
  "owner_name": "Username#1234",
  "email": "user@example.com",
  "total_usage": 0,
  "usages": {},  // Endpoint usage tracking
  "unlimited": false,
  "ratelimit_reached": 0,
  "creation_time": "timestamp",
  "acceptance_time": "timestamp"
}
```

**`applications` table structure:**
```javascript
{
  "id": "auto_generated",
  "owner": "discord_user_id",
  "email": "user@example.com",
  "name": "Application Name",
  "servers": "server_count",
  "description": "App description",
  "link": "http://app-website.com",
  "type": "bot/website/other",
  "email_consent": true,
  "owner_name": "Username#1234",
  "reason": "Why API access is needed",
  "time": "timestamp"
}
```

## Directory Structure Setup

### 1. Create Required Directories
```bash
mkdir -p cache/avatars
mkdir -p logs
```

### 2. Set Permissions
```bash
chmod 755 cache
chmod 755 cache/avatars
chmod 755 assets
chmod +x start.sh
```

### 3. Verify Directory Structure
Your final directory structure should look like:
```
/home/imgen/app/
├── assets/               # Image assets for endpoints
├── cache/               # Generated image cache
│   └── avatars/         # Avatar cache
├── dashboard.py         # Admin dashboard
├── endpoints/           # 80+ image generation endpoints
├── utils/              # Utility modules
├── views/              # HTML templates
├── config.json         # Your configuration
├── requirements.txt    # Python dependencies
├── server.py          # Main Flask application
├── start.sh           # Startup script
├── yeeter.py          # Cache cleanup service
└── venv/              # Python virtual environment
```

## Service Management

### 1. Install Process Manager
```bash
# Install PM2 (recommended)
sudo npm install -g pm2

# OR install supervisor
sudo apt install -y supervisor
```

### 2. Create PM2 Ecosystem File
```bash
nano ecosystem.config.js
```

```javascript
module.exports = {
  apps: [
    {
      name: 'imgen-server',
      script: 'start.sh',
      cwd: '/home/imgen/app',
      user: 'imgen',
      env: {
        'NODE_ENV': 'production'
      }
    },
    {
      name: 'imgen-yeeter',
      script: 'venv/bin/python',
      args: 'yeeter.py',
      cwd: '/home/imgen/app',
      user: 'imgen'
    }
  ]
};
```

### 3. Start Services
```bash
# With PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# OR create systemd service
sudo nano /etc/systemd/system/imgen.service
```

**Systemd service file:**
```ini
[Unit]
Description=DankMemer Image Generation Service
After=network.target rethinkdb.service redis.service

[Service]
Type=simple
User=imgen
WorkingDirectory=/home/imgen/app
Environment=PATH=/home/imgen/app/venv/bin
ExecStart=/home/imgen/app/start.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable imgen
sudo systemctl start imgen
```

## Testing the Installation

### 1. Pre-flight Dependency Check
Create a dependency check script:
```bash
nano check_dependencies.py
```

```python
#!/usr/bin/env python3
"""
Dependency checker for DankMemer/imgen
Run this script to verify all dependencies are properly installed.
"""

import sys
import subprocess

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} - OK")
        return True
    except ImportError:
        print(f"✗ {package_name} - MISSING")
        return False

def check_system_command(command):
    """Check if a system command is available."""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        print(f"✓ {command} - OK")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {command} - MISSING")
        return False

def main():
    print("DankMemer/imgen Dependency Check")
    print("=" * 40)
    
    all_good = True
    
    print("\n1. Checking Python packages...")
    python_packages = [
        ('flask', 'flask'),
        ('pillow', 'PIL'),
        ('requests', 'requests'),
        ('wand', 'wand'),
        ('rethinkdb', 'rethinkdb'),
        ('requests_oauthlib', 'requests_oauthlib'),
        ('sentry_sdk', 'sentry_sdk'),
        ('blinker', 'blinker'),
        ('moviepy', 'moviepy'),
        ('redis', 'redis'),
        ('numpy', 'numpy'),
        ('keras', 'keras'),
        ('scipy', 'scipy'),
        ('gevent', 'gevent'),
        ('tensorflow', 'tensorflow'),
        ('gunicorn', 'gunicorn'),
    ]
    
    for package, import_name in python_packages:
        if not check_python_package(package, import_name):
            all_good = False
    
    print("\n2. Checking optional packages...")
    optional_packages = [
        ('ujson', 'ujson'),
        ('hiredis', 'hiredis'),
        ('pillow-simd', None),  # Can't easily test import name
    ]
    
    for package, import_name in optional_packages:
        if import_name:
            check_python_package(package, import_name)
    
    print("\n3. Checking system commands...")
    system_commands = ['convert', 'gm', 'ffmpeg', 'rethinkdb', 'redis-cli']
    
    for command in system_commands:
        if not check_system_command(command):
            if command in ['convert', 'gm']:
                print("  Note: ImageMagick/GraphicsMagick required for image processing")
            elif command == 'ffmpeg':
                print("  Note: FFmpeg required for video processing endpoints")
            elif command == 'rethinkdb':
                print("  Note: RethinkDB required for database")
                all_good = False
            elif command == 'redis-cli':
                print("  Note: Redis required for caching and rate limiting")
                all_good = False
    
    print("\n4. Checking configuration...")
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['client_id', 'client_secret', 'admins', 'rdb_address', 'rdb_port', 'rdb_db']
        for key in required_keys:
            if key in config:
                print(f"✓ config.json has {key}")
            else:
                print(f"✗ config.json missing {key}")
                all_good = False
    except FileNotFoundError:
        print("✗ config.json not found")
        all_good = False
    except json.JSONDecodeError:
        print("✗ config.json is not valid JSON")
        all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("✓ All critical dependencies check passed!")
        print("You can now start the application with: ./start.sh")
    else:
        print("✗ Some dependencies are missing.")
        print("Please install missing packages before starting the application.")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

Run the dependency check:
```bash
chmod +x check_dependencies.py
python3 check_dependencies.py
```

### 2. Check Service Status
```bash
# PM2
pm2 status

# Systemd
sudo systemctl status imgen
sudo systemctl status rethinkdb
sudo systemctl status redis
```

### 2. Check Application Logs
```bash
# PM2
pm2 logs imgen-server

# Systemd
sudo journalctl -u imgen -f
```

### 3. Test Web Interface
```bash
curl http://localhost:65535/
```

### 4. Test API Endpoints
```bash
# Get available endpoints
curl http://localhost:65535/endpoints.json

# Test authentication (should return 401)
curl http://localhost:65535/api/deepfry
```

### 5. Access Dashboard
Visit `http://your-server-ip:65535` in a web browser and test Discord OAuth login.

## Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use
```bash
# Check what's using port 65535
sudo netstat -tulpn | grep 65535
sudo lsof -i :65535

# Kill the process or change port in start.sh
```

#### 2. Database Connection Issues
```bash
# Check RethinkDB status
sudo systemctl status rethinkdb
rethinkdb --join localhost:29015

# Check Redis status
redis-cli ping
```

#### 3. Permission Errors
```bash
# Fix ownership
sudo chown -R imgen:imgen /home/imgen/app
sudo chmod +x /home/imgen/app/start.sh
```

#### 4. Python Package Installation Failures

**Missing gunicorn:**
```bash
pip install gunicorn
```

**TensorFlow installation issues:**
```bash
# For CPU-only TensorFlow (lighter)
pip install tensorflow-cpu

# For systems with compatible GPU
pip install tensorflow
```

**Pillow-SIMD installation issues:**
```bash
# Install system dependencies first
sudo apt install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev

# Uninstall regular Pillow first
pip uninstall pillow

# Install Pillow-SIMD
pip install pillow-simd
```

**MoviePy/FFmpeg issues:**
```bash
# Install FFmpeg system package
sudo apt install -y ffmpeg

# Install imageio-ffmpeg for Python
pip install imageio-ffmpeg
```

**Wand (ImageMagick) issues:**
```bash
# Install ImageMagick development package
sudo apt install -y libmagickwand-dev

# Then install Wand
pip install Wand
```

**Complete dependency installation script:**
```bash
# System dependencies
sudo apt update
sudo apt install -y python3-dev build-essential libjpeg-dev zlib1g-dev \
    libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libhdf5-dev \
    ffmpeg imagemagick libmagickwand-dev

# Python packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn
pip install -r optional_requirements.txt
```

#### 5. ImageMagick Policy Issues
```bash
# Edit ImageMagick policy
sudo nano /etc/ImageMagick-6/policy.xml

# Comment out or modify restrictive policies
<!-- <policy domain="coder" rights="none" pattern="PDF" /> -->
```

### Log Locations
- Application logs: `pm2 logs` or `journalctl -u imgen`
- RethinkDB logs: `/var/log/rethinkdb/`
- Redis logs: `/var/log/redis/redis-server.log`
- Nginx logs (if used): `/var/log/nginx/`

## Production Considerations

### 1. Reverse Proxy Setup (Nginx)
```bash
sudo apt install -y nginx

sudo nano /etc/nginx/sites-available/imgen
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:65535;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/imgen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. SSL Certificate (Let's Encrypt)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. Firewall Configuration
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 4. Monitoring Setup
```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Consider setting up:
# - Prometheus + Grafana for metrics
# - ELK stack for log analysis
# - Uptime monitoring services
```

### 5. Backup Strategy
```bash
# Database backup script
#!/bin/bash
rethinkdb dump -c localhost:28015 -f backup_$(date +%Y%m%d_%H%M%S).tar.gz

# Set up cron job for regular backups
crontab -e
# Add: 0 2 * * * /path/to/backup/script.sh
```

### 6. Security Hardening
- Use strong passwords for all services
- Configure fail2ban for SSH protection
- Regular security updates
- Monitor for unusual activity
- Use environment variables for sensitive config
- Regular security audits

### 7. Performance Optimization
- Tune gunicorn worker count based on CPU cores
- Configure Redis memory settings
- Set up image caching strategy
- Monitor resource usage and scale accordingly
- Consider using a CDN for static assets

### 8. Scale Considerations
- Database clustering for high availability
- Load balancing for multiple app instances
- Separate cache and database servers
- Container orchestration (Docker/Kubernetes)

## API Usage Examples

### Getting an API Key
1. Visit the dashboard at your domain
2. Login with Discord
3. Request an API key through the interface
4. Wait for admin approval

### Using the API
```bash
# Basic usage
curl -H "Authorization: YOUR_API_KEY" \
     "http://your-domain.com/api/deepfry?avatar1=https://example.com/image.jpg"

# POST request
curl -X POST \
     -H "Authorization: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"avatars": ["https://example.com/image.jpg"], "text": "sample text"}' \
     "http://your-domain.com/api/meme"
```

This completes the comprehensive hosting guide for the DankMemer/imgen project. Follow these steps carefully, and you should have a fully functional image generation service running on your dedicated server.