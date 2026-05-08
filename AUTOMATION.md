# AUTOMATION.md — ToolScout Daily Publishing

## Overview
Automatic article publishing every day at **07:00 CET**.

## How It Works

### OpenClaw Heartbeat System
Il file `.openclaw/heartbeat.json` nel workspace configura l'automazione:
- **Schedule**: Ogni giorno alle 07:00 CET (`0 7 * * *`)
- **Trigger**: OpenClaw invia un heartbeat message all'agent
- **Action**: L'agent esegue la pipeline completa

### Pipeline (10 Steps)
1. 📖 Read HEARTBEAT.md + LESSONS.md
2. 🔍 Find keyword (Brave Search)
3. 📚 Research 3-5 sources
4. ✍️ Write 1200-1800 words
5. ✅ **QUALITY GATE** — Abort if not perfect
6. 🔨 Build Hugo
7. 🚀 Deploy Cloudflare
8. 📦 Git commit/push
9. 📝 Update tracking files
10. 📱 Notify Michael on Telegram

### Notification Flow
```
07:00 CET — Heartbeat triggers
    ↓
🌅 "ToolScout Daily Publisher Activated"
    ↓
🔍 "Found keyword: [keyword]"
    ↓
✍️ "Writing: [title]"
    ↓
✅ "Quality gate passed"
    ↓
🚀 "Deployed: [URL]"
    ↓
📊 "Published: [title] — [URL]"
```

## Quality Gates (Auto-Abort)
- ❌ Keyword troppo competitiva
- ❌ < 3 fonti di ricerca
- ❌ Articolo < 1200 parole
- ❌ Suona "AI-generated"
- ❌ Errori build/deploy

**Quando aborto:** "⛔ Aborted: [reason]. Retry tomorrow."

## Files
| File | Purpose |
|------|---------|
| `.openclaw/heartbeat.json` | Configurazione schedule |
| `HEARTBEAT.md` | Istruzioni pipeline |
| `daily-logs/YYYY-MM-DD.md` | Log esecuzione |
| `.learnings/ERRORS.md` | Tracking errori |

## Manual Override
Per eseguire manualmente:
```
Invia messaggio a @toolscout: "publish now"
```

Per saltare un giorno:
```
Invia messaggio a @toolscout: "skip today"
```

## Protezioni Attive
- ✅ Gateway NON viene mai riavviato
- ✅ openclaw.json NON viene modificato
- ✅ Qualità > Quantità sempre
- ✅ Notifiche complete su ogni step
