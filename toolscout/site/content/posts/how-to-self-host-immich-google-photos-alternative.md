---
title: "How to Self-Host Immich: Your Private Google Photos Alternative"
description: "Complete guide to self-hosting Immich with Docker. Backup photos from your phone, AI face recognition, and zero cloud storage fees. Full setup in 20 minutes."
date: 2026-04-13T06:50:00+02:00
draft: false
slug: "how-to-self-host-immich-google-photos-alternative"
categories: ["how-to guides"]
tags: ["immich", "google photos", "self-hosting", "docker", "privacy", "photos"]
author: "Scout"
---

# How to Self-Host Immich: Your Private Google Photos Alternative

Google Photos works well. It's free, syncs reliably, and finds photos when you search. But your entire visual history sits on Google's servers—faces, locations, events, relationships. All of it.

Immich gives you the same core features—automatic backup, face recognition, smart search—on hardware you control. About $5/month for a VPS. Your photos stay yours.

This guide gets you running in 20 minutes.

## What Immich Actually Is

Immich is open-source photo and video backup software. You run it on your own server (or home machine). It handles:

- Automatic phone backup (iOS and Android)
- Local AI face recognition
- Object/scene detection
- Map view with GPS clustering
- Shared albums
- Full-text search
- RAW support
- Timeline view

The project started in 2022 and releases updates regularly. v1.118.0 is current as of April 2026.

## The Real Trade-off

| Factor | Google Photos | Immich Self-Hosted |
|--------|---------------|-------------------|
| **Data ownership** | Google | You |
| **AI training** | Your photos train Google's models | Local models only |
| **Storage cost** | Free (compressed) or $20/year/100GB | ~$5/month VPS |
| **Face recognition** | Google's servers process faces | Local processing |
| **Location data** | Feeds Google Maps | Stays on your server |
| **Maintenance** | None | You manage updates |

You trade convenience for control. Whether that's worth it depends on your threat model.

## What You'll Need

**Hardware:**
- 4 CPU cores (ARM64 or x86)
- 8GB RAM minimum, 12GB recommended
- 100GB+ SSD storage

**Why so much RAM?** The AI features (face recognition, object detection) run ML models locally. They need memory.

**Software:**
- Docker and Docker Compose
- A domain name (optional but recommended)
- Basic Linux command line comfort

## Step 1: Server Setup

SSH into your server and update:

```bash
sudo apt update && sudo apt upgrade -y
```

Install Docker:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

Verify Docker works:

```bash
docker --version
```

## Step 2: Docker Compose Setup

Create a directory:

```bash
mkdir ~/immich && cd ~/immich
```

Download the official compose file (v1.118.0):

```bash
wget https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
```

Download the example environment file:

```bash
wget -O .env https://github.com/immich-app/immich/releases/latest/download/example.env
```

## Step 3: Configure Environment

Edit `.env`:

```bash
nano .env
```

Set these values:

```env
# Database
DB_PASSWORD=your_secure_random_password

# Storage
UPLOAD_LOCATION=./library

# Server URL (change to your domain)
PUBLIC_IMMICH_SERVER_URL=https://photos.yourdomain.com
```

Generate a strong password:

```bash
openssl rand -base64 32
```

## Step 4: Start Immich

Launch:

```bash
docker compose up -d
```

Check if containers are running:

```bash
docker ps
```

You should see: `immich_server`, `immich_microservices`, `immich_machine_learning`, `redis`, and `postgres`.

View logs if something fails:

```bash
docker logs immich_server -f
```

Wait for "Immich Server is listening" before proceeding.

## Step 5: Initial Configuration

Access your instance at `http://YOUR_SERVER_IP:2283`.

First-run setup:
1. Create admin account
2. Set thumbnail quality (I use 720p for web, original for archive)
3. Enable machine learning features
4. Configure backup settings

## Step 6: Add SSL with Nginx

For production, use a reverse proxy. Install Nginx:

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

Create config:

```bash
sudo nano /etc/nginx/sites-available/immich
```

Add:

```nginx
server {
    listen 80;
    server_name photos.yourdomain.com;

    client_max_body_size 50000M;

    location / {
        proxy_pass http://localhost:2283;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable and add SSL:

```bash
sudo ln -s /etc/nginx/sites-available/immich /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d photos.yourdomain.com
```

## Step 7: Mobile App Setup

Download:
- **iOS**: App Store
- **Android**: Play Store or F-Droid

Configuration:
1. Server URL: `https://photos.yourdomain.com`
2. Login with your admin credentials
3. Enable auto-backup (WiFi-only recommended)
4. Select albums to backup

The app backs up in background. First sync takes time depending on library size.

## AI Features: What Actually Works

Once photos are uploaded:

**Face Recognition**
Groups faces automatically. You name people, it finds more. Accuracy is good, not perfect. Works entirely offline.

**Object Detection**
Search "dog", "beach", "birthday"—it finds matches. Sometimes misses, sometimes false positives. Useful but not magic.

**CLIP Search**
Natural language search. "Sunset at beach" actually works surprisingly well. Depends on model quality.

**Map View**
Photos clustered by GPS. Useful for travel memories. Requires location data in EXIF.

## Storage Reality Check

Immich stores:
- Original files (largest)
- Thumbnails (configurable quality)
- Web-optimized videos
- Face recognition database
- Search index

**Rule of thumb:** Budget 1.5-2x your raw photo storage. 100GB of photos = 150-200GB on server.

**Cost optimization:**
- Use external storage (S3, Wasabi) for originals
- Keep thumbnails local for speed
- Set up automatic deletion of originals after backup verification

## Backing Up Immich Itself

Your photos aren't safe without backups. Immich stores data in two places:

1. **Upload directory** (`./library` by default)
2. **PostgreSQL database**

Backup script:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=/backup/immich

# Backup database
docker exec immich_postgres pg_dump -U postgres immich > $BACKUP_DIR/db-$DATE.sql

# Backup library
tar czf $BACKUP_DIR/library-$DATE.tar.gz ~/immich/library

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Run nightly via cron. Store backups offsite (S3, another server, external drive).

## Common Problems

**"Out of memory" crashes**
The ML container is greedy. Solutions:
- Add swap: `sudo fallocate -l 4G /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`
- Upgrade to 12GB+ RAM
- Disable machine learning temporarily in settings

**Slow uploads**
- Check Nginx `client_max_body_size` (set to 50000M)
- Verify you're on SSD, not HDD
- Try upload during off-peak hours

**Face recognition not working**
- Check `immich_machine_learning` container is running: `docker ps`
- Check logs: `docker logs immich_machine_learning`
- Initial scan takes hours for large libraries—be patient

**App won't connect**
- SSL certificate must be valid (no self-signed)
- Firewall must allow 443
- `PUBLIC_IMMICH_SERVER_URL` must match your domain exactly

## Performance Tuning

For 50,000+ photos:

**PostgreSQL tuning** (add to docker-compose environment):
```yaml
environment:
  POSTGRES_INITDB_ARGS: '--encoding=UTF-8'
```

**Hardware acceleration** (Intel GPUs):
```yaml
immich-machine-learning:
  devices:
    - /dev/dri:/dev/dri
```

**Separate storage:**
Mount external storage for `./library` if local disk is small.

## The Honest Assessment

Immich isn't perfect. Setup requires technical knowledge. AI features need real hardware. Mobile apps aren't as polished as Google's.

But it works. Your photos stay on your server. No terms-of-service changes. No AI training on your memories. No "free" service that disappears.

For $5/month and an afternoon of setup, that's a fair trade.

---

*Questions about the setup? Immich has active Discord and GitHub communities for troubleshooting.*
