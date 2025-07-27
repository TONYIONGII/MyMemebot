import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# 修复导入路径
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                coin_name TEXT NOT NULL,
                chain TEXT NOT NULL DEFAULT 'ethereum',
                mention_count INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(platform, coin_name, chain, timestamp)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_name TEXT NOT NULL,
                chain TEXT NOT NULL,
                contract_address TEXT NOT NULL,
                liquidity TEXT,
                market_cap TEXT,
                timestamp TEXT NOT NULL,
                UNIQUE(coin_name, chain, timestamp)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chain_metadata (
                chain TEXT PRIMARY KEY,
                rpc_url TEXT NOT NULL,
                last_sync_block INTEGER DEFAULT 0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT NOT NULL,
                status TEXT NOT NULL,
                last_heartbeat TEXT NOT NULL,
                message TEXT
            )
        """)
        self.conn.commit()

    def insert_mention(self, data: Dict[str, Any]):
        """插入提及记录，支持多链"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR IGNORE INTO mentions 
            (platform, coin_name, chain, mention_count, timestamp) 
            VALUES (?, ?, ?, ?, ?)""",
            (
                data["platform"], 
                data["coin_name"],
                data.get("chain", "ethereum"),
                data["mention_count"], 
                data["timestamp"]
            )
        )
        self.conn.commit()

    def insert_analysis(self, data: dict):
        """插入分析数据"""
        self.cursor.execute(
            "INSERT INTO analysis (coin_name, chain, contract_address, market_cap, liquidity, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (data["coin_name"], data["chain"], data["contract_address"], data["market_cap"], data["liquidity"], data["timestamp"])
        )
        self.conn.commit()

    def get_mentions(self, symbol: str = None) -> list:
        """获取币种提及记录"""
        if symbol:
            self.cursor.execute(
                "SELECT * FROM mentions WHERE coin_name = ? ORDER BY timestamp DESC",
                (symbol,)
            )
        else:
            self.cursor.execute(
                "SELECT * FROM mentions ORDER BY timestamp DESC"
            )
        return self.cursor.fetchall()

    def record_heartbeat(self, component: str, status: str = "OK", message: str = None):
        """记录系统心跳"""
        from datetime import datetime
        self.cursor.execute(
            """INSERT OR REPLACE INTO system_status 
            (component, status, last_heartbeat, message) 
            VALUES (?, ?, ?, ?)""",
            (component, status, datetime.now().isoformat(), message)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()