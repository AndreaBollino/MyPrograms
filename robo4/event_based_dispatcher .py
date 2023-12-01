import asyncio

async def producer(queue):
    for i in range(10):
        await asyncio.sleep(1)
        await queue.put(i)
    await queue.put(None)
    queue.task_done()

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed: {item}")
        queue.task_done()
        

async def main():
    queue = asyncio.Queue()
    tasks = [
        asyncio.create_task(producer(queue)),
        asyncio.create_task(consumer(queue)),
    ]
    await asyncio.gather(*tasks)
    await queue.join()

asyncio.run(main())