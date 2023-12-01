# import asyncio
# import aiohttp

# async def main():
#     async with aiohttp.ClientSession(trust_env=True) as session:
#         async with session.get('https://www.google.com') as response:
#             html = await response.text()
#         print(html)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# import requests

# url = 'https://www.google.com'

# try:
#     response = requests.get(url)
#     response.raise_for_status()  # Solleva un'eccezione se la richiesta ha avuto successo ma il codice di stato HTTP non è 200
#     html = response.text

#     with open('google.html', 'w', encoding='utf-8') as file:
#         file.write(html)
        
#     print("HTML della pagina è stato scritto su 'google.html'")

# except requests.exceptions.RequestException as e:
#     print(f"Si è verificato un errore durante la richiesta: {e}")


import asyncio
import aiohttp

urls = [
    'https://www.twitter.com',
    'https://www.google.com'
]


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())