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

Zapier's pricing is a trap. Start free, then watch your bill explode as your business grows. 10,000 tasks? That's $193/month. 50,000 tasks? $769/month. n8n gives you the same power—unlimited workflows, AI integration, 400+ apps—for the cost of a cheap VPS.

This guide gets you from zero to self-hosted automation in 15 minutes.

## What Is n8n?

n8n (pronounced "n-eight-n") is an open-source workflow automation platform. Think Zapier or Make, but you control the infrastructure, the data, and the pricing.

Key features:
- **400+ integrations** (Slack, Notion, Google Sheets, OpenAI, etc.)
- **AI-native**: Build LangChain-powered AI agents
- **Code when you need it**: Write JavaScript/Python or use the visual builder
- **Fair-code license**: Self-host for free, pay only for enterprise features
- **900+ workflow templates** to get started fast

## Why Self-Host Instead of Cloud?

| Factor | n8n Cloud Pro | Self-Hosted |
|--------|---------------|-------------|
| **Price** | $50/month | $5-15/month VPS |
| **Executions** | 50,000/month | Unlimited |
| **Data Control** | n8n hosts it | You own everything |
| **Custom Code** | ✅ | ✅ |
| **AI Model Choice** | Limited | Any (Ollama, local LLMs) |

Self-hosting means no execution limits, no vendor lock-in, and the ability to connect to internal systems Zapier can't touch.

## Prerequisites

Before starting, you'll need:

1. **A VPS or server** (DigitalOcean, Hetzner, AWS, or even a homelab)
   - Minimum: 2 CPU cores, 4GB RAM, 20GB SSD
   - Recommended: 2 CPU cores, 8GB RAM for AI workloads

2. **Docker and Docker Compose** installed

3. **A domain name** (optional but recommended for SSL)

4. **Basic command line knowledge**

## Step 1: Server Setup

Spin up a VPS with Ubuntu 22.04. SSH in and update:

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

## Step 2: Docker Compose Configuration

Create a directory for n8n:

```bash
mkdir ~/n8n && cd ~/n8n
```

Create a `docker-compose.yml` file:

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
    volumes:
      - n8n_data:/home/node/.n8n
      - /local-files:/files

volumes:
  n8n_data:
```

Replace:
- `your-username` and `your-secure-password` with your credentials
- `n8n.yourdomain.com` with your actual domain (or use your IP for testing)

## Step 3: Start n8n

Launch the container:

```bash
docker compose up -d
```

Check logs to ensure it's running:

```bash
docker logs n8n-n8n-1 -f
```

Wait for "Editor is now accessible via" message.

## Step 4: Access Your Instance

If you don't have a domain yet, access n8n via:

```
http://YOUR_SERVER_IP:5678
```

Log in with the credentials you set in the compose file.

## Step 5: Add SSL with Nginx (Recommended)

For production, use Nginx as a reverse proxy with Let's Encrypt:

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

Create an Nginx config:

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

Enable the site and get SSL:

```bash
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d n8n.yourdomain.com
```

Update your `docker-compose.yml`:

```yaml
environment:
  - N8N_HOST=n8n.yourdomain.com
  - N8N_PORT=5678
  - N8N_PROTOCOL=https
  - WEBHOOK_URL=https://n8n.yourdomain.com/
```

Restart:

```bash
docker compose down && docker compose up -d
```

## Step 6: Your First Workflow

Let's build a simple automation: "When I star an email in Gmail, add it to a Notion database."

1. Click **Add Workflow**
2. Add a **Gmail** trigger node
3. Set trigger to "Message Starred"
4. Add a **Notion** node
5. Configure it to create a database entry
6. Connect the nodes
7. Click **Execute Workflow** to test
8. Activate to run automatically

n8n's visual builder makes this intuitive—drag, drop, connect.

## Step 7: Add AI Capabilities

n8n integrates with LangChain for AI workflows. Connect:

- **OpenAI** (GPT-4, GPT-3.5)
- **Ollama** (self-hosted LLMs)
- **Vector databases** (Pinecone, Supabase)

Example AI workflow: "Summarize new support tickets and post to Slack."

1. **Trigger**: New email in support@ inbox
2. **OpenAI node**: Summarize content
3. **Slack node**: Post summary to #support channel

## Troubleshooting

### Container won't start

Check logs:
```bash
docker logs n8n-n8n-1
```

Common issues:
- Port 5678 already in use: Change the port mapping in docker-compose.yml
- Permission errors: Ensure the n8n_data volume has correct permissions

### Webhooks not working

Ensure `WEBHOOK_URL` is set correctly in your environment variables. It must match your public URL.

### Out of memory

n8n can be memory-intensive with AI workflows. Upgrade your VPS or add swap:

```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Database corruption

Always back up your volume:

```bash
docker run --rm -v n8n_n8n_data:/data -v ~/backups:/backup alpine tar czf /backup/n8n-backup-$(date +%Y%m%d).tar.gz -C /data .
```

## Security Best Practices

1. **Change default credentials** immediately
2. **Use strong passwords** for basic auth
3. **Enable 2FA** in n8n settings
4. **Restrict firewall** to necessary ports (80, 443)
5. **Keep n8n updated**:
   ```bash
   docker compose pull && docker compose up -d
   ```
6. **Regular backups** of the n8n_data volume

## Scaling Up

For high-volume workflows:

1. **Use an external database** (PostgreSQL instead of SQLite):
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

2. **Enable queue mode** for multiple workers
3. **Use Redis** for caching

## The Bottom Line

Self-hosting n8n takes 15 minutes to set up and saves you thousands as you scale. A $5 DigitalOcean droplet handles most small business needs. Compare that to Zapier's $193/month for 10,000 tasks.

The trade-off? You manage the infrastructure. But with Docker, it's mostly hands-off. Updates are one command. Backups are automated. And you own your data.

Start with the basic Docker setup above. Once you're comfortable, explore AI workflows, custom nodes, and advanced integrations. n8n grows with you—without the per-task tax.

---

*Questions about self-hosting n8n? Stuck on a step? Drop a comment below.*
