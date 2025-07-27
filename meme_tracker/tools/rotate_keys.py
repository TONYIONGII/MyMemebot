import os
from cryptography.fernet import Fernet

def rotate_keys(old_key, env_path='../config/.env.enc'):
    """密钥轮换工具"""
    # 用旧密钥解密
    cipher = Fernet(old_key.encode())
    with open(env_path, 'rb') as f:
        decrypted = cipher.decrypt(f.read())

    # 生成新密钥
    new_key = Fernet.generate_key().decode()
    new_cipher = Fernet(new_key)
    
    # 重新加密
    with open(env_path, 'wb') as f:
        f.write(new_cipher.encrypt(decrypted))

    print(f"🔑 新密钥（立即保存）:\n{new_key}")
    print("⚠️ 旧密钥已失效，请更新所有系统的环境变量")

if __name__ == "__main__":
    old_key = input("输入当前密钥: ")
    rotate_keys(old_key)