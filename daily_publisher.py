#!/usr/bin/env python3
"""
ToolScout Daily Publisher - Runs at 07:00 CET
Triggered by OpenClaw heartbeat system
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("C:/Users/Cassiopea/.openclaw/workspace-toolscout")
DAILY_LOGS = WORKSPACE / "daily-logs"
LEARNINGS = WORKSPACE / ".learnings"

# Ensure directories exist
DAILY_LOGS.mkdir(exist_ok=True)
LEARNINGS.mkdir(exist_ok=True)

def log_status(message: str, level: str = "INFO"):
    """Log to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DAILY_LOGS / f"{today}.md"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"- {message}\n")

def check_prerequisites():
    """Check if all prerequisites are met before publishing"""
    log_status("🔍 Checking prerequisites...")
    
    # Check LESSONS.md exists
    lessons_file = WORKSPACE / "LESSONS.md"
    if not lessons_file.exists():
        log_status("⚠️ LESSONS.md not found, creating...", "WARN")
        lessons_file.write_text("# Lessons Learned\n\n")
    
    # Check keywords.json exists
    keywords_file = WORKSPACE / "keywords.json"
    if not keywords_file.exists():
        log_status("⚠️ keywords.json not found, creating...", "WARN")
        keywords_file.write_text("[]")
    
    log_status("✅ Prerequisites checked")
    return True

def main():
    """Main entry point - this script is called by OpenClaw heartbeat"""
    log_status("🚀 ToolScout Daily Publisher started")
    log_status(f"📅 Running at {datetime.now().strftime('%Y-%m-%d %H:%M')} CET")
    
    if not check_prerequisites():
        log_status("❌ Prerequisites failed, aborting", "ERROR")
        return 1
    
    log_status("⏳ Ready for agent to execute pipeline...")
    log_status("📋 Agent should: read LESSONS.md → find keyword → write → build → deploy")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
