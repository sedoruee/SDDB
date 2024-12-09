import subprocess
import os
import sys

def install_package(package):
    """
    安装指定的Python库。
    """
    print(f"正在安装 {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_requests():
    """
    检查requests库是否存在，如果不存在则安装并重新运行脚本。
    """
    try:
        import requests
    except ImportError:
        print("缺少 requests 库。")
        install_package("requests")
        print("requests 库已安装完毕，正在重新运行脚本...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    return requests

def get_data_from_url(url, requests_lib):
    """
    从指定URL获取数据。
    """
    try:
        response = requests_lib.get(url)
        response.raise_for_status()
        return response.json()
    except requests_lib.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def process_data(data, requests_lib):
    """
    处理获取的数据，如果符合条件则执行指定操作。
    """
    if data and isinstance(data, dict) and data.get("type") == "bilibili_latest_Episode":
        print("数据类型匹配，正在执行 写入哔哩哔哩存档.py")
        script_path = os.path.join(os.path.dirname(__file__), "api中转站", "写入哔哩哔哩存档.py")
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path])
        else:
            print(f"文件 {script_path} 不存在。")

if __name__ == "__main__":
    requests_lib = check_requests()

    target_url = "http://localhost:8964/"
    data = get_data_from_url(target_url, requests_lib)
    process_data(data, requests_lib)