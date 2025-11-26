"""
密码学算法图形化界面应用
提供DES、RSA、SHA-1算法的可视化操作界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from crypto_algorithms import DESCrypto, RSACrypto, SHA1Hash
import traceback


class CryptoGUI:
    """密码学算法图形界面类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("密码学算法实验系统")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # RSA密钥对实例
        self.rsa = None
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # DES选项卡
        self.create_des_tab()
        
        # RSA选项卡
        self.create_rsa_tab()
        
        # SHA-1选项卡
        self.create_sha1_tab()
    
    def create_des_tab(self):
        """创建DES算法选项卡"""
        des_frame = ttk.Frame(self.notebook)
        self.notebook.add(des_frame, text="DES加密解密")
        
        # 密钥输入
        key_frame = ttk.LabelFrame(des_frame, text="DES密钥设置", padding=10)
        key_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(key_frame, text="密钥(8字节):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.des_key_entry = ttk.Entry(key_frame, width=50)
        self.des_key_entry.grid(row=0, column=1, padx=5, pady=5)
        self.des_key_entry.insert(0, "mydeskey")
        
        # 明文输入
        plain_frame = ttk.LabelFrame(des_frame, text="明文输入", padding=10)
        plain_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.des_plain_text = scrolledtext.ScrolledText(plain_frame, height=6, width=80)
        self.des_plain_text.pack(fill=tk.BOTH, expand=True)
        self.des_plain_text.insert(1.0, "Hello, 这是DES加密测试!")
        
        # 操作按钮
        btn_frame = ttk.Frame(des_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="加密", command=self.des_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="解密", command=self.des_decrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空", command=self.des_clear).pack(side=tk.LEFT, padx=5)
        
        # 密文/结果显示
        cipher_frame = ttk.LabelFrame(des_frame, text="密文/解密结果", padding=10)
        cipher_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.des_cipher_text = scrolledtext.ScrolledText(cipher_frame, height=6, width=80)
        self.des_cipher_text.pack(fill=tk.BOTH, expand=True)
    
    def create_rsa_tab(self):
        """创建RSA算法选项卡"""
        rsa_frame = ttk.Frame(self.notebook)
        self.notebook.add(rsa_frame, text="RSA加密解密")
        
        # 密钥生成
        key_frame = ttk.LabelFrame(rsa_frame, text="RSA密钥对生成", padding=10)
        key_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(key_frame, text="密钥长度:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.rsa_key_size = ttk.Combobox(key_frame, values=[1024, 2048, 3072, 4096], width=15)
        self.rsa_key_size.set(2048)
        self.rsa_key_size.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(key_frame, text="生成密钥对", command=self.rsa_generate_keys).grid(row=0, column=2, padx=5)
        self.rsa_key_status = ttk.Label(key_frame, text="未生成", foreground="red")
        self.rsa_key_status.grid(row=0, column=3, padx=5)
        
        # 明文输入
        plain_frame = ttk.LabelFrame(rsa_frame, text="明文输入", padding=10)
        plain_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.rsa_plain_text = scrolledtext.ScrolledText(plain_frame, height=4, width=80)
        self.rsa_plain_text.pack(fill=tk.BOTH, expand=True)
        self.rsa_plain_text.insert(1.0, "Hello, RSA!")
        
        # 操作按钮
        btn_frame = ttk.Frame(rsa_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="公钥加密", command=self.rsa_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="私钥解密", command=self.rsa_decrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空", command=self.rsa_clear).pack(side=tk.LEFT, padx=5)
        
        # 密文/结果显示
        cipher_frame = ttk.LabelFrame(rsa_frame, text="密文/解密结果", padding=10)
        cipher_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.rsa_cipher_text = scrolledtext.ScrolledText(cipher_frame, height=4, width=80)
        self.rsa_cipher_text.pack(fill=tk.BOTH, expand=True)
        
        # 密钥显示
        keys_frame = ttk.LabelFrame(rsa_frame, text="密钥信息", padding=10)
        keys_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.rsa_keys_text = scrolledtext.ScrolledText(keys_frame, height=6, width=80)
        self.rsa_keys_text.pack(fill=tk.BOTH, expand=True)
    
    def create_sha1_tab(self):
        """创建SHA-1算法选项卡"""
        sha1_frame = ttk.Frame(self.notebook)
        self.notebook.add(sha1_frame, text="SHA-1哈希")
        
        # 消息输入
        msg_frame = ttk.LabelFrame(sha1_frame, text="消息输入", padding=10)
        msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.sha1_message_text = scrolledtext.ScrolledText(msg_frame, height=8, width=80)
        self.sha1_message_text.pack(fill=tk.BOTH, expand=True)
        self.sha1_message_text.insert(1.0, "Hello, 这是SHA-1哈希测试消息!")
        
        # 操作按钮
        btn_frame = ttk.Frame(sha1_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="计算哈希值", command=self.sha1_hash).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空", command=self.sha1_clear).pack(side=tk.LEFT, padx=5)
        
        # 哈希值显示
        hash_frame = ttk.LabelFrame(sha1_frame, text="SHA-1哈希值(160位/40个十六进制字符)", padding=10)
        hash_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.sha1_hash_text = scrolledtext.ScrolledText(hash_frame, height=8, width=80)
        self.sha1_hash_text.pack(fill=tk.BOTH, expand=True)
    
    # DES相关方法
    def des_encrypt(self):
        """DES加密"""
        try:
            key = self.des_key_entry.get()
            plaintext = self.des_plain_text.get(1.0, tk.END).strip()
            
            if not key or not plaintext:
                messagebox.showwarning("警告", "请输入密钥和明文!")
                return
            
            des = DESCrypto(key)
            ciphertext = des.encrypt(plaintext)
            
            self.des_cipher_text.delete(1.0, tk.END)
            self.des_cipher_text.insert(1.0, ciphertext)
            
            messagebox.showinfo("成功", "DES加密完成!")
        except Exception as e:
            messagebox.showerror("错误", f"加密失败:\n{str(e)}")
            traceback.print_exc()
    
    def des_decrypt(self):
        """DES解密"""
        try:
            key = self.des_key_entry.get()
            ciphertext = self.des_cipher_text.get(1.0, tk.END).strip()
            
            if not key or not ciphertext:
                messagebox.showwarning("警告", "请输入密钥和密文!")
                return
            
            des = DESCrypto(key)
            plaintext = des.decrypt(ciphertext)
            
            self.des_cipher_text.delete(1.0, tk.END)
            self.des_cipher_text.insert(1.0, f"解密结果:\n{plaintext}")
            
            messagebox.showinfo("成功", "DES解密完成!")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败:\n{str(e)}")
            traceback.print_exc()
    
    def des_clear(self):
        """清空DES相关文本框"""
        self.des_plain_text.delete(1.0, tk.END)
        self.des_cipher_text.delete(1.0, tk.END)
    
    # RSA相关方法
    def rsa_generate_keys(self):
        """生成RSA密钥对"""
        try:
            key_size = int(self.rsa_key_size.get())
            self.rsa = RSACrypto(key_size)
            
            self.rsa_key_status.config(text="已生成", foreground="green")
            
            # 显示密钥信息
            self.rsa_keys_text.delete(1.0, tk.END)
            keys_info = f"【公钥】\n{self.rsa.get_public_key_str()}\n\n"
            keys_info += f"【私钥】\n{self.rsa.get_private_key_str()}"
            self.rsa_keys_text.insert(1.0, keys_info)
            
            messagebox.showinfo("成功", f"RSA密钥对生成完成!\n密钥长度: {key_size}位")
        except Exception as e:
            messagebox.showerror("错误", f"密钥生成失败:\n{str(e)}")
            traceback.print_exc()
    
    def rsa_encrypt(self):
        """RSA公钥加密"""
        try:
            if not self.rsa:
                messagebox.showwarning("警告", "请先生成RSA密钥对!")
                return
            
            plaintext = self.rsa_plain_text.get(1.0, tk.END).strip()
            
            if not plaintext:
                messagebox.showwarning("警告", "请输入明文!")
                return
            
            ciphertext = self.rsa.encrypt(plaintext)
            
            self.rsa_cipher_text.delete(1.0, tk.END)
            self.rsa_cipher_text.insert(1.0, ciphertext)
            
            messagebox.showinfo("成功", "RSA公钥加密完成!")
        except Exception as e:
            messagebox.showerror("错误", f"加密失败:\n{str(e)}\n\n提示:RSA加密有长度限制")
            traceback.print_exc()
    
    def rsa_decrypt(self):
        """RSA私钥解密"""
        try:
            if not self.rsa:
                messagebox.showwarning("警告", "请先生成RSA密钥对!")
                return
            
            ciphertext = self.rsa_cipher_text.get(1.0, tk.END).strip()
            
            if not ciphertext:
                messagebox.showwarning("警告", "请输入密文!")
                return
            
            plaintext = self.rsa.decrypt(ciphertext)
            
            self.rsa_cipher_text.delete(1.0, tk.END)
            self.rsa_cipher_text.insert(1.0, f"解密结果:\n{plaintext}")
            
            messagebox.showinfo("成功", "RSA私钥解密完成!")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败:\n{str(e)}")
            traceback.print_exc()
    
    def rsa_clear(self):
        """清空RSA相关文本框"""
        self.rsa_plain_text.delete(1.0, tk.END)
        self.rsa_cipher_text.delete(1.0, tk.END)
    
    # SHA-1相关方法
    def sha1_hash(self):
        """计算SHA-1哈希值"""
        try:
            message = self.sha1_message_text.get(1.0, tk.END).strip()
            
            if not message:
                messagebox.showwarning("警告", "请输入消息!")
                return
            
            hash_value = SHA1Hash.hash(message)
            
            # 显示详细信息
            result = f"消息: {message}\n\n"
            result += f"SHA-1哈希值:\n{hash_value}\n\n"
            result += f"哈希长度: {len(hash_value)}个十六进制字符 (160位)\n"
            result += f"字节表示: {len(hash_value)//2}字节\n\n"
            
            # 验证一致性
            hash_value2 = SHA1Hash.hash(message)
            result += f"再次计算: {hash_value2}\n"
            result += f"一致性验证: {'✓ 通过(相同输入产生相同哈希)' if hash_value == hash_value2 else '✗ 失败'}"
            
            self.sha1_hash_text.delete(1.0, tk.END)
            self.sha1_hash_text.insert(1.0, result)
            
            messagebox.showinfo("成功", "SHA-1哈希计算完成!")
        except Exception as e:
            messagebox.showerror("错误", f"哈希计算失败:\n{str(e)}")
            traceback.print_exc()
    
    def sha1_clear(self):
        """清空SHA-1相关文本框"""
        self.sha1_message_text.delete(1.0, tk.END)
        self.sha1_hash_text.delete(1.0, tk.END)


def main():
    """主函数"""
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()





