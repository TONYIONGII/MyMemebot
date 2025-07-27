# Meme Coin Tracker 🚀

一个自动追踪Reddit和Twitter上热门meme加密货币的Python系统，结合公链数据分析并通过Telegram发送通知。

## 功能特性

- 🔍 从Reddit和Twitter抓取提及meme币的帖子
- 📊 筛选提及次数≥7的代币
- ⛓️ 结合CoinGecko和Web3进行公链数据分析
- 🤖 通过Telegram机器人发送实时通知
- ⚡ 异步处理优化性能
- ??️ 完善的API速率限制处理
- 📈 内置压力测试脚本

## 快速开始

### 1. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. 配置环境变量

复制`.env.example`为`.env`并填写您的API密钥：

```bash
cp meme_tracker/config/.env.example meme_tracker/config/.env
```

### 3. 获取API密钥

- [Reddit API](https://www.reddit.com/prefs/apps)
- [Twitter Developer Portal](https://developer.twitter.com/)
- [Telegram BotFather](https://core.telegram.org/bots#6-botfather)
- [Infura](https://infura.io/) (Web3提供商)

### 4. 运行系统

```bash
python -m meme_tracker.main
```

### 5. 使用Telegram机器人

1. 搜索您的机器人并发送 `/start`
2. 发送 `/track` 开始接收通知

## 项目结构

```
meme_tracker/
├── __init__.py
├── main.py              # 主程序入口
├── config/
│   ├── __init__.py
│   ├── settings.py      # 配置设置
│   └── .env             # 环境变量
├── social_media.py      # 社交媒体抓取
├── analysis.py          # 加密货币分析
├── database.py          # 数据库管理
├── notification.py      # Telegram通知
├── data/
│   └── meme_coins.db    # SQLite数据库
└── logs/
    └── meme_tracker.log  # 日志文件
```

## 自定义设置

- 修改`MIN_MENTIONS_THRESHOLD`调整触发通知的提及阈值
- 修改`CHECK_INTERVAL_HOURS`调整检查频率
- 添加更多社交媒体平台或分析指标

## 压力测试

系统内置压力测试脚本，运行时会自动执行100次并发API请求测试。

## 贡献

欢迎提交Issue和Pull Request！
```