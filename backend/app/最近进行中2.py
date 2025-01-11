import os
import re
from datetime import datetime

def extract_subject_id(link):
    """
    从链接中提取主题ID。

    Args:
        link: 包含主题ID的链接字符串。

    Returns:
        主题ID（字符串），如果链接无效或未找到主题ID，则返回None。
    """
    if not link:
        return None
    match = re.search(r"subject/(\d+)", link)
    return match[1] if match else None

def read_metadata(file_path):
    """
    读取Markdown文件中的元数据。

    Args:
        file_path: Markdown文件的路径。

    Returns:
        包含元数据的字典，如果文件不存在或元数据格式不正确，则返回None。
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

    Args:
        date_str: 日期字符串，格式为YYYY-MM-DD。

    Returns:
        datetime对象，如果日期字符串格式不正确，则返回None。
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def create_launch_command(metadata, file_path):
    """
    根据页面种类创建启动命令。

    Args:
        metadata: 包含页面元数据的字典。
        file_path: 文件的路径。

    Returns:
        启动命令字符串，如果不需要启动命令，则返回空字符串。
    """
    subject_id = extract_subject_id(metadata.get("链接"))
    category = metadata.get("种类")
    launch_command = ""

    if category:
        if category in ["视觉小说", "游戏", "RPG", "漫画"]:
            if subject_id:
                launch_command = f'localexplorer:"F:\\Games\\galgame\\bgm{subject_id}"'
        elif category == "网课":
            launch_command = metadata.get("链接")
        elif category == "动画":
            launch_command = "file:///D:/Tools/Autohotkey/打开动画放映器.ahk"
        # 添加更多自定义种类的启动方式...

    return launch_command

def main():
    """
    主函数，生成最近添加的阅读内容表格。
    """
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
                
                # 符合条件: 有开始时间,且开始时间不为空,且结束时间为空
                if start_time is not None and end_time is None :
                    filtered_pages.append((start_time, metadata, file_path))

    # 根据开始时间倒序排序
    filtered_pages.sort(key=lambda x: x[0], reverse=True)

    # 只保留最近8条
    recent_items = filtered_pages[:8]

    # 打印表格
    print("| 启动 | 标题 | 种类 | 开始时间 | Bangumi ID |")
    print("|---|---|---|---|---|")
    for start_time, metadata, file_path in recent_items:
        subject_id = extract_subject_id(metadata.get("链接"))
        bgm_link = f"[bgm{subject_id}](https://bgm.tv/subject/{subject_id})" if subject_id else ""
        launch_command = create_launch_command(metadata, file_path)
        launch_button = f"[启动]({launch_command})" if launch_command else ""
        title_link = f"[{metadata.get('标题')}]({file_path})"
        category = metadata.get("种类") or "其他"
        category_link = f"[{category}]({metadata.get('链接')})" if metadata.get('链接') and category != "其他" else category
        print(f"| {launch_button} | {title_link} | {category_link} | {start_time.strftime('%Y-%m-%d')} | {bgm_link} |")

    input("按回车键退出...")

if __name__ == "__main__":
    main()