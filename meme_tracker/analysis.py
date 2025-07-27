import asyncio
import aiohttp
import sys
from pathlib import Path
from typing import Dict, Optional, List
from ratelimit import limits, sleep_and_retry
from web3 import Web3

# 修复导入路径
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import CoinGeckoConfig, ChainConfig

class CryptoAnalyzer:
    def __init__(self):
        eth_url = ChainConfig.get_provider('ethereum')
        self.web3 = Web3(Web3.HTTPProvider(eth_url)) if eth_url else None

    @sleep_and_retry
    @limits(calls=CoinGeckoConfig.CALLS_PER_MINUTE, period=60)
    async def fetch_coingecko_data(self, session: aiohttp.ClientSession, endpoint: str) -> Optional[dict]:
        """从CoinGecko获取数据"""
        try:
            async with session.get(f"{CoinGeckoConfig.API_URL}{endpoint}") as response:
                if response.status == 429:
                    await asyncio.sleep(60)
                    return await self.fetch_coingecko_data(session, endpoint)
                return await response.json()
        except Exception as e:
            print(f"Error fetching CoinGecko data: {e}")
            return None

    async def analyze_coin(self, session: aiohttp.ClientSession, coin_name: str) -> Optional[Dict[str, str]]:
        """分析单个加密货币"""
        # 获取基础信息
        data = await self.fetch_coingecko_data(session, f"/coins/{coin_name.lower()}")
        if not data:
            return None

        result = {
            "coin_name": coin_name,
            "chain": data.get("asset_platform_id", "Unknown"),
            "contract_address": data.get("contract_address", "N/A"),
            "market_cap": str(data.get("market_data", {}).get("market_cap", {}).get("usd", "N/A")),
            "liquidity": str(data.get("market_data", {}).get("total_volume", {}).get("usd", "N/A")),
            "timestamp": datetime.now().isoformat()
        }

        # 验证以太坊合约
        if result["chain"].lower() == "ethereum" and self.web3 and self.web3.is_connected():
            try:
                contract = self.web3.eth.contract(address=result["contract_address"])
                result["liquidity"] = f"{result['liquidity']} (Verified)"
            except:
                result["liquidity"] = f"{result['liquidity']} (Unverified)"

        return result

    async def analyze_coins(self, coin_names: List[str]) -> Dict[str, Dict[str, str]]:
        """批量分析加密货币"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.analyze_coin(session, coin) for coin in coin_names]
            results = await asyncio.gather(*tasks)
            return {res["coin_name"]: res for res in results if res}