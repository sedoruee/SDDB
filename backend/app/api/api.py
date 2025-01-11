import subprocess
import sys
import time
import threading
import json
import base64

def install_and_import(package):
    """
    安装并导入一个包。

    Args:
        package: 要安装的包的名称。
    """
    try:
        __import__(package)
    except ImportError:
        print(f"缺少模块 {package}，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"模块 {package} 安装完成。")

# 安装并导入所需的包
install_and_import("flask")

from flask import Flask, jsonify, request

app = Flask(__name__)

# 初始固定数值，使用字典存储，方便修改
api_data = {
    "api_endpoint": "/",  # 默认的 API 端点
    "fixed_value": {"value": 123}  # 初始值
}

# 互斥锁，用于线程安全地更新 api_data
data_lock = threading.Lock()

def run_api_relay_station():
    """
    运行 api_relay_station.py 脚本。
    """
    try:
        subprocess.run([sys.executable, "api_relay_station.py"], check=True)
        print("api_relay_station.py 执行完毕。")
    except subprocess.CalledProcessError as e:
        print(f"执行 api_relay_station.py 失败: {e}")
    except Exception as e:
        print(f"运行 api_relay_station.py 时发生错误: {e}")

@app.route('/', methods=['GET'])
def get_value():
    """
    获取当前固定数值的 API 端点。
    """
    with data_lock:
        return jsonify(api_data["fixed_value"])

@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    """
    捕获所有 GET 请求，并根据配置的 api_endpoint 返回数据
    """
    with data_lock:
      if path == api_data["api_endpoint"].lstrip('/'):
          return jsonify(api_data["fixed_value"])
      else:
        return jsonify({"error": "Not Found"}), 404

@app.route('/', methods=['POST'])
def update_value():
    """
    更新固定数值的 API 端点。
    """
    try:
        data = request.get_json()
        if "value" in data:
            with data_lock:
                api_data["fixed_value"]["value"] = data["value"]
            run_api_relay_station()  # 在这里调用
            return jsonify({"message": "数值更新成功", "new_value": api_data["fixed_value"]["value"]})
        else:
            return jsonify({"error": "请求中缺少 'value' 字段"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 删除 @app.route('/write/<base64_encoded>', methods=['GET']) 及其相关函数 write_to_api

@app.route('/update_api', methods=['POST'])
def update_api_config():
    """
    通过 POST 请求更新 API 配置。
    预期接收 JSON 格式的数据，例如：
    {
        "api_endpoint": "/new_endpoint",
        "fixed_value": {"value": 456}
    }
    或者
    {
        "api_endpoint": "/another_endpoint",
        "fixed_value": {"key1": "value1", "key2": 123}
    }
    """
    try:
        data = request.get_json()
        with data_lock:
            if "api_endpoint" in data:
                api_data["api_endpoint"] = data["api_endpoint"]
            if "fixed_value" in data:
                api_data["fixed_value"] = data["fixed_value"]
        run_api_relay_station() # 在这里调用
        return jsonify({"message": "API 配置更新成功", "new_data": api_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_api():
    """
    运行 Flask API。
    """
    app.run(host='0.0.0.0', port=8964)

def keep_terminal_open():
    """
    保持命令面板打开，直到用户按下 Ctrl+C。
    """
    try:
        while True:
            time.sleep(1)  # 每秒检查一次
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C，正在关闭 API...")
        sys.exit(0)

if __name__ == '__main__':
    api_thread = threading.Thread(target=run_api)
    api_thread.daemon = True  # 设置为守护线程，以便主线程退出时 API 线程也能退出
    api_thread.start()

    keep_terminal_open()