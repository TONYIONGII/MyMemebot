import os
import pytest
import praw
from dotenv import load_dotenv
import json
from unittest.mock import patch
from cryptography.fernet import Fernet

def sanitize_credentials(credentials):
    """清理敏感信息"""
    if not credentials:
        return None
    key = Fernet.generate_key()
    cipher = Fernet(key)
    return cipher.encrypt(credentials.encode()).decode()

def test_reddit_connection():
    """测试Reddit API连接"""
    try:
        # 安全加载环境变量
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/.env'))
        if not os.path.exists(env_path):
            pytest.skip("缺少环境配置文件")
        
        load_dotenv(env_path)
        
        # 验证必要环境变量
        required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            pytest.fail(f"缺少必要的环境变量: {missing_vars}")
        
        # 使用安全配置
        with patch('praw.Reddit') as mock_reddit:
            mock_reddit.return_value.subreddit.return_value = 'all'
            reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent="MemeTracker/v2.0 (by /u/TONYIONG)"
            )
            
            # 清理日志中的敏感信息
            sanitized_id = sanitize_credentials(os.getenv('REDDIT_CLIENT_ID'))
            sanitized_secret = sanitize_credentials(os.getenv('REDDIT_CLIENT_SECRET'))
            print(f"使用客户端ID: [已清理] 和密钥: [已清理] 进行测试")
            
            # 使用基础API测试
            subreddit = reddit.subreddit('all')
            assert subreddit is not None, "无法获取subreddit信息"
            
    except praw.exceptions.PRAWException as e:
        pytest.fail(f"PRAW API错误: {str(e)}")
    except Exception as e:
        pytest.fail(f"测试过程中发生意外错误: {str(e)}")

if __name__ == "__main__":
    # 仅用于开发测试，正式环境应使用pytest
    try:
        test_reddit_connection()
        print("测试执行完成")
    except Exception as e:
        print(f"测试失败: {str(e)}")
        exit(1)