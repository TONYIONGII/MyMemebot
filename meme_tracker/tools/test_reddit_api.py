import os
import praw
from dotenv import load_dotenv
import json

def test_reddit_connection():
    """测试Reddit API连接"""
    try:
        load_dotenv('../config/.env')
        
        # 使用最简配置
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="MemeTracker/v2.0 (by /u/TONYIONG)"
        )
        
        # 使用基础API测试
        subreddit = reddit.subreddit('all')
        return "✅ 连接成功 - API响应正常"
        
    except Exception as e:
        return f"❌ 连接失败: {str(e)}"

if __name__ == "__main__":
    result = test_reddit_connection()
    print(json.dumps(result, ensure_ascii=False))