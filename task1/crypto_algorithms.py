"""
密码学算法实现模块
包含DES、RSA、SHA-1算法的实现
"""

from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64


class DESCrypto:
    """DES加密解密类"""
    
    def __init__(self, key):
        """
        初始化DES密钥
        :param key: 8字节密钥
        """
        # 确保密钥是8字节
        if len(key) < 8:
            key = key.ljust(8, '0')
        elif len(key) > 8:
            key = key[:8]
        self.key = key.encode('utf-8')
    
    def encrypt(self, plaintext):
        """
        DES加密
        :param plaintext: 明文字符串
        :return: Base64编码的密文
        """
        cipher = DES.new(self.key, DES.MODE_ECB)
        # 填充明文到8字节的倍数
        padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
        # 加密
        ciphertext = cipher.encrypt(padded_text)
        # 返回Base64编码的结果
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext):
        """
        DES解密
        :param ciphertext: Base64编码的密文
        :return: 明文字符串
        """
        cipher = DES.new(self.key, DES.MODE_ECB)
        # Base64解码
        encrypted_data = base64.b64decode(ciphertext)
        # 解密
        decrypted_padded = cipher.decrypt(encrypted_data)
        # 去除填充
        plaintext = unpad(decrypted_padded, DES.block_size)
        return plaintext.decode('utf-8')


class RSACrypto:
    """RSA加密解密类"""
    
    def __init__(self, key_size=2048):
        """
        初始化RSA密钥对
        :param key_size: 密钥长度，默认2048位
        """
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self):
        """生成RSA密钥对"""
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()
    
    def get_public_key_str(self):
        """获取公钥字符串"""
        return self.public_key.export_key().decode('utf-8')
    
    def get_private_key_str(self):
        """获取私钥字符串"""
        return self.private_key.export_key().decode('utf-8')
    
    def encrypt(self, plaintext):
        """
        RSA公钥加密
        :param plaintext: 明文字符串
        :return: Base64编码的密文
        """
        cipher = PKCS1_OAEP.new(self.public_key)
        # 加密
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        # 返回Base64编码的结果
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext):
        """
        RSA私钥解密
        :param ciphertext: Base64编码的密文
        :return: 明文字符串
        """
        cipher = PKCS1_OAEP.new(self.private_key)
        # Base64解码
        encrypted_data = base64.b64decode(ciphertext)
        # 解密
        plaintext = cipher.decrypt(encrypted_data)
        return plaintext.decode('utf-8')


class SHA1Hash:
    """SHA-1哈希算法类"""
    
    @staticmethod
    def hash(message):
        """
        计算SHA-1哈希值
        :param message: 输入消息字符串
        :return: 十六进制哈希值字符串
        """
        sha1 = hashlib.sha1()
        sha1.update(message.encode('utf-8'))
        return sha1.hexdigest()
    
    @staticmethod
    def hash_file(filepath):
        """
        计算文件的SHA-1哈希值
        :param filepath: 文件路径
        :return: 十六进制哈希值字符串
        """
        sha1 = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)  # 64KB块读取
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("密码学算法测试")
    print("=" * 60)
    
    # 1. DES算法测试
    print("\n【1】DES加密解密测试")
    print("-" * 60)
    des_key = "mydeskey"
    des = DESCrypto(des_key)
    plaintext_des = "Hello, DES Encryption!"
    print(f"明文: {plaintext_des}")
    print(f"密钥: {des_key}")
    
    encrypted_des = des.encrypt(plaintext_des)
    print(f"密文(Base64): {encrypted_des}")
    
    decrypted_des = des.decrypt(encrypted_des)
    print(f"解密后: {decrypted_des}")
    print(f"验证: {'成功' if plaintext_des == decrypted_des else '失败'}")
    
    # 2. RSA算法测试
    print("\n【2】RSA加密解密测试")
    print("-" * 60)
    rsa = RSACrypto(2048)
    plaintext_rsa = "Hello, RSA Encryption!"
    print(f"明文: {plaintext_rsa}")
    print(f"密钥长度: 2048位")
    
    encrypted_rsa = rsa.encrypt(plaintext_rsa)
    print(f"密文(Base64): {encrypted_rsa[:60]}...")
    
    decrypted_rsa = rsa.decrypt(encrypted_rsa)
    print(f"解密后: {decrypted_rsa}")
    print(f"验证: {'成功' if plaintext_rsa == decrypted_rsa else '失败'}")
    
    print(f"\n公钥:\n{rsa.get_public_key_str()[:100]}...")
    print(f"\n私钥:\n{rsa.get_private_key_str()[:100]}...")
    
    # 3. SHA-1算法测试
    print("\n【3】SHA-1哈希算法测试")
    print("-" * 60)
    message_sha1 = "Hello, SHA-1 Hash!"
    print(f"消息: {message_sha1}")
    
    hash_value = SHA1Hash.hash(message_sha1)
    print(f"SHA-1哈希值: {hash_value}")
    print(f"哈希长度: {len(hash_value)}个十六进制字符 (160位)")
    
    # 验证相同输入产生相同哈希
    hash_value2 = SHA1Hash.hash(message_sha1)
    print(f"再次计算: {hash_value2}")
    print(f"验证: {'成功(哈希值一致)' if hash_value == hash_value2 else '失败'}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
