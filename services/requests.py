import aiohttp
import asyncio


async def post_data():
    url = "https://6a3c-92-63-205-187.ngrok-free.app/led/on"
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = response
            print(data)

if __name__ == "__main__":
    asyncio.run(post_data())