import os
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

def encrypt_env_file(key, input_path='.env', output_path='.env.enc'):
    """
    加密环境文件
    
    参数:
        key: 加密密钥(字符串)
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    try:
        # 确保输入文件存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件 {input_path} 不存在")
            
        # 创建输出目录(如果不存在)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 读取原始文件内容
        with open(input_path, 'rb') as f:
            original = f.read()
            
        # 加密内容
        cipher = Fernet(key.encode())
        encrypted = cipher.encrypt(original)
        
        # 写入加密文件
        with open(output_path, 'wb') as f:
            f.write(encrypted)
            
        print(f"成功加密文件并保存到 {output_path}")
        
    except InvalidToken:
        print("错误: 无效的加密密钥")
    except Exception as e:
        print(f"加密过程中发生错误: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='加密环境文件')
    parser.add_argument('--key', required=True, help='加密密钥')
    parser.add_argument('--input', default='.env', help='输入文件路径')
    parser.add_argument('--output', default='.env.enc', help='输出文件路径')
    
    args = parser.parse_args()
    encrypt_env_file(args.key, args.input, args.output)