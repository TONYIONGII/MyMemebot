import aiohttp
import json
from typing import List
from meme_tracker.config.settings import RedditConfig
import logging

logger = logging.getLogger(__name__)

class RedditAPI:
    def __init__(self):
        self.auth_url = "https://www.reddit.com/api/v1/access_token"
        self.base_url = "https://oauth.reddit.com"
        self.access_token = None

    async def authenticate(self):
        """使用OAuth2获取访问令牌"""
        # 手动构建认证头
        from base64 import b64encode
        creds = f"{RedditConfig.CLIENT_ID}:{RedditConfig.CLIENT_SECRET}".encode('utf-8')
        auth_header = f"Basic {b64encode(creds).decode('utf-8')}"
        
        data = {
            "grant_type": "password",
            "username": RedditConfig.USERNAME,
            "password": RedditConfig.PASSWORD,
            "scope": "read"
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": auth_header,
                "User-Agent": RedditConfig.USER_AGENT
            }
            async with session.post(
                self.auth_url,
                headers=headers,
                data=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.access_token = result["access_token"]
                    logger.info("Reddit认证成功")
                else:
                    error = await response.text()
                    logger.error(f"Reddit认证失败: {response.status} - {error}")
                    raise Exception(f"认证失败: {error}")

    async def get_hot_posts(self, subreddit: str = "cryptocurrency", limit: int = 100) -> List[str]:
        """直接通过API获取热门帖子"""
        if not self.access_token:
            await self.authenticate()

        url = f"{self.base_url}/r/{subreddit}/hot"
        params = {"limit": limit}
        headers = {
            "Authorization": f"bearer {self.access_token}",
            "User-Agent": RedditConfig.USER_AGENT,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=utf-8"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = []
                    for post in data["data"]["children"]:
                        try:
                            title = post["data"]["title"]
                            selftext = post["data"]["selftext"]
                            content = f"{title} {selftext}".encode('utf-8', errors='replace').decode('utf-8')
                            posts.append(content)
                        except Exception as e:
                            logger.warning(f"帖子处理错误: {e}")
                    return posts
                else:
                    error = await response.text()
                    logger.error(f"获取帖子失败: {response.status} - {error}")
                  