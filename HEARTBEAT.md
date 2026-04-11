# HEARTBEAT — ToolScout Autonomous Pipeline

## Timezone
Europe/Rome (CET)

## Every Heartbeat (30 min)
- Read LESSONS.md last 10 entries
- Read .learnings/ERRORS.md for recent errors
- Check drafts/ for articles needing review
- Check PIPELINE.md for status
- If nothing needs attention: HEARTBEAT_OK

## Every 2 Hours (08:00-23:00)
- Use Brave Search: find 1 new long-tail keyword
- Follow templates/keyword-research.md
- Add to data/keywords.json with status "pending"

## Daily (08:00)
- Pick highest-priority pending keyword from keywords.json
- Write full article (1200-1800 words) following templates/article-brief.md
- Self-review with templates/article-review.md
- If score >= 12/16: save to site/content/posts/[slug].md with Hugo frontmatter, git add+commit+push
- If score < 12/16: rewrite weak sections, re-review
- Log everything to daily-logs/YYYY-MM-DD.md
- Update PIPELINE.md

## Weekly (Monday 09:00)
- Review all articles from the week
- Update LESSONS.md with patterns
- Propose improvements to templates or SOUL.md

## Self-Improvement Rules
- Before writing ANY article: re-read last 10 LESSONS.md entries
- After EVERY article: log what went well/badly to LESSONS.md
- If same error appears 3x in ERRORS.md: create prevention rule
- Never repeat a logged mistake
