import asyncio
from meme_tracker.social_media import SocialMediaScraper
from meme_tracker.config.settings import RedditConfig
import logging

async def test_reddit_integration():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 验证配置
    try:
        RedditConfig.validate()
        logging.info("配置验证通过")
    except Exception as e:
        logging.error(f"配置错误: {e}")
        return False

    # 测试Reddit集成
    scraper = SocialMediaScraper()
    try:
        logging.info("测试Reddit认证...")
        await scraper.reddit.authenticate()
        logging.info("✓ 认证成功")
        
        logging.info("测试帖子获取...")
        posts = await scraper.get_reddit_posts(limit=3)
        logging.info(f"✓ 获取到{len(posts)}条帖子")
        
        logging.info("测试Unicode处理...")
        sample = posts[0] if posts else '测试内容 🚀🔥 你好'
        processed = sample.encode('utf-8', errors='replace').decode('utf-8')
        logging.info(f"原始: {sample[:100]}...")
        logging.info(f"处理后: {processed[:100]}...")
        
        return True
    except Exception as e:
        logging.error(f"测试失败: {e}", exc_info=True)
        return False
    finally:
        await scraper.close()

if __name__ == "__main__":
    result = asyncio.run(test_reddit_integration())
    print("\n=== 测试结果 ===")
    print("状态:", "通过 ✅" if result else "失败 ❌")