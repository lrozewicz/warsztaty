import asyncio

async def przyklad():
    print("Zaczynam")
    await asyncio.sleep(1)
    print("Koniec")

asyncio.run(przyklad())
