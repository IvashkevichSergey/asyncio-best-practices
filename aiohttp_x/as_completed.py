import asyncio
import aiohttp
from utils import async_timed


async def fetch_fact(session: aiohttp.ClientSession, url: str, delay: int):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return await result.text()


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        lst = [fetch_fact(session, f'http://numbersapi.com/{num}/trivia', num) for num in range(5)]
        for results in asyncio.as_completed(lst):
            print(await results)


asyncio.get_event_loop().run_until_complete(main())
