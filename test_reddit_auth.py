import aiohttp
import asyncio
import os
from base64 import b64encode

async def test_reddit_auth():
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    USERNAME = os.getenv("REDDIT_USERNAME")
    PASSWORD = os.getenv("REDDIT_PASSWORD")
    
    auth_url = "https://www.reddit.com/api/v1/access_token"
    auth_header = f"Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
    
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD,
        "scope": "read"
    }
    
    headers = {
        "Authorization": auth_header,
        "User-Agent": "MemeTrackerTester/1.0"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(auth_url, headers=headers, data=data) as response:
            print(f"状态码: {response.status}")
            print(f"响应: {await response.text()}")

if __name__ == "__main__":
    print("=== Reddit认证测试 ===")
    print(f"Client ID: {os.getenv('REDDIT_CLIENT_ID')}")
    print(f"Username: {os.getenv('REDDIT_USERNAME')}")
    
    if not all([os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET'), 
                os.getenv('REDDIT_USERNAME'), os.getenv('REDDIT_PASSWORD')]):
        print("错误: 缺少必要的环境变量")
    else:
        asyncio.run(test_reddit_auth())