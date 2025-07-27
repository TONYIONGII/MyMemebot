import unittest
from meme_tracker.utils.crypto_utils import CryptoManager

class TestCryptoUtils(unittest.TestCase):
    def setUp(self):
        """使用临时密钥初始化"""
        self.test_key = CryptoManager.generate_key()
        self.crypto = CryptoManager(self.test_key)

    def test_encrypt_decrypt(self):
        """测试加密解密流程"""
        original = "This is a secret message"
        encrypted = self.crypto.encrypt(original)
        decrypted = self.crypto.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_bytes_handling(self):
        """测试字节数据加密"""
        original = b"Binary data \x00\x01"
        encrypted = self.crypto.encrypt(original)
        decrypted = self.crypto.decrypt(encrypted)
        self.assertEqual(original, decrypted.encode('utf-8'))

    def test_key_rotation(self):
        """测试密钥轮换"""
        new_key = CryptoManager.generate_key()
        new_crypto = CryptoManager(new_key)
        
        # 旧密钥加密的数据应该无法用新密钥解密
        encrypted = self.crypto.encrypt("test")
        with self.assertRaises(Exception):
            new_crypto.decrypt(encrypted)

if __name__ == '__main__':
    unittest.main()