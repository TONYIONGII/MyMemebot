import aiohttp
import asyncio
import os
import sys
from base64 import b64encode
from datetime import datetime

def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ERROR][{timestamp}] {message}", file=sys.stderr)

def log_info(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[INFO][{timestamp}] {message}")

async def test_auth():
    try:
        CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
        CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
        
        if not CLIENT_ID or not CLIENT_SECRET:
            raise ValueError("Reddit API凭证未配置")
            
        auth_url = "https://www.reddit.com/api/v1/access_token"
        auth_header = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        
        log_info("开始Reddit API认证测试")
        log_info(f"使用Client ID: {CLIENT_ID[:3]}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                auth_url,
                headers={
                    "Authorization": f"Basic {auth_header}",
                    "User-Agent": "MemeTrackerTester/1.0"
                },
                data={"grant_type": "client_credentials"}
            ) as response:
                status = response.status
                response_text = await response.text()
                
                log_info(f"认证响应状态码: {status}")
                log_info(f"认证响应内容: {response_text[:100]}...")
                
                if status != 200:
                    raise Exception(f"API认证失败: {response_text}")
                
                return True
                
    except Exception as e:
        log_error(f"测试过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Reddit API测试 ===")
    try:
        success = asyncio.run(test_auth())
        if not success:
            sys.exit(1)
    except Exception as e:
        log_error(f"测试执行失败: {str(e)}")
        sys.exit(1)