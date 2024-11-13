import subprocess
import platform
import sys
import os

def send_notification(title, message):
    """
    根据操作系统发送通知。

    参数:
    title (str): 通知的标题。
    message (str): 通知的消息内容。

    此函数检查当前操作系统，并使用相应的方式发送通知。
    支持的系统包括 Linux, macOS (Darwin) 和 Windows。
    """
    # 获取当前系统名称
    system = platform.system()

    # 根据系统类型发送通知
    if system == "Linux":
        # 在 Linux 系统上使用 notify-send 命令发送通知
        subprocess.run(["notify-send", title, message])
    elif system == "Darwin":  # macOS
        # 在 macOS 上使用 osascript 命令发送通知
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    elif system == "Windows":
        # 在 Windows 系统上使用 powershell 命令发送通知
        script = f'[System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
        subprocess.run(["powershell", "-command", script])
    else:
        # 当系统不支持时，打印错误信息
        print(f"Unsupported platform: {system}")




#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)