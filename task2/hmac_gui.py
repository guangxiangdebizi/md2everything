import tkinter as tk
from tkinter import ttk, messagebox
import hmac
import hashlib

class HMACTool:
    def __init__(self, root):
        self.root = root
        self.root.title("HMAC 计算工具")
        self.root.geometry("500x400")

        # Key Input
        tk.Label(root, text="密钥 (Key):").pack(pady=5)
        self.key_entry = tk.Entry(root, width=50)
        self.key_entry.pack(pady=5)

        # Message Input
        tk.Label(root, text="消息 (Message):").pack(pady=5)
        self.msg_text = tk.Text(root, height=5, width=50)
        self.msg_text.pack(pady=5)

        # Algorithm Selection
        tk.Label(root, text="哈希算法:").pack(pady=5)
        self.algo_var = tk.StringVar(value="sha256")
        self.algo_combo = ttk.Combobox(root, textvariable=self.algo_var, values=["md5", "sha1", "sha256", "sha512"])
        self.algo_combo.pack(pady=5)

        # Calculate Button
        tk.Button(root, text="计算 HMAC", command=self.calculate_hmac).pack(pady=10)

        # Result Output
        tk.Label(root, text="HMAC (Hex):").pack(pady=5)
        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(root, textvariable=self.result_var, width=60, state='readonly')
        self.result_entry.pack(pady=5)

    def calculate_hmac(self):
        key = self.key_entry.get()
        msg = self.msg_text.get("1.0", tk.END).strip()
        algo_name = self.algo_var.get()

        if not key:
            messagebox.showerror("错误", "请输入密钥")
            return
        if not msg:
            messagebox.showerror("错误", "请输入消息")
            return

        try:
            # Convert string to bytes
            key_bytes = key.encode('utf-8')
            msg_bytes = msg.encode('utf-8')
            
            # Get digestmod
            digestmod = getattr(hashlib, algo_name)
            
            # Calculate HMAC
            h = hmac.new(key_bytes, msg_bytes, digestmod)
            hmac_hex = h.hexdigest()
            
            self.result_var.set(hmac_hex)
        except Exception as e:
            messagebox.showerror("错误", f"计算失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HMACTool(root)
    root.mainloop()

