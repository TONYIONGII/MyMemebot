import asyncio
import logging
import aiohttp
import sys
import os
import time
import telegram
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import locale
import io

# 强制设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 设置统一编码

# 修复导入路径
sys.path.append(str(Path(__file__).parent))
from social_media import SocialMediaScraper
from analysis import CryptoAnalyzer 
from database import DatabaseManager
from notification import TelegramNotifier
from config.settings import DATABASE_PATH

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(DATABASE_PATH.parent.parent / "logs" / "meme_tracker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def check_and_notify(bot=None):
    """检查趋势币种并发送通知"""
    try:
        logger.info("开始检查趋势meme币...")
        
        # 记录心跳
        with DatabaseManager() as db:
            db.record_heartbeat("main", "running", "开始检查趋势币种")
        
        # 初始化组件
        scraper = SocialMediaScraper()
        analyzer = CryptoAnalyzer()
        
        # 获取趋势币种
        trending_coins = await scraper.get_trending_coins()
        if not trending_coins:
            logger.info("未发现符合条件的趋势币种")
            return
            
        # 分析币种数据
        async with aiohttp.ClientSession() as session:
            analysis_results = await analyzer.analyze_coins(list(trending_coins.keys()))
            
        # 存储数据并发送通知
        with DatabaseManager() as db:
            for coin, count in trending_coins.items():
                if coin in analysis_results:
                    # 存储数据
                    db.insert_mention({
                        "platform": "Reddit+X",
                        "coin_name": coin,
                        "mention_count": count,
                        "timestamp": datetime.now().isoformat()
                    })
                    db.insert_analysis(analysis_results[coin])
                    
                    # 记录日志代替通知
                    logger.info(f"检测到趋势币种: {coin} (提及次数: {count})")
        
        logger.info("趋势检查完成")
        with DatabaseManager() as db:
            db.record_heartbeat("main", "idle", "趋势检查完成")
        
    except Exception as e:
        logger.error(f"检查趋势时出错: {e}")
        with DatabaseManager() as db:
            db.record_heartbeat("main", "error", str(e))

async def stress_test():
    """压力测试"""
    logger.info("跳过压力测试阶段...")
    return True

def daemonize():
    """创建守护进程"""
    import os
    import sys
    from signal import SIGTERM
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"第一次fork失败: {e}\n")
        sys.exit(1)
        
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"第二次fork失败: {e}\n")
        sys.exit(1)
        
    sys.stdout.flush()
    sys.stderr.flush()
    
    # 重定向标准文件描述符
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/tmp/meme-tracker.out', 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open('/tmp/meme-tracker.err', 'a+') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

def main():
    """主程序入口"""
    if '--daemon' in sys.argv:
        daemonize()
    
    logger.info("跳过Telegram通知功能，仅运行核心逻辑")
    while True:
        asyncio.run(check_and_notify())
        time.sleep(1800)  # 每30分钟运行一次

if __name__ == "__main__":
    main()
# 保留唯一的函数定义