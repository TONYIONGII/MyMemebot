import os
from pathlib import Path
from dotenv import load_dotenv

# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载环境变量
load_dotenv(BASE_DIR / 'config' / '.env')

# API配置
class RedditConfig:
    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "").strip()
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
    USERNAME = os.getenv("REDDIT_USERNAME", "").strip()
    PASSWORD = os.getenv("REDDIT_PASSWORD", "").strip()
    USER_AGENT = os.getenv("REDDIT_USER_AGENT", "MemeTracker/v1.0 (by /u/YourUsername)").strip()
    CALLS_PER_MINUTE = 60
    REQUIRED_FIELDS = ["CLIENT_ID", "CLIENT_SECRET", "USERNAME", "PASSWORD"]
    
    @classmethod
    def validate(cls):
        for field in cls.REQUIRED_FIELDS:
            if not getattr(cls, field):
                raise ValueError(f"Reddit配置缺失: {field}")
class TwitterConfig:
    API_KEY = os.getenv("TWITTER_API_KEY", "")
    API_SECRET = os.getenv("TWITTER_API_SECRET", "")
    BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    CALLS_PER_MINUTE = 300

class CoinGeckoConfig:
    API_URL = "https://api.coingecko.com/api/v3"
    CALLS_PER_MINUTE = 30

class TelegramConfig:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class ChainConfig:
    @staticmethod
    def get_provider(chain: str):
        """获取指定链的RPC提供商"""
        rpc_map = {
            'ethereum': os.getenv("ETHEREUM_RPC"),
            'polygon': os.getenv("POLYGON_RPC"), 
            'bsc': os.getenv("BSC_RPC"),
            'solana': os.getenv("SOLANA_RPC"),
            'avalanche': os.getenv("AVALANCHE_RPC"),
            'arbitrum': os.getenv("ARBITRUM_RPC")
        }
        chain_key = str(chain).lower().strip()
        if not (url := rpc_map.get(chain_key)):
            raise ValueError(f"Unsupported chain: {chain} (available: {list(rpc_map.keys())})")
        return url  # 返回原始URL，由调用方决定如何构造provider

    @staticmethod
    def supported_chains():
        """获取支持的所有链"""
        return ['ethereum', 'polygon', 'bsc', 'solana', 'avalanche', 'arbitrum']

# 数据库配置
DATABASE_PATH = BASE_DIR / 'data' / 'meme_coins.db'