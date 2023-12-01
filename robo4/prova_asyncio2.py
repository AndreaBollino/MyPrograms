import asyncio
import aiohttp

async def download_page(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['http://example.com/page1', 'http://example.com/page2', 'http://example.com/page3']
    tasks = [download_page(url) for url in urls]
    
    pages = await asyncio.gather(*tasks)
    
    for url, page in zip(urls, pages):
        print(f'{url} is {len(page)} bytes long')

# Python 3.7+
asyncio.run(main())