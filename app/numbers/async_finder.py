import asyncio
import logging
import re
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def use_regex(text):
    regex = (r">(?:\+)?(?: )?([7,8])?(?: )?(?:\(?([0-9]{3,4})\)?)?"
             r"(?: )?([0-9]{2,3}[?: \-]?[0-9]{2,3}[?: \-]?[0-9]{2,3})<")
    res = re.findall(regex, text)
    if not res:
        logger.warning("Finder error")
    else:
        country, city, number = res[0]

        city = city or "495"
        number = number.replace("-", "").replace(" ", "")

        number = f"8{city}{number}"
        logger.info(f"Found number {number}")  # or save number


async def get_phone(link, session, executor):
    try:
        response = await session.get(link)
        text = await response.text()
    except Exception as e:
        logger.warning(e)
    else:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, use_regex(text))


async def worker(name, queue, executor):
    async with aiohttp.ClientSession() as session:
        while True:
            url = await queue.get()

            try:
                await get_phone(url, session, executor)
            except Exception as e:
                print(e)

            queue.task_done()


async def producer(queue):
    for line in open("file.txt"):
        url = line.strip("\n")
        await queue.put(url)


async def main():
    queue = asyncio.Queue(maxsize=50)
    executor = ProcessPoolExecutor(max_workers=4)
    tasks = []
    for i in range(10):
        worker_task = asyncio.create_task(worker(f"worker {i}", queue, executor))
        tasks.append(worker_task)

    await producer(queue)

    await queue.join()

    for t in tasks:
        t.cancel()


start = datetime.now()
asyncio.run(main())
print(datetime.now() - start)
