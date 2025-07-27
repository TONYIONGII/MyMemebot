import praw
import aiohttp
import asyncio
import re
from typing import List, Dict, Any
from collections import Counter
from ratelimit import limits, sleep_and_retry
from functools import partial
from meme_tracker.config.settings import RedditConfig, TwitterConfig
import logging

logger = logging.getLogger(__name__)

class SocialMediaScraper:
    def __init__(self):
        # 使用同步praw客户端作为最终解决方案
        from meme_tracker.reddit_api import RedditAPI
        self.reddit = RedditAPI()
        logger.info("Reddit API客户端初始化成功")
        
        # Twitter客户端保持测试模式
        self.twitter_client = None
        logger.warning("Twitter客户端处于测试模式 - 跳过初始化")

    @sleep_and_retry
    @limits(calls=RedditConfig.CALLS_PER_MINUTE, period=60)
    async def get_reddit_posts(self, subreddit: str = "cryptocurrency", limit: int = 100) -> List[str]:
        """获取Reddit热门帖子（使用同步客户端+异步包装）"""
        try:
            posts = await self.reddit.get_hot_posts(subreddit, limit)
            # 严格处理Unicode字符
            processed = []
            for post in posts:
                try:
                    clean_text = post.encode('utf-8', errors='replace').decode('utf-8')
                    if any(ord(c) > 127 for c in clean_text):
                        logger.debug(f"处理包含Unicode字符的帖子: {clean_text[:50]}...")
                    processed.append(clean_text)
                except Exception as e:
                    logger.warning(f"帖子编码处理失败: {e}")
            return processed
        except Exception as e:
            logger.error(f"获取Reddit帖子失败: {e}")
            return []

    @sleep_and_retry
    @limits(calls=TwitterConfig.CALLS_PER_MINUTE, period=60)
    async def get_twitter_posts(self, query: str = "memecoin", count: int = 100) -> List[str]:
        """获取Twitter最近推文（测试模式返回空列表）"""
        logger.warning("Twitter功能处于测试模式 - 返回空列表")
        return []

    @staticmethod
    def extract_coins(texts: List[str], min_length: int = 3, max_length: int = 10) -> Counter:
        """从文本中提取加密货币符号（增强Unicode处理）"""
        pattern = re.compile(r'\$?[A-Z]{%d,%d}\b' % (min_length, max_length))
        counter = Counter()
        for text in texts:
            try:
                # 过滤控制字符和非打印字符
                clean_text = ''.join(c for c in text if c.isprintable())
                matches = pattern.findall(clean_text)
                counter.update(matches)
            except Exception as e:
                logger.warning(f"币种提取失败: {e}")
        return counter

    async def get_trending_coins(self, min_mentions: int = 7) -> Dict[str, int]:
        """获取趋势加密货币（合并Reddit和Twitter结果）"""
        reddit_posts = await self.get_reddit_posts()
        twitter_posts = await self.get_twitter_posts()
        
        all_coins = self.extract_coins(reddit_posts) + self.extract_coins(twitter_posts)
        return {coin: count for coin, count in all_coins.items() if count >= min_mentions}

    async def close(self):
        """清理资源"""
        if hasattr(self, 'reddit'):
            if hasattr(self.reddit, 'session'):
                await self.reddit.session.close()
            logger.info("Reddit客户端资源清理完成")