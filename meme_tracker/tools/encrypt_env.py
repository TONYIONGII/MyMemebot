import os
from cryptography.fernet import Fernet

def encrypt_file(input_path, output_path):
    """加密文件函数"""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    
    with open(input_path, 'rb') as f:
        encrypted = cipher_suite.encrypt(f.read())
    
    with open(output_path, 'wb') as f:
        f.write(encrypted)
    
    return key.decode()

if __name__ == "__main__":
    env_path = os.path.join(os.path.dirname(__file__), "../config/.env")
    encrypted_path = os.path.join(os.path.dirname(__file__), "../config/.env.enc")
    
    if os.path.exists(env_path):
        key = encrypt_file(env_path, encrypted_path)
        print(f"🔑 加密密钥（妥善保存）:\n{key}")
        print(f"🔒 加密文件已保存至: {encrypted_path}")
    else:
        print("❌ 未找到.env文件，请检查路径")