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

def main():
    """
    主函数，用于生成软件文件名称和对应名称的清单。
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    reading_dir = os.path.join(root_dir, "藏书阁", "阅读")

    table_data = []
    filtered_pages = []

    for filename in os.listdir(reading_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(reading_dir, filename)
            metadata = read_metadata(file_path)

            if metadata:
                start_time_str = metadata.get("开始时间")
                end_time_str = metadata.get("结束时间")
                start_time = parse_date(start_time_str) if start_time_str else None
                # 符合条件: 有开始时间,且开始时间不为空
                if start_time is not None :
                    filtered_pages.append((start_time, metadata, file_path))

    # 根据开始时间倒序排序
    filtered_pages.sort(key=lambda x: x[0], reverse=True)

    for start_time, metadata, file_path in filtered_pages:
        end_time_str = metadata.get("结束时间")
        end_time = parse_date(end_time_str) if end_time_str else None
        # 增加的判断逻辑
        if  end_time is None:
            subject_id = extract_subject_id(metadata.get("链接"))
            if subject_id and metadata.get("种类") not in ["动画", "游戏"]:
                file_name = f"bgm{subject_id}"
                title = metadata.get("标题")
                table_data.append([file_name, title])

    # 打印表格
    print("软件文件名称\t对应名称")
    print("-" * 30)
    for row in table_data:
        print(f"{row[0]}\t\t{row[1]}")

    input("按回车键退出...")

if __name__ == "__main__":
    main()