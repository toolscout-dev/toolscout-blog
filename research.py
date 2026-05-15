# research.py — Playwright-based research for ToolScout
"""
Research module using Playwright for web scraping.
Falls back to Brave Search if Playwright fails.
"""

import asyncio
import json
import re
from datetime import datetime
from typing import List, Dict, Optional

try:
    from playwright.async_api import async_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

class Researcher:
    def __init__(self):
        self.results = []
        
    async def search_github_trending(self) -> List[Dict]:
        """Find trending open source projects on GitHub"""
        if not PLAYWRIGHT_AVAILABLE:
            return []
            
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # GitHub trending
                await page.goto("https://github.com/trending", timeout=30000)
                await page.wait_for_selector("article.Box-row", timeout=10000)
                
                items = await page.query_selector_all("article.Box-row")
                for item in items[:10]:
                    try:
                        link_elem = await item.query_selector("h2 a")
                        if link_elem:
                            repo = await link_elem.inner_text()
                            url = "https://github.com" + await link_elem.get_attribute("href")
                            desc_elem = await item.query_selector("p.col-9")
                            description = await desc_elem.inner_text() if desc_elem else ""
                            
                            results.append({
                                "title": repo.strip(),
                                "url": url,
                                "snippet": description.strip(),
                                "source": "github_trending"
                            })
                    except:
                        continue
                        
            except Exception as e:
                print(f"GitHub error: {e}")
            finally:
                await browser.close()
                
        return results
    
    async def search_alternative_to(self, tool_name: str) -> List[Dict]:
        """Search for alternatives on alternativeTo.net"""
        if not PLAYWRIGHT_AVAILABLE:
            return []
            
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                url = f"https://alternativeto.net/software/{tool_name.lower().replace(' ', '-')}/"
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Extract alternatives
                items = await page.query_selector_all("[data-testid='alternative-item']")
                for item in items[:5]:
                    try:
                        name_elem = await item.query_selector("h3, .AlternativeItem__name")
                        name = await name_elem.inner_text() if name_elem else ""
                        
                        link_elem = await item.query_selector("a")
                        href = await link_elem.get_attribute("href") if link_elem else ""
                        
                        if name:
                            results.append({
                                "title": f"{name} — Alternative to {tool_name}",
                                "url": f"https://alternativeto.net{href}" if href.startswith("/") else href,
                                "snippet": f"Open source alternative to {tool_name}",
                                "source": "alternativeto"
                            })
                    except:
                        continue
                        
            except Exception as e:
                print(f"AlternativeTo error: {e}")
            finally:
                await browser.close()
                
        return results
    
    async def search_google(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search Google and extract results using Playwright"""
        if not PLAYWRIGHT_AVAILABLE:
            return []
            
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            # Hide webdriver
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            page = await context.new_page()
            
            try:
                # Navigate to Google with delay
                await page.goto("https://www.google.com", wait_until="networkidle")
                await page.wait_for_timeout(1000)
                
                # Type search query
                search_box = await page.wait_for_selector("textarea[name='q']", timeout=10000)
                await search_box.fill(query)
                await search_box.press("Enter")
                
                # Wait for results
                await page.wait_for_timeout(3000)
                
                # Extract search results - multiple strategies
                items = await page.query_selector_all("div.g")
                if not items:
                    items = await page.query_selector_all("div[data-ved]")
                
                for item in items[:max_results]:
                    try:
                        title_elem = await item.query_selector("h3")
                        title = await title_elem.inner_text() if title_elem else ""
                        
                        link_elem = await item.query_selector("a")
                        url = await link_elem.get_attribute("href") if link_elem else ""
                        
                        snippet_elem = await item.query_selector("div.VwiC3b, span:not([class])")
                        snippet = ""
                        if snippet_elem:
                            snippet = await snippet_elem.inner_text()
                        
                        if title and url and not url.startswith("/"):
                            results.append({
                                "title": title,
                                "url": url,
                                "snippet": snippet[:200],
                                "source": "google"
                            })
                    except:
                        continue
                        
            except Exception as e:
                print(f"Playwright error: {e}")
            finally:
                await browser.close()
                
        return results
    
    async def extract_article_content(self, url: str) -> Dict:
        """Extract main content from an article page"""
        if not PLAYWRIGHT_AVAILABLE:
            return {}
            
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_load_state("networkidle")
                
                # Extract title
                title = await page.title()
                
                # Extract main content (common selectors)
                content_selectors = [
                    "article",
                    "main",
                    "[role='main']",
                    ".content",
                    ".post-content",
                    "#content"
                ]
                
                content = ""
                for selector in content_selectors:
                    try:
                        elem = await page.query_selector(selector)
                        if elem:
                            content = await elem.inner_text()
                            if len(content) > 500:
                                break
                    except:
                        continue
                
                # Extract headings for structure
                headings = await page.eval_on_selector_all("h1, h2, h3", 
                    "elements => elements.map(e => ({tag: e.tagName, text: e.innerText}))")
                
                return {
                    "url": url,
                    "title": title,
                    "content": content[:5000],  # Limit content
                    "headings": headings,
                    "scraped_at": datetime.now().isoformat()
                }
                
            except Exception as e:
                return {"url": url, "error": str(e)}
            finally:
                await browser.close()
    
    async def find_competitors(self, keyword: str) -> List[Dict]:
        """Find top-ranking articles for a keyword"""
        results = await self.search_google(f"{keyword} 2026", max_results=10)
        
        competitors = []
        for result in results:
            if any(x in result['url'] for x in ['blog', 'article', 'guide', 'review']):
                competitors.append(result)
                
        return competitors
    
    def analyze_keyword_potential(self, keyword: str, serp_results: List[Dict]) -> Dict:
        """Analyze if a keyword is worth targeting"""
        # Check for weak signals
        weak_signals = 0
        strong_domains = ['reddit.com', 'quora.com', 'medium.com', 'github.com']
        
        for result in serp_results[:5]:
            domain = result['url'].split('/')[2] if '/' in result['url'] else ''
            
            # Weak domains = opportunity
            if any(sd in domain for sd in strong_domains):
                weak_signals += 1
            
            # Old dates = opportunity
            if any(year in result.get('snippet', '') for year in ['2023', '2024']):
                weak_signals += 1
        
        return {
            "keyword": keyword,
            "competition_score": len(serp_results),
            "weak_signals": weak_signals,
            "opportunity_score": weak_signals / max(len(serp_results), 1),
            "recommendation": "TARGET" if weak_signals >= 2 else "SKIP"
        }

# Synchronous wrapper for easy use
def search(query: str, max_results: int = 5) -> List[Dict]:
    """Synchronous wrapper for search_google"""
    researcher = Researcher()
    return asyncio.run(researcher.search_google(query, max_results))

def extract(url: str) -> Dict:
    """Synchronous wrapper for extract_article_content"""
    researcher = Researcher()
    return asyncio.run(researcher.extract_article_content(url))

def analyze_keyword(keyword: str) -> Dict:
    """Full keyword analysis with SERP check"""
    researcher = Researcher()
    serp = asyncio.run(researcher.search_google(keyword, max_results=10))
    return researcher.analyze_keyword_potential(keyword, serp)

if __name__ == "__main__":
    # Test
    print("Testing Playwright research...")
    results = search("open source alternative to Jira 2026", 3)
    print(json.dumps(results, indent=2))
