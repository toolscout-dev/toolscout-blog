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

Notion works well. Your notes live on their servers. If that bothers you, AFFiNE is an alternative.

Open source. Self-hostable. Combines documents, whiteboards, databases. This guide gets you running in 10 minutes.

## What AFFiNE Is

AFFiNE (pronounced "a-fine") is an open-source workspace. Documents like Notion. Whiteboards like Miro. Self-hostable.

40,000+ GitHub stars. Active development. v0.18.0 current as of April 2026.

## Why Self-Host?

- Data stays on your infrastructure
- No subscription fees
- Use your own AI keys (Claude, OpenAI, Gemini)
- Compliance requirements
- Modify code if needed

## Requirements

- Docker and Docker Compose
- 2GB RAM (4GB recommended)
- 10GB disk space
- Basic command line knowledge

## Step 1: Create Directory

```bash
mkdir affine-selfhosted
cd affine-selfhosted
```

## Step 2: Download Docker Compose

```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/toeverything/AFFiNE/stable/.docker/selfhost/compose.yml
```

Or create manually:

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

## Step 3: Configure Environment

Create `.env`:

```bash
# Database
DB_USERNAME=affine
DB_PASSWORD=your_secure_password_here
DB_DATABASE=affine
DB_DATA_LOCATION=./postgres_data

# Storage
UPLOAD_LOCATION=./storage
CONFIG_LOCATION=./config

# AFFiNE
AFFINE_REVISION=stable
PORT=3010
```

Generate password:

```bash
openssl rand -base64 32
```

## Step 4: Launch

```bash
docker compose up -d
```

First startup takes 2-3 minutes. Check logs:

```bash
docker compose logs -f affine
```

Wait for "Server is running on http://localhost:3010".

## Step 5: Access

Open browser:

```
http://localhost:3010
```

Or server IP:

```
http://your-server-ip:3010
```

## Step 6: Setup

1. Create admin account
2. Choose workspace name
3. Start creating

## Optional: Enable AI

Add to `.env`:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Or Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or Gemini
GOOGLE_API_KEY=your-key-here
```

Restart:

```bash
docker compose restart
```

## Production: Reverse Proxy

Nginx example:

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

## Backups

Data locations:
- `./postgres_data` - Database
- `./storage` - Files
- `./config` - Configuration

Backup script:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "/backups/affine_${DATE}.tar.gz" ./postgres_data ./storage ./config
```

## Updates

```bash
docker compose pull
docker compose up -d
```

## Troubleshooting

**Port 3010 in use:**
Change in `.env`: `PORT=3011`

**Permission errors:**
```bash
chmod -R 777 ./postgres_data ./storage
```

**Database errors:**
Check postgres health: `docker compose ps`

## Notion Import

1. Export Notion as Markdown + CSV
2. AFFiNE: Settings → Import
3. Upload files

Complex databases need manual adjustment.

## Summary

10 minutes. Private Notion alternative. No subscription. No data mining.

AFFiNE isn't perfect. Self-hosting requires maintenance. But you control your data.

---

*AFFiNE v0.18.0 tested. Setup verified April 2026.*
