import sys
import os
import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AuthDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self._setup_ui()

    def _setup_ui(self):
        self.dialog.title("上网认证客户端")
        self.dialog.iconbitmap(resource_path("favicon.ico"))
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close)

        tk.Label(self.dialog, text="统一认证账号:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.dialog, text="统一认证密码:").grid(row=1, column=0, padx=10, pady=10)
        
        username_entry = tk.Entry(self.dialog, textvariable=self.username)
        password_entry = tk.Entry(self.dialog, textvariable=self.password, show="*")
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        submit_button = tk.Button(self.dialog, text="提交", command=self._submit)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def _submit(self):
        if self.username.get() and self.password.get():
            self.dialog.destroy()
        else:
            messagebox.showerror("错误", "账号或密码不能为空！")

    def _on_close(self):
        messagebox.showinfo("退出", "程序已退出，因为未输入账号密码。")
        try:
            self.dialog.destroy()
            self.parent.destroy()
        except tk.TclError:
            pass
        os._exit(1)

    def get_credentials(self):
        self.parent.wait_window(self.dialog)
        return self.username.get(), self.password.get()

def perform_login(username, password):
    params = {
        'callback': 'dr1730552179698',
        'DDDDD': username,
        'upass': password,
        '0MKKey': '123456',
        'R1': '0',
        'R3': '0',
        'R6': '0',
        'para': '00',
        'v6ip': '',
        '_': generate_random(13)
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.post(
            'http://192.168.8.123/drcom/login',
            params=params,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        return parse_response(response)
    except requests.RequestException as e:
        return ("错误", f"网络请求失败: {str(e)}")

def generate_random(length):
    return str(int.from_bytes(os.urandom(length), byteorder='big'))[:length]

def parse_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else ''
    
    status_mapping = {
        "信息页": ("错误", "连接失败，账号或密码不正确"),
        "认证成功页": ("成功", "已连接（Code:200）")
    }
    
    return status_mapping.get(title, ("错误", f"未知响应状态（Title: {title}）"))

def main():
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(resource_path("favicon.ico"))

    try:
        auth = AuthDialog(root)
        username, password = auth.get_credentials()
        
        if not username or not password:
            messagebox.showerror("错误", "账号或密码为空，程序退出。")
            return
        
        status, message = perform_login(username, password)
        messagebox.showinfo(status, message)
        
    except Exception as e:
        print(f"程序异常: {str(e)}")
    finally:
        try:
            if root.winfo_exists():
                root.quit()
                root.destroy()
        except tk.TclError:
            pass

if __name__ == "__main__":
    main()
