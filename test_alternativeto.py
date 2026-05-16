import asyncio
from research import Researcher

r = Researcher()
results = asyncio.run(r.search_alternative_to("Dropbox"))
print('Found:', len(results))
for item in results[:5]:
    title = item['title'].encode('ascii', 'ignore').decode()
    print(f"- {title}")
