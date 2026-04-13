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

Google Photos knows more about your life than your therapist. Every photo you've taken, every face you know, every location you've visited—it's all in their cloud, feeding their AI, their ads, their data machine.

Immich gives you the same experience—automatic phone backup, AI face recognition, smart search—without surrendering your memories to Big Tech. And it costs about $5/month to host.

This guide gets you from zero to private photo cloud in 20 minutes.

## What Is Immich?

Immich is an open-source, self-hosted photo and video backup solution. Think Google Photos, but you own the infrastructure, the data, and the AI models.

**Key features:**
- Automatic mobile backup (iOS and Android)
- AI face recognition and grouping
- Object and scene detection
- Map view with GPS clustering
- Shared albums
- Full-text search
- RAW format support
- Timeline view

It's actively developed, has a thriving community, and improves monthly.

## The Privacy Math

| Factor | Google Photos | Immich Self-Hosted |
|--------|---------------|-------------------|
| **Who owns your data** | Google | You |
| **AI training** | Your photos train Google's models | Local models, no external sharing |
| **Storage cost** | Free (compressed) or $20/year/100GB | ~$5/month VPS for unlimited |
| **Face recognition** | Google sees everyone you know | Stays on your server |
| **Location history** | Google Maps integration | Private to you |

The trade-off? You manage the server. For privacy-conscious users, that's a feature, not a bug.

## Prerequisites

Before starting, you'll need:

1. **A VPS or server** with:
   - 4 CPU cores (ARM64 or x86)
   - 8GB RAM minimum (12GB recommended)
   - 100GB+ storage (SSD strongly recommended)

2. **Docker and Docker Compose** installed

3. **A domain name** (optional but recommended)

4. **Basic command line knowledge**

**Why the beefy specs?** AI features (face recognition, object detection) run machine learning models locally. They need RAM and CPU.

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

Install Docker Compose:

```bash
sudo apt install docker-compose-plugin -y
```

## Step 2: Create the Docker Compose File

Create a directory for Immich:

```bash
mkdir ~/immich && cd ~/immich
```

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:release
    command: ['start.sh', 'immich']
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
    env_file:
      - .env
    ports:
      - 2283:3001
    depends_on:
      - redis
      - database
    restart: always

  immich-microservices:
    container_name: immich_microservices
    image: ghcr.io/immich-app/immich-server:release
    command: ['start.sh', 'microservices']
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
    env_file:
      - .env
    depends_on:
      - redis
      - database
    restart: always

  immich-machine-learning:
    container_name: immich_machine_learning
    image: ghcr.io/immich-app/immich-machine-learning:release
    volumes:
      - model-cache:/cache
    env_file:
      - .env
    restart: always

  redis:
    container_name: immich_redis
    image: redis:6.2-alpine
    restart: always

  database:
    container_name: immich_postgres
    image: tensorchord/pgvecto-rs:pg14-v0.2.0
    env_file:
      - .env
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: always

volumes:
  pgdata:
  model-cache:
```

## Step 3: Configure Environment Variables

Create `.env` file:

```bash
nano .env
```

Add:

```env
# Database
DB_HOSTNAME=immich_postgres
DB_USERNAME=postgres
DB_PASSWORD=your_secure_password_here
DB_DATABASE_NAME=immich

# Redis
REDIS_HOSTNAME=immich_redis

# Upload location
UPLOAD_LOCATION=./library

# Server URL
PUBLIC_IMMICH_SERVER_URL=https://photos.yourdomain.com
IMMICH_SERVER_URL=http://immich-server:3001

# Web
IMMICH_WEB_URL=http://immich-web:3000

# Machine learning
MACHINE_LEARNING_HOST=0.0.0.0
MACHINE_LEARNING_PORT=3003
```

Replace `your_secure_password_here` with a strong password and `photos.yourdomain.com` with your domain.

## Step 4: Start Immich

Launch the stack:

```bash
docker compose up -d
```

Check logs to ensure everything starts:

```bash
docker logs immich_server -f
```

Wait for "Immich Server is listening" message.

## Step 5: Initial Setup

Access your instance:

```
http://YOUR_SERVER_IP:2283
```

First run:
1. Create an admin account
2. Set up your library settings
3. Configure thumbnail quality
4. Enable machine learning features

## Step 6: Add SSL with Nginx

For production, use Nginx as a reverse proxy:

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

Create Nginx config:

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

Enable SSL:

```bash
sudo ln -s /etc/nginx/sites-available/immich /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d photos.yourdomain.com
```

## Step 7: Mobile App Setup

Download the Immich app:
- **iOS**: App Store
- **Android**: Play Store or F-Droid

Configure:
1. Enter your server URL (`https://photos.yourdomain.com`)
2. Log in with your credentials
3. Enable automatic backup
4. Choose backup settings (WiFi only, include videos, etc.)

The app backs up photos in the background, just like Google Photos.

## Step 8: Explore AI Features

Once photos are uploaded, Immich's AI kicks in:

**Face Recognition**
Automatically groups faces. Name people to search for them later.

**Object Detection**
Search for "dog," "beach," "birthday"—Immich finds matching photos.

**CLIP Search**
Type "sunset at the beach" and find relevant images, even without tags.

**Map View**
Photos clustered by GPS location. Explore your travels visually.

## Storage Management

Immich stores:
- Original photos/videos
- Thumbnails (configurable quality)
- Encoded videos (for web playback)
- Face recognition data

**Storage tips:**
- Use external storage (S3, NFS) for large libraries
- Set up automatic cleanup of originals after backup
- Monitor disk space with `df -h`

## Backing Up Your Immich Server

Your photos are only safe if you back them up:

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar czf /backup/immich-$DATE.tar.gz ~/immich/library
```

Store backups offsite (S3, another server, external drive).

## Troubleshooting

**Out of memory errors**
Immich's AI features are RAM-hungry. If containers crash:
- Add swap: `sudo fallocate -l 4G /swapfile`
- Upgrade your VPS to 12GB+ RAM
- Disable machine learning temporarily

**Slow uploads**
- Check Nginx `client_max_body_size`
- Verify disk I/O isn't bottlenecked
- Use SSD storage, not HDD

**Face recognition not working**
- Ensure `immich_machine_learning` container is running
- Check logs: `docker logs immich_machine_learning`
- First scan takes time for large libraries

**Mobile app won't connect**
- Verify SSL certificate is valid (self-signed won't work)
- Check firewall allows port 443
- Ensure `PUBLIC_IMMICH_SERVER_URL` is set correctly

## Performance Optimization

For large libraries (50,000+ photos):

1. **Use PostgreSQL tuning**:
   ```env
   DB_URL=postgresql://postgres:password@immich_postgres:5432/immich?sslmode=disable
   ```

2. **Enable hardware acceleration** (if available):
   ```yaml
   immich-machine-learning:
     devices:
       - /dev/dri:/dev/dri  # Intel GPU
   ```

3. **Separate storage**:
   Mount external storage for the library directory

## The Bottom Line

Immich isn't perfect. Setup requires technical knowledge. AI features need serious hardware. Mobile apps aren't as polished as Google's.

But you know what? Your photos stay yours. No AI training on your memories. No algorithmic timeline manipulation. No "free" service that changes terms next year.

For $5/month and 20 minutes of setup, that's a trade worth making.

---

*Self-hosting Immich? Questions about the setup? Drop them in the comments.*
