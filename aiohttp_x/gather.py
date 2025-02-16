import asyncio
import aiohttp
from utils import async_timed


async def fetch_fact(session: aiohttp.ClientSession, url: str, delay: int = 0):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return await result.text()


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        lst = [fetch_fact(session, f'http://numbersapi.com/{num}/trivia', 3-num) for num in range(2)]
        result = await asyncio.gather(*lst, return_exceptions=True)
        for res in result:
            print(res)


asyncio.get_event_loop().run_until_complete(main())
