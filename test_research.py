import asyncio
from research import Researcher

r = Researcher()
results = asyncio.run(r.search_github_trending())
print('Found:', len(results))
for item in results[:3]:
    title = item['title'].encode('ascii', 'ignore').decode()
    snippet = item['snippet'][:60].encode('ascii', 'ignore').decode() if item['snippet'] else ''
    print(f"- {title}: {snippet}...")
