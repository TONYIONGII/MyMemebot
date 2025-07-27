import aiohttp
import asyncio
import os
from base64 import b64encode

# 从环境变量获取凭证
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

async def test_auth():
    auth_url = "https://www.reddit.com/api/v1/access_token"
    auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            auth_url,
            headers={
                "Authorization": f"Basic {auth_header}",
                "User-Agent": "MemeTrackerTester/1.0"
            },
            data={"grant_type": "client_credentials"}
        ) as response:
            print(f"状态码: {response.status}")
            print(f"响应: {await response.text()}")

if __name__ == "__main__":
    print("=== Reddit API测试 ===")
    print(f"Client ID: {CLIENT_ID}")
    print(f"Client Secret: {CLIENT_SECRET[:3]}...")
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("错误: 缺少API凭证")
    else:
        asyncio.run(test_auth())