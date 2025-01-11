import os
import re
import pyperclip
import time
import threading

# 定义根文件夹和 Obsidian Vault 路径
ROOT_FOLDERS = ["F:\\Games\\galgame", "X:\\Game\\galgame", "J:\\Games\\galme"]
OBSIDIAN_VAULT = "D:\\Obsidian\\藏书阁\\阅读"

def extract_category(clip_text):
    match = re.search(r"类型: (.+?)\n种类:", clip_text)
    return match.group(1) if match else None

def extract_subject_id(url):
    match = re.search(r"subject/(\d+)", url)
    return match.group(1) if match else None

def extract_title(clip_text):
    match = re.search(r"标题: (.+?)\n链接:", clip_text)
    return match.group(1) if match else None

def clean_file_name(file_name):
    return re.sub(r'[<>:".|?*\/, ]+', "_", file_name)

def open_or_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "created"
    return "exists"

def create_markdown_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return "created" if os.path.exists(file_path) else "failed"

def check_file_exist(file_pattern, clean_title):
    # 精确匹配文件名
    if os.path.exists(file_pattern):
        return file_pattern
    else:
        return None

def main():
    # 从剪贴板获取内容
    clipboard = pyperclip.paste()
    
    # 提取 Bangumi 链接和种类
    url_match = re.search(r"链接: (.+)", clipboard)
    bgm_url = url_match.group(1) if url_match else None
    category = extract_category(clipboard)
    
    if not bgm_url:
        print("无法从剪贴板中提取 Bangumi 链接。")
    
    subject_id = extract_subject_id(bgm_url)
    if not subject_id:
        print("无法从剪贴板中提取 Bangumi 主题 ID。")
    
    game_title = extract_title(clipboard)
    if not game_title:
        print("无法从剪贴板中提取标题。")
    
    clean_title = clean_file_name(game_title)
    markdown_file_path = os.path.join(OBSIDIAN_VAULT, f"{clean_title}.md")
    
# 判断是否需要创建文件夹（仅当种类为“游戏”时）
    target_folder = None
    note_folder_found = False
    game_folder_found = False

    if category == "游戏":
        print("判断为游戏，正在准备检测文件夹")

        # 检查是否存在笔记文件夹
        if os.path.exists(markdown_file_path):
            note_folder_found = True
            print("检测到笔记文件夹/Markdown 文件存在")

        # 检查是否存在游戏文件夹
        for root_folder in ROOT_FOLDERS:
            folder_path = os.path.join(root_folder, f"bgm{subject_id}")
            if os.path.exists(folder_path):
                game_folder_found = True
                target_folder = folder_path
                print("检测到游戏文件夹存在")
                break

        # 根据检测结果进行处理
        if note_folder_found and game_folder_found:
            print(f"笔记和游戏文件夹均存在，打开游戏文件夹: {target_folder}")
            os.startfile(target_folder)
            return
        elif note_folder_found and not game_folder_found:
            print("仅检测到笔记文件夹，游戏文件夹缺失")
            create_game_folder = input("是否创建游戏文件夹？(回车创建，其他键跳过): ").strip().lower()
            if create_game_folder == "":
                for root_folder in ROOT_FOLDERS:
                    folder_path = os.path.join(root_folder, f"bgm{subject_id}")
                    result = open_or_create_folder(folder_path)
                    if result == "created":
                        target_folder = folder_path
                        print(f"成功创建游戏文件夹: {target_folder}")
                        break
        elif not note_folder_found and game_folder_found:
            print(f"仅检测到游戏文件夹，打开游戏文件夹: {target_folder}")
            os.startfile(target_folder)
            create_note_file = input("是否创建笔记文件/Markdown？(回车创建，其他键跳过): ").strip().lower()
            if create_note_file == "":
                result = create_markdown_file(markdown_file_path, clipboard)
                print(f"Markdown 文件创建结果: {result}")
        else:
            print("笔记文件夹和游戏文件夹均未找到")
            create_folder_md = input("是否创建文件夹和Markdown文件？(回车一起创建，1单独创建文件夹，2单独创建Markdown): ").strip().lower()
            if create_folder_md == "" or create_folder_md == "1":
                for root_folder in ROOT_FOLDERS:
                    folder_path = os.path.join(root_folder, f"bgm{subject_id}")
                    result = open_or_create_folder(folder_path)
                    if result == "created":
                        target_folder = folder_path
                        print(f"成功创建游戏文件夹: {target_folder}")
                        break
            if create_folder_md == "" or create_folder_md == "2":
                if not os.path.exists(markdown_file_path):
                    result = create_markdown_file(markdown_file_path, clipboard)
                    print(f"Markdown 文件创建结果: {result}")
                else:
                    print(f"已存在 Markdown 文件: {markdown_file_path}")

    if category != "游戏":
    	print("判断非游戏,跳过游戏文件夹相关处理")
    # 判断 Markdown 文件是否存在
    existing_file = check_file_exist(markdown_file_path, clean_title)
    if existing_file:
        print(f"已存在 Markdown 文件: {existing_file}")
        os.startfile(f"obsidian://open?vault=Obsidian&file={clean_title}")
    else:
        print("Markdown 文件未找到。")
        create_md = input("是否创建 Markdown 文件？(回车或1创建, 其它键取消): ").strip().lower()
        if create_md == "" or create_md == "1":
            result = create_markdown_file(markdown_file_path, clipboard)
            print(f"Markdown 文件创建结果: {result}")
            print(f"祝您旅途愉快")

    # 打开文件夹或文件
    if target_folder and not os.path.exists(markdown_file_path):
        print(f"打开游戏文件夹: {target_folder}")
        os.startfile(target_folder)
    if not existing_file and os.path.exists(markdown_file_path):
        print(f"打开新创建的 Markdown 文件: {markdown_file_path}")
        os.startfile(f"obsidian://open?vault=Obsidian&file={clean_title}")

    
def timeout_exit(timeout):
    time.sleep(timeout)
    print("\n超时自动退出...")
    os._exit(0)  # 使用 os._exit(0) 强制退出

if __name__ == "__main__":
    main()
    timeout = 5  # 设置超时时间，单位为秒
    timer = threading.Thread(target=timeout_exit, args=(timeout,))
    timer.daemon = True  # 设置为守护线程，主线程结束时自动退出
    timer.start()

    input("按任意键退出或者{}秒后自动退出...".format(timeout))