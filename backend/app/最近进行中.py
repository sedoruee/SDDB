import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk  # Import ttk for better styling
import webbrowser
import subprocess
import threading
import time

def extract_subject_id(link):
    """
    从链接中提取主题ID。
    """
    if not link:
        return None
    match = re.search(r"subject/(\d+)", link)
    return match[1] if match else None

def read_metadata(file_path):
    """
    读取Markdown文件中的元数据。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith("---"):
                metadata_str = content.split("---")[1]
                metadata = {}
                for line in metadata_str.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip().strip('"')
                return metadata
            else:
                return None
    except FileNotFoundError:
        return None

def parse_date(date_str):
    """
    将日期字符串解析为datetime对象。
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def create_launch_command(metadata, file_path):
    """
    根据页面种类创建启动命令。
    """
    subject_id = extract_subject_id(metadata.get("链接"))
    category = metadata.get("种类")
    launch_command = ""

    if category:
        if category in ["视觉小说", "游戏", "RPG", "漫画"]:
            if subject_id:
                launch_command = f'F:\\Games\\galgame\\bgm{subject_id}'
        elif category == "网课":
            launch_command = metadata.get("链接")
        elif category == "动画":
            launch_command = "D:\\Tools\\Autohotkey\\打开动画放映器.ahk"
        # 添加更多自定义种类的启动方式...

    return launch_command

def open_link(url):
    """
    使用默认浏览器打开链接。
    """
    if url:
        webbrowser.open_new(url)

def local_explorer(directory):
    """打开资源管理器并进入指定文件夹"""
    try:
        # 使用绝对路径并直接打开文件夹
        subprocess.run(['explorer', os.path.abspath(directory)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening directory: {e}")

def open_ahk(file_path):
    """运行 AutoHotkey 脚本"""
    try:
        subprocess.run(['C:\\Program Files\\AutoHotkey\\AutoHotkey.exe', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running AHK script: {e}")

def on_closing():
    """窗口关闭事件处理"""
    root.destroy()
    os._exit(0) # 强制退出程序

def refresh_data():
    """刷新数据并更新界面"""
    global recent_items
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    reading_dir = os.path.join(root_dir, "藏书阁", "阅读")

    filtered_pages = []

    for filename in os.listdir(reading_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(reading_dir, filename)
            metadata = read_metadata(file_path)

            if metadata:
                start_time_str = metadata.get("开始时间")
                end_time_str = metadata.get("结束时间")
                start_time = parse_date(start_time_str) if start_time_str else None
                end_time = parse_date(end_time_str) if end_time_str else None

                if start_time is not None and end_time is None:
                    filtered_pages.append((start_time, metadata, file_path))

    filtered_pages.sort(key=lambda x: x[0], reverse=True)
    recent_items = filtered_pages[:8]

    # 更新表格数据
    tree.delete(*tree.get_children())  # Clear existing data
    for start_time, metadata, file_path in recent_items:
        subject_id = extract_subject_id(metadata.get("链接"))
        bgm_link = f"https://bgm.tv/subject/{subject_id}" if subject_id else ""
        launch_command = create_launch_command(metadata, file_path)
        title = metadata.get('标题')
        category = metadata.get("种类") or "其他"
        category_link = metadata.get('链接') if metadata.get('链接') and category != "其他" else ""

        tree.insert("", tk.END, values=(
            "启动" if launch_command else "",
            title,
            category,
            start_time.strftime('%Y-%m-%d'),
            f"bgm{subject_id}" if subject_id else ""
        ), tags=(launch_command,bgm_link,category_link,file_path)) # Store launch command in tags

def on_double_click(event):
    """双击表格行事件处理"""
    item = tree.selection()[0]
    column = tree.identify_column(event.x)
    
    if column == "#1":
      # Handle "启动" column
      launch_command = tree.item(item,"tags")[0]
      if launch_command:
        if launch_command.startswith("http"):
            open_link(launch_command)
        elif launch_command.endswith(".ahk"):
            open_ahk(launch_command)
        else:
            local_explorer(launch_command)
    elif column == "#2":
      # Handle "标题" column
      file_path = tree.item(item,"tags")[3]
      local_explorer(os.path.dirname(file_path))
    elif column == "#3":
      # Handle "种类" column
      category_link = tree.item(item,"tags")[2]
      open_link(category_link)
    elif column == "#5":
      # Handle "Bangumi ID" column
      bgm_link = tree.item(item,"tags")[1]
      open_link(bgm_link)

def auto_refresh():
    """自动刷新数据"""
    while True:
        refresh_data()
        time.sleep(600)

# --- 主程序 ---
root = tk.Tk()
root.title("最近添加的阅读内容")

# 设置窗口大小和位置
window_width = 600  # Adjusted width
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = 0
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 表格
columns = ("启动", "标题", "种类", "开始时间", "Bangumi ID")
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")

# 设置列
tree.column("启动", width=50, anchor="center")
tree.column("标题", width=180, anchor="w")
tree.column("种类", width=80, anchor="w")
tree.column("开始时间", width=80, anchor="center")
tree.column("Bangumi ID", width=80, anchor="center")

# 设置表头
tree.heading("启动", text="启动")
tree.heading("标题", text="标题")
tree.heading("种类", text="种类")
tree.heading("开始时间", text="开始时间")
tree.heading("Bangumi ID", text="Bangumi ID")

# 绑定双击事件
tree.bind("<Double-1>", on_double_click)

# 初始数据
recent_items = []

# 初始刷新
refresh_data()

# 自动刷新线程
refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
refresh_thread.start()

# 窗口置顶且贴边
root.wm_attributes("-topmost", True)
root.bind("<Map>", lambda event: root.wm_attributes("-topmost", True))

# 关闭窗口事件
root.protocol("WM_DELETE_WINDOW", on_closing)
tree.pack(expand=True, fill="both")
root.mainloop()