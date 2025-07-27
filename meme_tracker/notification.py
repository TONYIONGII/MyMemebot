import logging
import mimetypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    Application, 
    ContextTypes, 
    CommandHandler,
    CallbackContext
)

logger = logging.getLogger(__name__)

# 替代imghdr的功能
def guess_image_type(file_path):
    return mimetypes.guess_type(file_path)[0] or 'unknown'
import sys
from pathlib import Path
from typing import Dict, Any

# 修复导入路径
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import TelegramConfig

class TelegramNotifier:
    def __init__(self):
        import os
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN环境变量未配置")
        self.app = None
        
    async def initialize(self):
        """异步初始化"""
        from telegram import Bot
        try:
            # 先验证Token有效性
            test_bot = Bot(token=self.token)
            await test_bot.initialize()
            
            # 初始化主应用
            self.app = Application.builder().token(self.token).build()
            self._setup_handlers()
            await self.app.initialize()
            
            logger.info("Telegram Bot初始化成功")
        except Exception as e:
            logger.critical(f"Telegram Bot初始化失败: {e}")
            raise

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("track", self.track))
        self.app.add_handler(CommandHandler("status", self.status))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理/start命令"""
        await update.message.reply_text(
            "🚀 Meme Coin Tracker Bot 已启动！\n"
            "使用 /track 开始追踪热门meme币\n"
            "每30分钟会自动检查并通知提及次数≥7的币种"
        )

    async def track(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理/track命令"""
        chat_id = update.effective_chat.id
        context.job_queue.run_repeating(
            self._send_alerts,
            interval=1800,  # 每30分钟
            first=0,
            chat_id=chat_id,
            name=str(chat_id)
        )
        await update.message.reply_text("✅ 追踪已启动！您将收到热门meme币的通知")

    async def _send_alerts(self, context: CallbackContext):
        """发送警报通知"""
        from .main import check_and_notify  # 避免循环导入
        await check_and_notify(context.bot)
        
        # 每次检查后发送心跳
        await self._send_heartbeat(context)

    async def _send_heartbeat(self, context: CallbackContext):
        """发送心跳检测"""
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text=f"💓 系统运行正常 | 最后检查时间: {now}"
        )

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理/status命令"""
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(
            f"🤖 Meme Tracker 状态报告\n"
            f"运行状态: 正常\n"
            f"最后心跳: {now}\n"
            f"使用 /track 开始追踪"
        )

    async def send_coin_alert(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, coin_data: Dict[str, Any], analysis_data: Dict[str, Any]):
        """发送单个币种通知"""
        keyboard = [[
            InlineKeyboardButton(
                f"{coin_data['coin_name']} on CoinGecko",
                url=f"https://www.coingecko.com/en/coins/{coin_data['coin_name'].lower()}"
            )
        ]]
        
        message = (
            f"🔥 热门Meme币警报: {coin_data['coin_name']}\n"
            f"平台: {coin_data['platform']}\n"
            f"提及次数: {coin_data['mention_count']}\n"
            f"链: {analysis_data['chain']}\n"
            f"市值: ${analysis_data['market_cap']}\n"
            f"流动性: ${analysis_data['liquidity']}\n"
            f"合约地址: {analysis_data['contract_address']}\n"
            f"时间: {analysis_data['timestamp']}"
        )
        
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            logger.error(f"发送Telegram通知失败: {e}")
            raise

    async def run(self):
        """启动Telegram机器人"""
        try:
            await self.app.run_polling()
        except Exception as e:
            logger.critical(f"Telegram机器人运行失败: {e}")
            raise