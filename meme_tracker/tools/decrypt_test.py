import os
from cryptography.fernet import Fernet

def decrypt_file(encrypted_path, key):
    """解密文件测试"""
    cipher_suite = Fernet(key.encode())
    with open(encrypted_path, 'rb') as f:
        return cipher_suite.decrypt(f.read()).decode()

if __name__ == "__main__":
    key = input("请输入加密密钥: ")
    encrypted_path = os.path.join(os.path.dirname(__file__), "../config/.env.enc")
    
    try:
        content = decrypt_file(encrypted_path, key)
        print("✅ 解密成功（前100字符）:\n", content[:100] + "...")
    except Exception as e:
        print("❌ 解密失败:", str(e))