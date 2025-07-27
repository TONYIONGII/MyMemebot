import os
import re
from pathlib import Path

def detect_secrets():
    """检测项目中的敏感信息"""
    risks = []
    
    # 检查加密文件完整性
    env_enc = Path("meme_tracker/config/.env.enc")
    env_file = Path("meme_tracker/config/.env")
    if not env_enc.exists():
        if env_file.exists() and "default" in env_file.read_text():
            risks.append("⚠️ 使用默认配置 - 请创建正式的.env.enc文件")
        else:
            risks.append("❌ 缺失加密的.env.enc文件且无默认配置")
    elif env_enc.stat().st_size < 10:
        risks.append("❌ 加密文件可能损坏")

    # 检查密钥硬编码
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(('.py', '.md', '.txt')):
                path = Path(root) / file
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    if re.search(r'[A-Za-z0-9+/]{43}=', f.read()):
                        risks.append(f"⚠️ 疑似密钥硬编码在: {path}")

    return risks or ["✅ 未检测到明显安全问题"]

if __name__ == "__main__":
    print("\n".join(detect_secrets()))