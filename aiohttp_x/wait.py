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
        lst = [asyncio.create_task(fetch_fact(session, f'http://numbersapi.com/{num}/trivia', num)) for num in range(5)]
        # done, pending = await asyncio.wait(lst, return_when='FIRST_EXCEPTION')
        done, lst = await asyncio.wait(lst, timeout=2)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(lst)}')

        for done_task in done:
            if done_task.exception() is None:
                print(await done_task)
            else:
                print("THERE WAS An EXCEPTION -", done_task.exception())

        for pending_task in lst:
            print(pending_task.get_name(), "is still in progress")
            # pending_task.cancel()
            # result = await pending_task
            # print(result)


asyncio.get_event_loop().run_until_complete(main())
