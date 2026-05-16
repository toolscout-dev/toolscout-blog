# HEARTBEAT — ToolScout Autonomous Pipeline

## Timezone
Europe/Rome (CET)

## Schedule
**Daily at 07:00 CET** — Automatic article publication

## Pre-Flight Checklist (BEFORE writing)
1. Read LESSONS.md — apply all learnings
2. Check keywords.json — avoid duplicates
3. Verify yesterday's article performed well

## Article Pipeline (07:00 CET Daily)
1. **Find keyword** — Playwright → GitHub trending/AlternativeTo (fallback: Brave Search)
2. **Validate keyword** — Check SERP competition
3. **Research** — Extract 3-5 authoritative sources
4. **Write** — 1200-1800 words, Hugo frontmatter, SEO optimized
5. **Quality gate** — If not A-grade, ABORT and notify Michael
6. **Build** — Hugo minify
7. **Git** — add, commit, push (Cloudflare Pages auto-deploys)
8. **Update** — keywords.json, published.json, PIPELINE.md
9. **Log** — daily-logs/YYYY-MM-DD.md
10. **Notify** — Telegram with title + live URL

## Quality Standards (NON-NEGOTIABLE)
- Keyword must have search volume + low competition
- Article must be comprehensive, accurate, valuable
- No filler, no fluff, no AI-sounding garbage
- If uncertain: ABORT, log reason, try tomorrow

## Post-Publication
- Update LESSONS.md with new insights
- Monitor performance (check next day)
- Propose improvements to SOUL.md weekly

## Error Handling
- Log to .learnings/ERRORS.md
- Notify Michael immediately on Telegram
- NEVER publish substandard content
- If 3 errors of same type → create prevention rule
