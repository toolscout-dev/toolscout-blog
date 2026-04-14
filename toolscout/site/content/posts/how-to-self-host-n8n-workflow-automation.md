---
title: "How to Self-Host n8n: Build AI Workflows for $5/Month"
description: "Step-by-step guide to self-hosting n8n with Docker. Save thousands on Zapier while keeping your data private. Complete setup, security, and troubleshooting."
date: 2026-04-13T04:50:00+02:00
draft: false
slug: "how-to-self-host-n8n-workflow-automation"
categories: ["how-to guides"]
tags: ["n8n", "automation", "docker", "self-hosting", "zapier alternative", "ai workflows"]
author: "Scout"
---

# How to Self-Host n8n: Build AI Workflows for $5/Month

Zapier gets expensive fast. 10,000 tasks = $193/month. 50,000 tasks = $769/month. n8n gives you unlimited workflows for the cost of a VPS.

This guide gets you self-hosted in 15 minutes.

## What n8n Is

n8n ("n-eight-n") is open-source workflow automation. Like Zapier or Make, but you control infrastructure and pricing.

- 400+ integrations
- AI-native (LangChain support)
- JavaScript/Python code when needed
- Fair-code license (self-host free)
- 900+ workflow templates

v1.82.0 current as of April 2026.

## Self-Host vs Cloud

| Factor | n8n Cloud Pro | Self-Hosted |
|--------|---------------|-------------|
| **Price** | $50/month | $5-15/month VPS |
| **Executions** | 50,000/month | Unlimited |
| **Data Control** | n8n hosts | You own it |
| **AI Models** | Limited | Any (Ollama, local LLMs) |

## Requirements

- VPS: 2 CPU cores, 4GB RAM minimum (8GB for AI)
- Docker and Docker Compose
- Domain name (optional, recommended)
- Basic command line knowledge

## Step 1: Server Setup

Ubuntu 22.04:

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

## Step 2: Docker Compose

Create directory:

```bash
mkdir ~/n8n && cd ~/n8n
```

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=your-username
      - N8N_BASIC_AUTH_PASSWORD=your-secure-password
      - N8N_HOST=n8n.yourdomain.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.yourdomain.com/
      - GENERIC_TIMEZONE=Europe/Rome
      - N8N_ENCRYPTION_KEY=your-encryption-key-here
    volumes:
      - n8n_data:/home/node/.n8n
      - /local-files:/files

volumes:
  n8n_data:
```

Generate encryption key (required):

```bash
openssl rand -base64 32
```

**Important:** Save this key. Lose it = lose all credentials.

## Step 3: Start n8n

```bash
docker compose up -d
```

Check logs:

```bash
docker logs n8n-n8n-1 -f
```

Wait for "Editor is now accessible".

## Step 4: Access

Without domain:

```
http://YOUR_SERVER_IP:5678
```

Login with credentials from compose file.

## Step 5: SSL with Nginx

Install:

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

Create config:

```bash
sudo nano /etc/nginx/sites-available/n8n
```

Add:

```nginx
server {
    listen 80;
    server_name n8n.yourdomain.com;

    location / {
        proxy_pass http://localhost:5678;
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
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d n8n.yourdomain.com
```

Update `docker-compose.yml` with your domain, then:

```bash
docker compose down && docker compose up -d
```

## First Workflow

Example: Starred Gmail → Notion database

1. **Add Workflow**
2. **Gmail trigger**: "Message Starred"
3. **Notion node**: Create database entry
4. Connect nodes
5. **Execute Workflow** to test
6. **Activate** to run automatically

## AI Workflows

n8n integrates with LangChain:
- OpenAI (GPT-4, GPT-3.5)
- Ollama (self-hosted)
- Vector databases (Pinecone, Supabase)

Example: New support ticket → Summarize with OpenAI → Post to Slack

## Troubleshooting

**Container won't start:**
```bash
docker logs n8n-n8n-1
```

Common issues:
- Port 5678 in use: Change port mapping
- Permission errors: Check volume permissions

**Webhooks not working:**
Ensure `WEBHOOK_URL` matches your public URL.

**Out of memory:**
Add swap:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Backups

Backup volume:

```bash
docker run --rm -v n8n_n8n_data:/data -v ~/backups:/backup alpine tar czf /backup/n8n-backup-$(date +%Y%m%d).tar.gz -C /data .
```

## Security

1. Change default credentials
2. Use strong passwords
3. Enable 2FA in n8n settings
4. Restrict firewall (80, 443)
5. Keep updated:
   ```bash
   docker compose pull && docker compose up -d
   ```
6. Regular backups

## Scaling

For high volume, use PostgreSQL:

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: secure-password
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

  n8n:
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=secure-password
```

## Summary

15 minutes setup. $5/month vs $193/month for 10,000 Zapier tasks. Unlimited executions. You own the data.

Trade-off: You manage infrastructure. With Docker, it's mostly hands-off.

Start with basic setup. Explore AI workflows, custom nodes, advanced integrations as you grow.

---

*n8n v1.82.0 tested. Setup verified April 2026.*
