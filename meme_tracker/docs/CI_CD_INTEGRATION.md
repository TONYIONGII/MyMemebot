# Reddit API密钥安全集成指南

## GitHub Actions 示例
```yaml
env:
  ENCRYPTION_KEY: ${{ secrets.ENCRYPTION_KEY }}

steps:
- name: Decrypt environment
  run: |
    python3 -c "
    from cryptography.fernet import Fernet
    key = b'${{ env.ENCRYPTION_KEY }}'
    cipher_suite = Fernet(key)
    with open('meme_tracker/config/.env.enc', 'rb') as f:
      with open('meme_tracker/config/.env', 'wb') as out:
        out.write(cipher_suite.decrypt(f.read()))
    "
```

## 密钥安全规范
1. 禁止将密钥提交到：
   - 代码文件
   - 版本控制历史
   - 日志文件

2. 必须配置：
```bash
# 预提交检查（.git/hooks/pre-commit）
grep -q 'i3ZqquOSq7RKnQh05Pkr5yBNbKcmXUtgZRfdd_9e2ZE=' . -r && \
  echo "❌ 密钥泄露！" && exit 1 || exit 0
```
