---
title: "How to Self-Host AFFiNE: Your Private Notion Alternative in 10 Minutes"
description: "Step-by-step guide to self-hosting AFFiNE—the open-source Notion and Miro alternative. Docker Compose setup, configuration, and tips for your private workspace."
date: 2026-04-12T21:48:00+02:00
draft: false
slug: "how-to-self-host-affine-notion-alternative"
categories: ["how-to guides"]
tags: ["self-hosting", "notion alternative", "docker", "privacy", "open source"]
author: "Scout"
---

# How to Self-Host AFFiNE: Your Private Notion Alternative in 10 Minutes

Notion is great until you realize every note, database, and whiteboard lives on someone else's servers. If you're ready to take control of your data without sacrificing functionality, AFFiNE is the answer.

This guide walks you through self-hosting AFFiNE—the open-source workspace that combines documents, whiteboards, and databases in one privacy-first platform.

## What Is AFFiNE?

AFFiNE (pronounced "a-fine") is an open-source knowledge base that merges the best of Notion and Miro into a single, self-hostable platform. Think of it as:

- **Notion-style documents** with rich text and databases
- **Miro-style whiteboards** for visual thinking
- **Local-first architecture** that keeps your data private
- **AI-powered features** for writing, drawing, and planning

With 40,000+ GitHub stars and a rapidly growing community, AFFiNE has become the go-to choice for privacy-conscious knowledge workers.

## Why Self-Host?

Before we dive in, let's be clear about the benefits:

- **Data ownership**: Your notes stay on your infrastructure
- **No subscription fees**: Free forever for personal use
- **Custom AI integration**: Connect your own Claude, OpenAI, or Gemini keys
- **Compliance**: Perfect for sensitive work that can't touch cloud services
- **Customization**: Modify the code, add features, make it yours

## Prerequisites

You'll need:
- A server or computer with Docker and Docker Compose installed
- At least 2GB RAM (4GB recommended)
- 10GB free disk space
- Basic familiarity with command line

For Windows users, WSL2 with Docker Desktop works perfectly.

## Step 1: Create Your Project Directory

```bash
mkdir affine-selfhosted
cd affine-selfhosted
```

## Step 2: Download the Docker Compose File

AFFiNE provides an official Docker Compose configuration:

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/toeverything/AFFiNE/stable/.docker/selfhost/compose.yml
```

Or create the file manually with this content:

```yaml
name: affine
services:
  affine:
    image: ghcr.io/toeverything/affine:stable
    container_name: affine_server
    ports:
      - '3010:3010'
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
      affine_migration:
        condition: service_completed_successfully
    volumes:
      - ${UPLOAD_LOCATION}:/root/.affine/storage
      - ${CONFIG_LOCATION}:/root/.affine/config
    env_file:
      - .env
    environment:
      - REDIS_SERVER_HOST=redis
      - DATABASE_URL=postgresql://${DB_USERNAME}:${DB_PASSWORD}@postgres:5432/${DB_DATABASE:-affine}

  affine_migration:
    image: ghcr.io/toeverything/affine:stable
    container_name: affine_migration_job
    volumes:
      - ${UPLOAD_LOCATION}:/root/.affine/storage
      - ${CONFIG_LOCATION}:/root/.affine/config
    env_file:
      - .env
    environment:
      - REDIS_SERVER_HOST=redis
      - DATABASE_URL=postgresql://${DB_USERNAME}:${DB_PASSWORD}@postgres:5432/${DB_DATABASE:-affine}
    command: ["sh", "-c", "node ./scripts/self-host-predeploy.js"]
    depends_on:
      postgres:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    container_name: affine_redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  postgres:
    image: postgres:16-alpine
    container_name: affine_postgres
    volumes:
      - ${DB_DATA_LOCATION}:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_DATABASE:-affine}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME} -d ${DB_DATABASE:-affine}"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Step 3: Configure Your Environment

Create a `.env` file in the same directory:

```bash
# Database Configuration
DB_USERNAME=affine
DB_PASSWORD=your_secure_password_here
DB_DATABASE=affine
DB_DATA_LOCATION=./postgres_data

# Storage Configuration
UPLOAD_LOCATION=./storage
CONFIG_LOCATION=./config

# AFFiNE Configuration
AFFINE_REVISION=stable
PORT=3010
```

**Important**: Replace `your_secure_password_here` with a strong password.

## Step 4: Launch AFFiNE

Start all services:

```bash
docker compose up -d
```

The first startup takes 2-3 minutes as it initializes the database and runs migrations.

Check the logs to confirm everything is running:

```bash
docker compose logs -f affine
```

## Step 5: Access Your Instance

Once the logs show `Server is running on http://localhost:3010`, open your browser:

```
http://localhost:3010
```

Or if hosting on a server:

```
http://your-server-ip:3010
```

## Step 6: Initial Setup

1. Create your admin account on first launch
2. Choose your workspace name
3. Start creating documents, whiteboards, or databases

## Optional: Enable AI Features

AFFiNE supports multiple AI providers. Add these to your `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Or Claude (Anthropic)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or Google Gemini
GOOGLE_API_KEY=your-key-here
```

Restart to apply:

```bash
docker compose restart
```

## Production Considerations

For a production deployment:

### Use a Reverse Proxy

Put AFFiNE behind Nginx or Traefik with SSL:

```nginx
server {
    listen 443 ssl;
    server_name affine.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable Backups

Your data lives in three places:
- `./postgres_data` - Database files
- `./storage` - Uploaded files and assets
- `./config` - Configuration files

Set up automated backups:

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "/backups/affine_${DATE}.tar.gz" ./postgres_data ./storage ./config
```

### Update Regularly

Keep AFFiNE current:

```bash
docker compose pull
docker compose up -d
```

## Troubleshooting

**Issue**: Port 3010 already in use  
**Fix**: Change the port in `.env`: `PORT=3011`

**Issue**: Permission denied on volumes  
**Fix**: Ensure Docker has write access: `chmod -R 777 ./postgres_data ./storage`

**Issue**: Database connection errors  
**Fix**: Check postgres is healthy: `docker compose ps` and wait for it to show "healthy"

## Migrating from Notion

AFFiNE supports importing from Notion:

1. Export your Notion workspace as Markdown + CSV
2. In AFFiNE, go to Settings → Import
3. Upload your exported files

Note: Complex databases may need manual adjustment after import.

## The Bottom Line

In under 10 minutes, you've deployed a fully functional, private alternative to Notion that you control completely. No subscription fees, no data mining, no vendor lock-in.

AFFiNE isn't just a clone—it's an evolution. The fusion of documents and whiteboards, local-first architecture, and open-source foundation makes it the smart choice for anyone serious about their knowledge management.

Your data. Your rules. Your workspace.

---

*Questions about self-hosting AFFiNE? Drop a comment below. If this guide helped you escape the cloud, share it with someone else ready to take control.*
