import os
import re
from pathlib import Path
import json
from typing import List, Dict

SECRET_PATTERNS = {
    "api_key": re.compile(r'(?i)(api|access|secret)[_-]?key["\']?\\s*[:=]\\s*["\']?([A-Za-z0-9+/=]{20,100})["\']?'),
    "jwt": re.compile(r'eyJ[A-Za-z0-9-_=]+\\.[A-Za-z0-9-_=]+(?:\\.[A-Za-z0-9-_.+/=]+)?'),
    "aws": re.compile(r'(?i)AKIA[0-9A-Z]{16}'),
    "crypto": re.compile(r'[A-Za-z0-9+/]{43}=')
}

def detect_secrets() -> List[str]:
    """检测项目中的敏感信息"""
    risks = []
    
    # 检查加密文件完整性
    env_enc = Path("meme_tracker/config/.env.enc")
    if not env_enc.exists():
        risks.append("❌ 缺失加密的.env.enc文件")
    elif env_enc.stat().st_size < 10:
        risks.append("❌ 加密文件可能损坏")

    # 检查密钥硬编码
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(('.py', '.js', '.md', '.txt', '.json')):
                path = Path(root) / file
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for secret_type, pattern in SECRET_PATTERNS.items():
                        if pattern.search(content):
                            risks.append(
                                f"🚨 检测到疑似{secret_type.upper()}密钥在: {path}\n"
                                f"    匹配内容: {pattern.search(content).group()[:20]}..."
                            )

    return risks or ["✅ 未检测到明显安全问题"]

def generate_report(risks: List[str]) -> Dict:
    """生成结构化安全报告"""
    return {
        "timestamp": datetime.now().isoformat(),
        "risk_count": len(risks),
        "risks": risks,
        "severity": "CRITICAL" if any("🚨" in r for r in risks) else "LOW"
    }

if __name__ == "__main__":
    from datetime import datetime
    
    risks = detect_secrets()
    print("\n".join(risks))
    
    # 生成JSON报告
    report = generate_report(risks)
    with open("security_report.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    print("\n".join(detect_secrets()))